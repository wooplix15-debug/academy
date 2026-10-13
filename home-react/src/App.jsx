import { useEffect, useState } from 'react';
import { ConsultingPage, ContactPage, SpeakingPage } from './BrandPages.jsx';

const services = [
  {
    number: '01',
    label: 'STRATEGY',
    title: 'AI Consulting',
    description: 'Find useful opportunities, shape a pilot and plan implementation.',
    href: '/ai-consulting',
    icon: '✳',
  },
  {
    number: '02',
    label: 'SPEAKING',
    title: 'AI Speaking',
    description: 'Practical talks for business leaders, technical teams and students.',
    href: '/ai-speaking',
    icon: '◉',
  },
  {
    number: '03',
    label: 'EDUCATION',
    title: 'Academy',
    description: 'Advanced AI and Zoho courses with practical work and project learning.',
    href: '/academy',
    icon: '▦',
  },
];

const milestones = [
  ['2008', 'Technology foundations', 'Started a career in software and digital work.'],
  ['2013', 'Building for business', 'Worked across software, requirements and delivery.'],
  ['2018', 'Systems & automation', 'Focused on business processes and connected applications.'],
  ['2023', 'Zoho & implementation', 'Led business system projects and shared experience at Zoholics India.'],
  ['2026', 'Applied AI', 'Bringing consulting, speaking and practical education together.'],
];

const projects = [
  ['EDUCATION · DIGITAL MARKETING', 'ABTI Learning', 'Digital learning and growth.'],
  ['TRAINING · ZOHO CRM', 'MindCypress', 'Zoho CRM for an upskilling platform.'],
  ['ENTERPRISE IT · INTEGRATION', 'Datasource Technology', 'Enterprise and healthcare solutions.'],
  ['E-COMMERCE · WEB DESIGN', 'Christian Chapman Art', 'A portfolio and e-commerce platform.'],
];

function DirectionMark({ down = false }) {
  return (
    <span className={`inline-flex size-10 shrink-0 items-center justify-center rounded-full border border-current/20 ${down ? 'rotate-90' : ''}`} aria-hidden="true">
      <svg viewBox="0 0 20 20" className="size-4" fill="none">
        <path d="M3.5 10h12m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </span>
  );
}

function Wordmark({ dark = false }) {
  return (
    <a className={`inline-flex items-center gap-3 ${dark ? 'text-forest' : 'text-white'}`} href="/" aria-label="Vivek Pandey home">
      <span className="font-display text-[2rem] font-extrabold leading-none tracking-[-0.1em]">vp<span className="text-copper">.</span></span>
      <span className="text-sm font-semibold tracking-tight sm:text-base">Vivek Pandey</span>
    </a>
  );
}

function Header({ currentPath = '/' }) {
  const [open, setOpen] = useState(false);
  const links = [['Home', '/'], ['Consulting', '/ai-consulting'], ['Speaking', '/ai-speaking'], ['Academy', '/academy']];
  return <header className="site-header"><div className="home-container header-inner">
    <Wordmark dark />
    <button type="button" className="menu-toggle" aria-label={open ? 'Close navigation menu' : 'Open navigation menu'} aria-expanded={open} aria-controls="main-navigation" onClick={() => setOpen(!open)}><span /><span /></button>
    <nav id="main-navigation" className={`site-nav ${open ? 'is-open' : ''}`} aria-label="Main navigation">
      {links.map(([label, href]) => <a key={href} href={href} aria-current={href === currentPath ? 'page' : undefined} onClick={() => setOpen(false)}>{label}</a>)}
      <a href="/contact" className="nav-contact" onClick={() => setOpen(false)}>Contact <span aria-hidden="true">＋</span></a>
    </nav>
  </div></header>;
}

