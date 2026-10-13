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
  const onHome = currentPath === '/';
  const links = [
    ['Home', '/'],
    ['Consulting', '/ai-consulting'],
    ['Speaking', '/ai-speaking'],
    ['Academy', '/academy'],
  ];

  return (
    <header className={`inset-x-0 top-0 z-30 border-b ${onHome ? 'absolute border-white/15 text-white' : 'sticky border-ink/10 bg-ivory/95 text-forest backdrop-blur-md'}`}>
      <div className={`mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8 lg:px-12 ${!onHome ? 'text-forest' : ''}`}>
        <Wordmark dark={!onHome} />
        <button
          type="button"
          className={`flex size-11 flex-col items-center justify-center gap-1.5 rounded-full border md:hidden ${onHome ? 'border-white/30' : 'border-forest/25'}`}
          aria-label={open ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={open}
          aria-controls="main-navigation"
          onClick={() => setOpen(value => !value)}
        >
          <span className={`h-px w-4 ${onHome ? 'bg-white' : 'bg-forest'}`} />
          <span className={`h-px w-4 ${onHome ? 'bg-white' : 'bg-forest'}`} />
        </button>
        <nav id="main-navigation" className={`${open ? 'flex' : 'hidden'} absolute left-4 right-4 top-[calc(100%+0.5rem)] flex-col gap-1 rounded-2xl border border-white/15 bg-forest/95 p-3 text-white shadow-2xl backdrop-blur-lg md:static md:flex md:flex-row md:items-center md:gap-7 md:border-0 md:bg-transparent md:p-0 md:shadow-none ${!onHome ? 'md:text-forest' : ''}`} aria-label="Main navigation">
          {links.map(([label, href]) => (
            <a key={label} className={`rounded-xl px-3 py-3 text-sm font-medium transition hover:text-copper md:px-0 md:py-2 ${href === currentPath ? 'text-copper' : onHome ? 'text-white/80' : 'text-forest/75'}`} href={href} aria-current={href === currentPath ? 'page' : undefined} onClick={() => setOpen(false)}>{label}</a>
          ))}
          <a aria-current={currentPath === '/contact' ? 'page' : undefined} className={`group mt-1 inline-flex items-center justify-between gap-3 rounded-full border py-1 pl-5 pr-1 text-sm font-semibold transition hover:bg-forest hover:text-white md:ml-1 md:mt-0 ${onHome ? 'border-white/50' : 'border-forest/25'}`} href="/contact" onClick={() => setOpen(false)}>
            Contact <span className="grid size-9 place-items-center rounded-full bg-copper text-forest transition group-hover:bg-forest group-hover:text-white"><DirectionMark /></span>
          </a>
        </nav>
      </div>
    </header>
  );
}

function useScrollReveals() {
  useEffect(() => {
    const targets = document.querySelectorAll('[data-reveal]');
    if (!targets.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

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
      document.documentElement.classList.remove('motion-ready');
    };
  }, []);
}

function Hero() {
  return (
    <section id="top" className="relative isolate flex min-h-[720px] items-end overflow-hidden bg-forest text-white sm:min-h-[780px] lg:min-h-[min(900px,100svh)]" aria-label="Vivek Pandey introduction">
      <img className="hero-image absolute inset-0 -z-20 h-full w-full object-cover object-[58%_36%] sm:object-[60%_35%]" src="/assets/personal-brand/vivek-office-02.jpg" width="2400" height="1350" alt="Vivek Pandey in his office" fetchPriority="high" />
      <div className="absolute inset-0 -z-10 bg-gradient-to-r from-[#071610]/90 via-[#071610]/55 to-[#071610]/5" />
      <div className="absolute inset-0 -z-10 bg-gradient-to-t from-[#071610]/65 via-transparent to-[#071610]/20" />
      <div className="absolute -left-36 top-1/3 -z-10 size-[34rem] rounded-full border border-white/10" />
      <div className="mx-auto w-full max-w-7xl px-5 pb-12 pt-36 sm:px-8 sm:pb-16 lg:px-12 lg:pb-[4.5rem]">
        <div className="max-w-2xl animate-rise">
          <p className="mb-5 text-[0.68rem] font-bold uppercase tracking-[0.24em] text-white/75">AI CONSULTING · SPEAKING · EDUCATION</p>
          <h1 className="font-display max-w-xl text-4xl font-semibold leading-[1.08] tracking-[-0.045em] sm:text-5xl lg:text-[4.25rem]">Practical AI for business, <span className="font-serif font-normal italic text-copper">grounded in experience.</span></h1>
          <div className="mt-8 flex flex-wrap items-center gap-x-7 gap-y-4">
            <a className="group inline-flex items-center gap-4 rounded-full bg-ivory py-2 pl-6 pr-2 text-sm font-bold text-forest transition hover:bg-white" href="#work">Explore my work <span className="transition group-hover:translate-x-1"><DirectionMark /></span></a>
            <a className="inline-flex items-center gap-3 border-b border-white/50 pb-1 text-sm font-semibold text-white transition hover:border-copper hover:text-copper" href="#journey">Career journey <DirectionMark down /></a>
          </div>
        </div>
        <div className="mt-20 flex items-center gap-4 text-[0.6rem] font-bold uppercase tracking-[0.18em] text-white/75 sm:mt-28">
          <span>Based in India</span><span className="h-px w-8 bg-white/40" /><span>Working internationally</span>
        </div>
      </div>
      <div className="pointer-events-none absolute bottom-0 right-0 -z-10 h-1/2 w-1/3 bg-gradient-to-tl from-copper/10 to-transparent" />
    </section>
  );
}

