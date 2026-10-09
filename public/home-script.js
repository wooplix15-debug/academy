(() => {
  const menu = document.querySelector('.nav-toggle');
  const nav = document.querySelector('#brand-nav');

  const closeMenu = () => {
    nav?.classList.remove('is-open');
    menu?.setAttribute('aria-expanded', 'false');
    menu?.setAttribute('aria-label', 'Open menu');
  };

  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    nav?.classList.toggle('is-open', open);
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
  document.querySelectorAll('[data-brand-year]').forEach(label => { label.textContent = new Date().getFullYear(); });

  const siteNav = document.querySelector('.site-nav');
  const hero = document.querySelector('.hero-stage');
  const progress = document.querySelector('.page-progress span');
  let scrollFrame = 0;

  const updatePageChrome = () => {
    scrollFrame = 0;
    const scrollTop = window.scrollY;
    const heroThreshold = hero ? Math.max(180, hero.offsetHeight - 96) : 180;
    siteNav?.classList.toggle('is-past-hero', scrollTop > heroThreshold);

    if (progress) {
      const available = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = available > 0 ? Math.min(1, Math.max(0, scrollTop / available)) : 0;
      progress.style.transform = `scaleX(${ratio})`;
    }
  };

  const requestChromeUpdate = () => {
    if (scrollFrame) return;
    scrollFrame = window.requestAnimationFrame(updatePageChrome);
  };

  window.addEventListener('scroll', requestChromeUpdate, { passive: true });
  window.addEventListener('resize', requestChromeUpdate, { passive: true });
  updatePageChrome();

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll(
    '.statement-grid, .stat-grid > div, .signature-grid > div, .section-heading, .service-card, .timeline article, .wooplix-card, .framework-card, .work-tiles article, .philosophy-copy, .course-preview, .cta-section'
  );

  if (!reduceMotion && 'IntersectionObserver' in window && revealItems.length) {
    document.documentElement.classList.add('motion-ready');
    revealItems.forEach((item, index) => {
      item.classList.add('reveal-item');
      item.style.setProperty('--reveal-delay', `${(index % 4) * 70}ms`);
    });
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealItems.forEach(item => revealObserver.observe(item));
  }

  const slides = [...document.querySelectorAll('.hero-slide')];
  const slideButtons = [...document.querySelectorAll('[data-slide-index]')];
  const currentSlide = document.querySelector('[data-slide-current]');
  let slideIndex = slides.findIndex(slide => slide.classList.contains('is-active'));
  if (slides.length) {
    const showSlide = index => {
      slideIndex = (index + slides.length) % slides.length;
      slides.forEach((slide, position) => slide.classList.toggle('is-active', position === slideIndex));
      slideButtons.forEach((button, position) => {
        const active = position === slideIndex;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });
      if (currentSlide) currentSlide.textContent = String(slideIndex + 1).padStart(2, '0');
    };
    slideButtons.forEach(button => button.addEventListener('click', () => showSlide(Number(button.dataset.slideIndex))));
    if (!reduceMotion && slides.length > 1) {
      window.setInterval(() => {
        if (document.visibilityState === 'visible') showSlide(slideIndex + 1);
      }, 6500);
    }
  }

  const form = document.querySelector('#enquiry-form');
  if (!form) return;

  const params = new URLSearchParams(window.location.search);
  const serviceInputs = [...form.querySelectorAll('input[name="service"]')];
  const serviceFields = [...form.querySelectorAll('[data-service-fields]')];
  const status = document.querySelector('#enquiry-status');
  const fallback = document.querySelector('#enquiry-fallback');
  const fallbackText = document.querySelector('#enquiry-copy-text');
  const services = ['AI consulting', 'Speaking enquiry', 'Course enquiry', 'General enquiry'];

  const selectedService = () => serviceInputs.find(input => input.checked)?.value || 'AI consulting';
  const showServiceFields = () => {
    const selected = selectedService();
    serviceFields.forEach(section => { section.hidden = section.dataset.serviceFields !== selected; });
  };
  const selectService = service => {
    const input = serviceInputs.find(candidate => candidate.value === service);
    if (input) input.checked = true;
    showServiceFields();
  };

  serviceInputs.forEach(input => input.addEventListener('change', showServiceFields));
  if (services.includes(params.get('service'))) selectService(params.get('service'));
  if (['30', '60'].includes(params.get('duration')) && form.elements.duration) form.elements.duration.value = params.get('duration');
  showServiceFields();

  const compose = () => {
    const data = new FormData(form);
    const service = selectedService();
    const duration = data.get('duration') || 'Not specified';
    const session = duration === 'Not specified' ? duration : `${duration} minutes`;
    const lines = [
      `Name: ${data.get('name') || 'Not specified'}`,
      `Email: ${data.get('email') || 'Not specified'}`,
      `Organisation: ${data.get('organisation') || 'Not specified'}`,
      `Industry: ${data.get('industry') || 'Not specified'}`,
      `Location / time zone: ${data.get('timezone') || 'Not specified'}`,
      `Preferred timing: ${data.get('timing') || 'Not specified'}`,
      `Enquiry type: ${service}`,
    ];
    if (service === 'AI consulting') lines.push(`Preferred discussion: ${session}`);
    if (service === 'Speaking enquiry') lines.push(`Audience: ${data.get('audience') || 'Not specified'}`, `Event format: ${data.get('format') || 'Not specified'}`);
    if (service === 'Course enquiry') lines.push(`Programme: ${data.get('programme') || 'Not specified'}`, `Learners / team size: ${data.get('learners') || 'Not specified'}`);
    lines.push('', 'Question or brief:', data.get('message') || '', '', 'Please confirm availability, scope and fees.');
    return {
      subject: `Vivek Pandey — ${service}${duration === 'Not specified' ? '' : ` (${session})`}`,
      body: lines.join('\n'),
    };
  };

  const showFallback = enquiry => {
    if (!fallback || !fallbackText) return;
    fallback.hidden = false;
    fallbackText.value = `To: wooplix15@gmail.com\nSubject: ${enquiry.subject}\n\n${enquiry.body}`;
    fallbackText.focus();
    fallbackText.select();
  };

  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const enquiry = compose();
    status.textContent = 'Opening an email draft. Review the details and send it from your email app.';
    window.location.href = `mailto:wooplix15@gmail.com?subject=${encodeURIComponent(enquiry.subject)}&body=${encodeURIComponent(enquiry.body)}`;
    window.setTimeout(() => showFallback(enquiry), 700);
  });

  document.querySelector('#copy-enquiry')?.addEventListener('click', async () => {
    if (!form.reportValidity()) return;
    const enquiry = compose();
    const text = `To: wooplix15@gmail.com\nSubject: ${enquiry.subject}\n\n${enquiry.body}`;
    try {
      await navigator.clipboard.writeText(text);
      status.textContent = 'Enquiry copied. Paste it into an email to wooplix15@gmail.com. It has not been sent.';
    } catch {
      showFallback(enquiry);
      status.textContent = 'Copy is unavailable here. The enquiry text is ready below to select manually.';
    }
  });
})();