function useScrollReveals() {
  useEffect(() => {
    const targets = document.querySelectorAll('[data-reveal]');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion) return;

    const portraits = [...document.querySelectorAll('[data-parallax]')];
    const marquees = [...document.querySelectorAll('[data-scroll-marquee]')];
    let frame = 0;
    const paintScroll = () => {
      frame = 0;
      portraits.forEach(image => {
        const bounds = image.parentElement.getBoundingClientRect();
        if (bounds.bottom < 0 || bounds.top > window.innerHeight) return;
        const progress = (window.innerHeight / 2 - bounds.top - bounds.height / 2) / window.innerHeight;
        image.style.setProperty('--portrait-drift', `${Math.max(-45, Math.min(45, progress * (window.innerWidth < 768 ? 40 : 110)))}px`);
        image.closest('.hero-portrait-stack, .event-portrait')?.style.setProperty('--surface-drift', `${Math.max(-45, Math.min(45, progress * (window.innerWidth < 768 ? 40 : 110)))}px`);
      });
      marquees.forEach(element => {
        const bounds = element.getBoundingClientRect();
        const progress = Math.max(0, Math.min(1, (window.innerHeight - bounds.top) / (window.innerHeight + bounds.height)));
        element.style.setProperty('--marquee-shift', `${180 - progress * 360}px`);
        element.style.setProperty('--contact-turn', `${progress * 360}deg`);
      });
      const height = document.documentElement.scrollHeight - window.innerHeight;
      document.documentElement.style.setProperty('--page-progress', String(height > 0 ? window.scrollY / height : 0));
      document.documentElement.style.setProperty('--contact-turn', `${height > 0 ? window.scrollY / height * 360 : 0}deg`);
    };
    const scheduleScroll = () => { if (!frame) frame = requestAnimationFrame(paintScroll); };
    window.addEventListener('scroll', scheduleScroll, { passive: true });
    window.addEventListener('resize', scheduleScroll);
    paintScroll();

    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        currentObserver.unobserve(entry.target);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -48px 0px' });

    document.documentElement.classList.add('motion-ready');
    targets.forEach(target => observer.observe(target));

    return () => {
      observer.disconnect();
      window.removeEventListener('scroll', scheduleScroll);
      window.removeEventListener('resize', scheduleScroll);
      cancelAnimationFrame(frame);
      document.documentElement.classList.remove('motion-ready');
    };
  }, []);
}

function HomeIcon({ type = 'build' }) {
  const paths = {
    analyse: <><path d="M4 4v16h16M8 14l4-5 4 3 4-7" /></>,
    automate: <><circle cx="12" cy="12" r="8" /><path d="M12 4v16M4 12h16M7 6c5 5 5 7 0 12M17 6c-5 5-5 7 0 12" /></>,
    build: <><path d="M4 7l8-4 8 4-8 4-8-4ZM4 12l8 4 8-4M4 17l8 4 8-4" /></>,
    speaking: <><rect x="9" y="3" width="6" height="12" rx="3" /><path d="M6 11v1a6 6 0 0 0 12 0v-1M12 18v3M8 21h8" /></>,
  };
  return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[type] ?? paths.build}</svg>;
}

function Hero() {
  return <section id="top" className="new-hero" aria-label="Vivek Pandey introduction"><div className="home-container hero-grid">
    <div className="hero-copy animate-rise">
      <h1><span className="headline-mask"><span>Practical AI for business,</span></span><span className="headline-mask headline-accent"><span>grounded in experience.</span></span></h1>
      <p>Find useful AI opportunities, improve business processes and build practical skills.</p>
      <div className="home-actions"><a className="home-button primary" href="/ai-consulting">Explore AI consulting <span aria-hidden="true">＋</span></a><a className="home-button secondary" href="/academy">Discover the Academy</a></div>
      <div className="hero-metrics" aria-label="Experience in numbers">{[['19', 'years in technology'], ['995+', 'Wooplix projects'], ['75+', 'countries reached by Wooplix'], ['35+', 'Zoho apps']].map(([value, label]) => <div key={label}><strong>{value}</strong><span>{label}</span></div>)}</div>
    </div>
    <figure className="hero-portrait-stack">
      <div className="hero-portrait-frame"><img data-parallax src="/assets/personal-brand/vivek-office-02.jpg" width="2400" height="1350" alt="Vivek Pandey in his office" fetchPriority="high" /></div>
      <figcaption><strong>Vivek Pandey</strong><span>Business. Technology. People.</span></figcaption>
      <span className="portrait-outline" aria-hidden="true" />
      <a className="portrait-contact" href="/contact" aria-label="Start a conversation with Vivek Pandey"><svg className="contact-ring" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="home-contact-circle" d="M 60,60 m -43,0 a 43,43 0 1,1 86,0 a 43,43 0 1,1 -86,0" /></defs><text><textPath href="#home-contact-circle" textLength="263" lengthAdjust="spacing">LET’S TALK · YOUR NEXT STEP · </textPath></text></svg><span aria-hidden="true">＋</span></a>
    </figure>
  </div></section>;
}