function Experience() {
  return (
    <>
      <section className="mx-auto grid max-w-7xl gap-8 px-5 py-20 sm:px-8 sm:py-28 lg:grid-cols-[1.1fr_0.9fr] lg:gap-20 lg:px-12">
        <div>
          <p className="eyebrow">EXPERIENCE</p>
          <h2 className="section-title mt-5">Business first.<br /><span className="font-serif font-normal italic text-copper">Technology with purpose.</span></h2>
        </div>
        <div className="flex flex-col items-start justify-end">
          <p className="max-w-xl text-lg leading-relaxed text-ink/70">Software, business systems and automation shaped by practical delivery. Today, I help teams make clear decisions about AI.</p>
          <a className="text-link mt-7" href="/ai-consulting">How I can help <DirectionMark /></a>
        </div>
      </section>
      <section className="border-y border-ink/10 bg-[#f0eee7]" aria-label="Experience in numbers">
        <div className="mx-auto grid max-w-7xl grid-cols-2 gap-6 px-5 py-9 sm:px-8 md:grid-cols-4 md:py-12 lg:px-12">
          {[["19", "years in technology"], ["995+", "Wooplix projects"], ["75+", "countries reached by Wooplix"], ["35+", "Zoho apps"]].map(([value, label]) => (
            <div key={label} className="border-l border-ink/15 pl-4 sm:pl-6"><strong className="font-display block text-3xl font-semibold tracking-tight text-forest sm:text-4xl">{value}</strong><span className="mt-1 block text-xs leading-relaxed text-ink/60 sm:text-sm">{label}</span></div>
          ))}
        </div>
      </section>
    </>
  );
}

function Services() {
  return (
    <section id="work" className="mx-auto max-w-7xl scroll-mt-16 px-5 py-20 sm:px-8 sm:py-28 lg:px-12">
      <div className="mb-10 grid gap-5 md:grid-cols-[1fr_0.55fr] md:items-end lg:mb-14">
        <div><p className="eyebrow">WORK WITH ME</p><h2 className="section-title mt-5">Three ways to<br /><span className="font-serif font-normal italic text-copper">move forward.</span></h2></div>
        <p className="max-w-sm text-sm leading-relaxed text-ink/60 md:justify-self-end">For organisations, events and teams building their AI capability.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {services.map(service => (
          <article key={service.number} data-reveal className="reveal group flex min-h-[310px] flex-col rounded-2xl border border-ink/10 bg-white p-6 transition duration-300 hover:-translate-y-1 hover:border-copper/40 hover:shadow-[0_20px_60px_-35px_rgba(23,45,34,0.35)] sm:p-8">
            <div className="flex items-start justify-between"><span className="text-[0.65rem] font-bold tracking-[0.18em] text-ink/45">{service.number} / {service.label}</span><span className="grid size-12 place-items-center rounded-full bg-[#f0eee7] text-xl text-forest transition group-hover:bg-forest group-hover:text-copper">{service.icon}</span></div>
            <h3 className="font-display mt-10 text-2xl font-semibold tracking-tight text-forest">{service.title}</h3>
            <p className="mt-3 max-w-sm text-sm leading-relaxed text-ink/65">{service.description}</p>
            <a className="text-link mt-auto pt-7" href={service.href}>Explore {service.title === 'Academy' ? 'the Academy' : service.title.toLowerCase()} <DirectionMark /></a>
          </article>
        ))}
      </div>
    </section>
  );
}

