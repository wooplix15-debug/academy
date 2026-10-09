const brandMenu = document.querySelector('.nav-toggle');
const brandNav = document.querySelector('#brand-nav');
function closeBrandMenu() {
  brandNav?.classList.remove('is-open');
  brandMenu?.setAttribute('aria-expanded', 'false');
  brandMenu?.setAttribute('aria-label', 'Open menu');
}
brandMenu?.addEventListener('click', () => {
  const open = brandMenu.getAttribute('aria-expanded') !== 'true';
  brandNav?.classList.toggle('is-open', open);
  brandMenu.setAttribute('aria-expanded', String(open));
  brandMenu.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
});
brandNav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeBrandMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeBrandMenu(); });
document.querySelectorAll('[data-brand-year]').forEach(label => { label.textContent = new Date().getFullYear(); });

const homeHeader = document.querySelector('.home-header');
const homeHero = document.querySelector('.portrait-hero');
const homeProgress = document.querySelector('.home-progress span');
let homeScrollFrame = 0;
const updateHomeChrome = () => {
  homeScrollFrame = 0;
  const y = window.scrollY;
  const threshold = homeHero ? Math.max(160, homeHero.offsetHeight - 90) : 160;
  homeHeader?.classList.toggle('is-past-hero', y > threshold);
  if (homeProgress) {
    const range = document.documentElement.scrollHeight - window.innerHeight;
    homeProgress.style.transform = `scaleX(${range > 0 ? Math.max(0, Math.min(1, y / range)) : 0})`;
  }
};
window.addEventListener('scroll', () => {
  if (homeScrollFrame) return;
  homeScrollFrame = window.requestAnimationFrame(updateHomeChrome);
}, { passive: true });
window.addEventListener('resize', updateHomeChrome, { passive: true });
updateHomeChrome();

const homeMotionItems = document.querySelectorAll('.home-intro,.career-heading,.career-timeline li,.home-section-head,.home-service-list>a,.affiliation-card,.home-proof,.home-session-options>a');
if (homeMotionItems.length && 'IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('motion-ready');
  const homeObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    homeObserver.unobserve(entry.target);
  }), { rootMargin: '0px 0px -7% 0px', threshold: 0.08 });
  homeMotionItems.forEach(item => homeObserver.observe(item));
}

const portraitSlides = [...document.querySelectorAll('[data-portrait-slide]')];
const portraitDots = [...document.querySelectorAll('[data-portrait-dot]')];
const portraitCurrent = document.querySelector('[data-portrait-current]');
const portraitPause = document.querySelector('[data-portrait-pause]');
const portraitHero = document.querySelector('.portrait-hero');
if (portraitSlides.length) {
  let portraitIndex = 0;
  let portraitTimer;
  let portraitPaused = false;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const showPortrait = index => {
    portraitIndex = (index + portraitSlides.length) % portraitSlides.length;
    portraitSlides.forEach((slide, slideIndex) => {
      const active = slideIndex === portraitIndex;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
    });
    portraitDots.forEach((dot, dotIndex) => {
      const active = dotIndex === portraitIndex;
      dot.classList.toggle('is-active', active);
      if (active) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });
    if (portraitCurrent) portraitCurrent.textContent = String(portraitIndex + 1).padStart(2, '0');
  };
  const stopPortraits = () => {
    window.clearInterval(portraitTimer);
    portraitTimer = undefined;
  };
  const startPortraits = () => {
    stopPortraits();
    if (!portraitPaused && !reduceMotion) portraitTimer = window.setInterval(() => showPortrait(portraitIndex + 1), 6500);
  };
  portraitDots.forEach((dot, index) => dot.addEventListener('click', () => {
    showPortrait(index);
    startPortraits();
  }));
  portraitPause?.addEventListener('click', () => {
    portraitPaused = !portraitPaused;
    portraitPause.setAttribute('aria-pressed', String(portraitPaused));
    portraitPause.textContent = portraitPaused ? 'Play' : 'Pause';
    if (portraitPaused) stopPortraits();
    else startPortraits();
  });
  portraitHero?.addEventListener('mouseenter', stopPortraits);
  portraitHero?.addEventListener('mouseleave', startPortraits);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopPortraits();
    else startPortraits();
  });
  showPortrait(0);
  startPortraits();
}

const enquiryForm = document.querySelector('#enquiry-form');
if (enquiryForm) {
  const parameters = new URLSearchParams(window.location.search);
  const topicAliases = {
    'AI consulting': 'AI consulting',
    'Speaking enquiry': 'Speaking',
    'Speaking': 'Speaking',
    'Course enquiry': 'Academy',
    'Academy': 'Academy',
    'General enquiry': 'Other',
    'Other': 'Other'
  };
  const requestedTopic = parameters.get('topic') || parameters.get('service');
  if (topicAliases[requestedTopic]) enquiryForm.elements.topic.value = topicAliases[requestedTopic];
  const status = document.querySelector('#enquiry-status');
  enquiryForm.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(enquiryForm);
    const duration = ['30', '60'].includes(parameters.get('duration')) ? parameters.get('duration') : '';
    const subject = `Vivek Pandey — ${data.get('topic')}`;
    const body = [
      `Name: ${data.get('name')}`,
      `Phone: ${data.get('phone')}`,
      `Email: ${data.get('email')}`,
      `Topic: ${data.get('topic')}`,
      ...(duration ? [`Requested session: ${duration} minutes`] : [])
    ].join('\n');
    window.location.href = `mailto:wooplix15@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    status.textContent = 'Your email app should open with this enquiry. Review it and press Send.';
  });
}