function Experience() {
  return <section className="home-section experience-section"><div className="home-container experience-grid">
    <div data-reveal className="reveal"><p className="home-eyebrow">WHY WORK WITH ME</p><h2 data-reveal className="home-heading title-reveal">Real experience.<br /><span>Practical solutions.</span></h2><p className="home-body">19 years of software, business systems and automation. I help teams turn an idea into a clear plan and a useful solution.</p><a className="home-button secondary" href="#journey">Explore my journey</a></div>
    <ul className="capability-list">{[['analyse', 'AI & automation', 'Strategy and implementation'], ['build', 'Zoho ecosystem', 'Custom solutions and integrations'], ['automate', 'Business processes', 'Connect technology with daily work'], ['speaking', 'Training & enablement', 'Build skills your team can use']].map(([icon, title, detail]) => <li key={title} data-reveal className="reveal"><span><HomeIcon type={icon} /></span><div><h3>{title}</h3><p>{detail}</p></div></li>)}</ul>
    <figure data-reveal className="reveal experience-portrait event-portrait"><img data-parallax src="/assets/personal-brand/vivek-zoholics-2026.webp" width="944" height="1666" alt="Vivek Pandey at Zoholics India 2026" loading="lazy" /><figcaption><strong>Zoholics India 2026</strong><span>Learning and connecting with the technology community.</span></figcaption></figure>
  </div></section>;
}

function Services() {
  return <section id="work" className="home-section services-section"><div className="home-container"><p className="home-eyebrow">HOW I CAN HELP</p><h2 data-reveal className="home-heading title-reveal">Three ways to <span>move forward.</span></h2><div className="service-grid">
    {services.map((service, index) => <article key={service.number} data-reveal className="reveal home-service"><span className="card-number">{service.number}</span><div className="service-icon"><HomeIcon type={['automate', 'speaking', 'build'][index]} /></div><h3>{service.title}</h3><p>{service.description}</p><a href={service.href}>Explore {service.title === 'Academy' ? 'courses' : index === 0 ? 'consulting' : 'speaking'} <span aria-hidden="true">＋</span></a></article>)}
  </div></div></section>;
}

function Journey() {
  return <section id="journey" className="home-section timeline-section"><div className="home-container"><p className="home-eyebrow">MY JOURNEY</p><h2 data-reveal className="home-heading title-reveal">From foundations <span>to applied AI.</span></h2><ol className="home-timeline">{milestones.map(([year, title, description]) => <li key={year} data-reveal className={`reveal ${year === '2026' ? 'current' : ''}`}><i aria-hidden="true" /><strong>{year}</strong><h3>{title}</h3><p>{description}</p></li>)}</ol></div></section>;
}