function Journey() {
  return (
    <section id="journey" className="scroll-mt-12 bg-forest py-20 text-white sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8 lg:px-12">
        <div className="mb-12 grid gap-5 md:grid-cols-[1fr_0.55fr] md:items-end lg:mb-16">
          <div><p className="eyebrow text-copper">THE JOURNEY</p><h2 className="section-title mt-5 text-white">From software<br /><span className="font-serif font-normal italic text-copper">to applied AI.</span></h2></div>
          <p className="max-w-sm text-sm leading-relaxed text-white/60 md:justify-self-end">A short view of the work and how it has evolved.</p>
        </div>
        <ol data-reveal className="journey-list relative ml-2 sm:ml-4">
          {milestones.map(([year, title, description], index) => (
            <li key={year} data-reveal className="reveal relative grid gap-2 pb-9 pl-7 last:pb-0 sm:grid-cols-[6rem_1fr] sm:gap-7 sm:pl-10">
              <span className={`absolute -left-[5px] top-1 size-[9px] rounded-full ${index === milestones.length - 1 ? 'bg-copper ring-4 ring-copper/20' : 'bg-white/60'}`} />
              <span className="font-display text-lg font-semibold text-copper">{year}</span>
              <div><h3 className="font-display text-lg font-semibold">{title}</h3><p className="mt-1 max-w-2xl text-sm leading-relaxed text-white/60">{description}</p></div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

function SelectedWork() {
  return (
    <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-28 lg:px-12">
      <div className="mb-10 grid gap-5 md:grid-cols-[1fr_0.55fr] md:items-end lg:mb-14">
        <div><p className="eyebrow">SELECTED COMPANY WORK</p><h2 className="section-title mt-5">Projects across<br /><span className="font-serif font-normal italic text-copper">different industries.</span></h2></div>
        <p className="max-w-sm text-sm leading-relaxed text-ink/60 md:justify-self-end">Selected examples from Wooplix Technologies’ public portfolio.</p>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {projects.map(([category, title, description], i) => (
          <article key={title} data-reveal className="reveal min-h-52 rounded-2xl border border-ink/10 bg-white p-6 transition hover:border-forest/35 hover:bg-[#f7f5ef] sm:p-7">
            <span className="text-[0.6rem] font-bold leading-relaxed tracking-[0.13em] text-ink/45">{category}</span>
            <div className="mt-9 flex items-end justify-between gap-2"><h3 className="font-display text-lg font-semibold leading-tight text-forest">{title}</h3><span className="font-display text-xs font-semibold text-copper">0{i + 1}</span></div>
            <p className="mt-2 text-sm leading-relaxed text-ink/60">{description}</p>
          </article>
        ))}
      </div>
      <div className="mt-6 flex items-center gap-4 rounded-xl bg-[#f0eee7] p-4 sm:px-6">
        <img className="h-8 w-auto max-w-full object-contain object-left" src="/assets/wooplix-partner-badge.png" alt="Wooplix Technologies, Zoho Authorized Partner and NASSCOM Member" loading="lazy" />
        <p className="ml-auto hidden text-xs text-ink/55 sm:block">Wooplix Technologies</p>
      </div>
    </section>
  );
}

function CallToAction() {
  return (
    <section className="mx-auto max-w-7xl px-5 pb-20 sm:px-8 sm:pb-28 lg:px-12">
      <div className="grid gap-8 rounded-[1.75rem] bg-[#e8e5db] p-7 sm:p-10 md:grid-cols-[1fr_auto] md:items-end lg:p-14">
        <div><p className="eyebrow">LET’S TALK</p><h2 className="section-title mt-5">Bring a question.<br /><span className="font-serif font-normal italic text-copper">Leave with a next step.</span></h2><p className="mt-4 text-sm text-ink/60">Choose a 30-minute introduction or a 60-minute working session.</p></div>
        <div className="flex flex-wrap gap-3 md:flex-col lg:flex-row">
          <a className="inline-flex min-h-12 items-center justify-center gap-3 rounded-full bg-forest py-2 pl-5 pr-2 text-sm font-semibold text-white transition hover:bg-[#244637]" href="/contact?topic=AI%20consulting&duration=30">Request 30 minutes <span className="grid size-9 place-items-center rounded-full bg-copper text-forest"><DirectionMark /></span></a>
          <a className="inline-flex min-h-12 items-center justify-center gap-3 rounded-full border border-forest/30 py-2 pl-5 pr-2 text-sm font-semibold text-forest transition hover:bg-white" href="/contact?topic=AI%20consulting&duration=60">Request 60 minutes <span className="grid size-9 place-items-center rounded-full bg-white text-forest"><DirectionMark /></span></a>
        </div>
      </div>
    </section>
  );
}

function Footer() {
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
        : <><Hero /><Experience /><Services /><Journey /><SelectedWork /><CallToAction /></>;

  return (
    <div className="min-h-screen bg-ivory text-ink antialiased">
      <a className="skip-link" href="#main">Skip to content</a>
      <Header currentPath={currentPath} />
      <main id="main">{content}</main>
      <Footer />
    </div>
  );
}