function SelectedWork() {
  return <section className="home-section projects-section"><div className="home-container"><p className="home-eyebrow">SELECTED COMPANY WORK</p><h2 data-reveal className="home-heading title-reveal">Selected <span>work.</span></h2><p className="project-note">Examples from Wooplix Technologies’ public portfolio.</p><div className="project-grid">{projects.map(([category, title, description], index) => <article key={title} data-reveal className="reveal home-project"><span className="project-index" aria-hidden="true">0{index + 1}</span><div className="project-copy"><span>{category}</span><h3>{title}</h3><p>{description}</p></div></article>)}</div></div></section>;
}

function CallToAction() {
  return <section className="home-cta"><div className="contact-marquee" data-scroll-marquee aria-hidden="true"><div className="contact-marquee-track"><span>Let’s talk.</span><span>Let’s talk.</span><span>Let’s talk.</span></div></div><div className="home-container cta-grid"><div><p className="home-eyebrow">LET’S CONNECT</p><h2 data-reveal className="title-reveal">Bring a question.<br /><span>Leave with a next step.</span></h2><p>Choose an introduction or a working session.</p></div><div className="home-actions"><a className="home-button primary" href="/contact?topic=AI%20consulting&duration=30">Request 30 minutes</a><a className="home-button outline" href="/contact?topic=AI%20consulting&duration=60">Request 60 minutes</a></div></div></section>;
}

function Footer({ compact = false }) {
  if (compact) return <footer className="home-footer"><div className="home-container"><Wordmark /><nav aria-label="Footer navigation"><a href="/">Home</a><a href="/ai-consulting">Consulting</a><a href="/ai-speaking">Speaking</a><a href="/academy">Academy</a><a href="/contact">Contact</a></nav><small>© 2026 Vivek Pandey</small></div></footer>;
  return (
    <footer className="bg-[#0b1711] text-white">
      <div className="mx-auto max-w-7xl px-5 py-12 sm:px-8 lg:px-12">
        <div className="grid gap-10 border-b border-white/15 pb-10 sm:grid-cols-3">
          <div><Wordmark /><p className="mt-4 text-sm leading-relaxed text-white/55">Business understanding.<br />Technology with purpose.</p></div>
          <div><p className="eyebrow text-copper">EXPLORE</p><div className="mt-4 flex flex-col items-start gap-2 text-sm text-white/70"><a className="hover:text-white" href="/ai-consulting">AI Consulting</a><a className="hover:text-white" href="/ai-speaking">AI Speaking</a><a className="hover:text-white" href="/academy">Academy</a></div></div>
          <div><p className="eyebrow text-copper">CONNECT</p><div className="mt-4 flex flex-col items-start gap-2 text-sm text-white/70"><a className="hover:text-white" href="/#journey">The journey</a><a className="hover:text-white" href="/contact">Start a conversation</a><a className="hover:text-white" href="mailto:wooplix15@gmail.com">wooplix15@gmail.com</a></div></div>
        </div>
        <div className="flex flex-col gap-3 pt-5 text-xs text-white/45 sm:flex-row sm:items-center sm:justify-between"><span>© 2026 Vivek Pandey</span><span>For international leaders &amp; teams.</span><a className="inline-flex items-center gap-2 hover:text-white" href="#top">Back to top <DirectionMark /></a></div>
      </div>
    </footer>
  );
}

export default function App({ path: suppliedPath } = {}) {
  useScrollReveals();
  const currentPath = suppliedPath ?? (typeof window !== 'undefined' ? window.location.pathname.replace(/\.html$/, '') : '/');
  const content = currentPath === '/ai-consulting'
    ? <ConsultingPage />
    : currentPath === '/ai-speaking'
      ? <SpeakingPage />
      : currentPath === '/contact'
        ? <ContactPage />
        : <><Hero /><Services /><Experience /><Journey /><SelectedWork /><CallToAction /></>;

  return (
    <div className={`${currentPath === '/' ? 'home-page ' : 'brand-page '}min-h-screen bg-ivory text-ink antialiased`}>
      <a className="skip-link" href="#main">Skip to content</a>
      <Header currentPath={currentPath} />
      <main id="main">{content}</main>
      <Footer compact />
    </div>
  );
}
