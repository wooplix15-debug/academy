import { useEffect, useState } from 'react';

function Arrow({ down = false }) {
  return <span aria-hidden="true" className={`inline-grid size-9 shrink-0 place-items-center rounded-full border border-current/20 ${down ? 'rotate-90' : ''}`}><svg viewBox="0 0 20 20" className="size-4" fill="none"><path d="M3.5 10h12m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" /></svg></span>;
}

function Eyebrow({ children, light = false }) {
  return <p className={`text-[0.65rem] font-bold uppercase tracking-[0.2em] ${light ? 'text-copper' : 'text-ink/50'}`}>{children}</p>;
}

function PageHero({ eyebrow, title, intro, action, sideTitle, sideText, sideIcon }) {
  return (
    <section className="brand-hero mx-auto grid max-w-7xl gap-8 px-5 pb-16 pt-16 sm:px-8 sm:pb-20 sm:pt-20 lg:grid-cols-[1.35fr_0.65fr] lg:items-start lg:gap-20 lg:px-12">
      <div data-reveal>
        <Eyebrow>{eyebrow}</Eyebrow>
        <h1 className="font-display mt-5 max-w-3xl text-4xl font-semibold leading-[1.08] tracking-[-0.045em] text-forest sm:text-5xl lg:text-[4rem]">{title}</h1>
        <p className="mt-6 max-w-2xl text-base leading-relaxed text-ink/65 sm:text-lg">{intro}</p>
        {action && <a className="group mt-7 inline-flex items-center gap-3 rounded-full bg-forest py-2 pl-5 pr-2 text-sm font-semibold text-white transition hover:bg-[#244637]" href={action.href}>{action.label}<span className="rounded-full bg-copper text-forest"><Arrow /></span></a>}
      </div>
      {sideTitle && <aside data-reveal className="rounded-2xl border border-ink/10 bg-[#ecfaf6] p-6 sm:p-8"><span className="mb-6 grid size-12 place-items-center rounded-full bg-white text-xl text-forest" aria-hidden="true">{sideIcon}</span><h2 className="font-display text-xl font-semibold tracking-tight text-forest">{sideTitle}</h2><p className="mt-3 text-sm leading-relaxed text-ink/65">{sideText}</p></aside>}
    </section>
  );
}

function BrandSection({ title, intro, children, dark = false, id }) {
  return (
    <section id={id} className={`brand-section border-t ${dark ? 'border-white/10 bg-forest text-white' : 'border-ink/10'} `}>
      <div className="mx-auto max-w-7xl px-5 py-14 sm:px-8 sm:py-20 lg:px-12">
        <header data-reveal className="mb-8 max-w-3xl sm:mb-11"><h2 className={`font-display text-2xl font-semibold leading-tight tracking-[-0.035em] sm:text-3xl lg:text-4xl ${dark ? 'text-white' : 'text-forest'}`}>{title}</h2>{intro && <p className={`mt-4 max-w-2xl text-sm leading-relaxed sm:text-base ${dark ? 'text-white/60' : 'text-ink/60'}`}>{intro}</p>}</header>
        {children}
      </div>
    </section>
  );
}

function CardGrid({ items, dark = false, columns = 3 }) {
  return <div className={`grid gap-3 sm:gap-4 ${columns === 2 ? 'md:grid-cols-2' : 'md:grid-cols-3'}`}>
    {items.map(([title, text], index) => <article key={title} data-reveal className={`brand-card rounded-2xl border p-6 transition duration-300 hover:-translate-y-1 sm:p-7 ${dark ? 'border-white/10 bg-white/[0.04] hover:border-copper/40' : 'border-ink/10 bg-white hover:border-copper/40 hover:shadow-[0_20px_60px_-35px_rgba(23,45,34,0.35)]'}`}>
      <span className={`font-display text-xs font-semibold ${dark ? 'text-copper' : 'text-copper'}`}>{String(index + 1).padStart(2, '0')}</span>
      <h3 className={`font-display mt-7 text-lg font-semibold leading-snug ${dark ? 'text-white' : 'text-forest'}`}>{title}</h3>
      <p className={`mt-3 text-sm leading-relaxed ${dark ? 'text-white/60' : 'text-ink/65'}`}>{text}</p>
    </article>)}
  </div>;
}

function StepList({ items, dark = false }) {
  return <ol className={`max-w-4xl divide-y ${dark ? 'divide-white/15' : 'divide-ink/10'}`}>
    {items.map((text, index) => <li key={text} data-reveal className="flex gap-4 py-5 sm:gap-6"><span className={`grid size-9 shrink-0 place-items-center rounded-full border text-xs ${dark ? 'border-white/20 text-copper' : 'border-ink/15 text-copper'}`}>{String(index + 1).padStart(2, '0')}</span><p className={`pt-1 text-sm leading-relaxed sm:text-base ${dark ? 'text-white/70' : 'text-ink/70'}`}>{text}</p></li>)}
  </ol>;
}

export function ConsultingPage() {
  const focusAreas = [
    ['Choosing an AI opportunity', 'Review repetitive work, information gaps and slow decisions. Compare AI with simpler alternatives and identify a problem worth addressing.'],
    ['Planning implementation', 'Assess the available data, existing systems, permissions and team skills. Define a pilot with a clear boundary and a way to measure its usefulness.'],
    ['Preparing the team', 'Identify where people need to review outputs, approve actions and handle exceptions. Plan training, ownership and support alongside the technology.'],
  ];
  const industries = [
    ['Manufacturing', 'Finding approved operating information, handling incoming documents and supporting production or maintenance enquiries.'],
    ['Software development', 'Organising requirements, preparing development and test inputs, maintaining documentation and reviewing agent-assisted work.'],
    ['Sports and apparel', 'Answering product enquiries, preparing customer responses and improving document or order-related workflows.'],
  ];
  const steps = [
    'Understand the process. Walk through the current work, the people involved and the problem that needs attention.',
    'Compare possible approaches. Consider existing tools, rules, automation and AI, including the dependencies and limitations of each option.',
    'Define a pilot. Agree its scope, required access, measures, human review and the conditions for continuing or stopping.',
    'Plan the next stage. Identify implementation work, responsibilities, training and support. A larger engagement has its own agreed scope and deliverables.',
  ];
  return <>
    <PageHero eyebrow="AI CONSULTING" title="Decide where AI belongs in your business." intro="Bring a process, a recurring problem or an implementation idea. We will examine the current work, compare the options and identify a practical first step." action={{ href: '#sessions', label: 'Choose a consulting session' }} sideTitle="For leaders and delivery teams" sideText="A useful starting point is one business question: which task needs to improve, who owns it and how will you know that the change helped?" sideIcon="✳" />
    <BrandSection title="What we can work on"><CardGrid items={focusAreas} /></BrandSection>
    <BrandSection title="How a consulting engagement works" dark><StepList items={steps} dark /></BrandSection>
    <BrandSection title="Example discussion areas" intro="These examples help frame a first conversation. The approach depends on the actual process, data and access available in your organisation."><CardGrid items={industries} /></BrandSection>
    <BrandSection title="What to bring to the first conversation"><p data-reveal className="max-w-3xl text-sm leading-relaxed text-ink/65 sm:text-base">Share a short description of your business, the process you want to improve, the systems involved and the decision you need help making. Include your time zone and any important deadline. A brief example is useful; confidential client documents are not needed for the initial enquiry.</p></BrandSection>
    <BrandSection id="sessions" title="Bring one question. Find the next step." intro="Choose the conversation that fits your need. Send the context first so the discussion can focus on your business.">
      <div className="grid gap-4 md:grid-cols-2">
        {[
          ['FOCUSED DISCUSSION', '30', 'Explore one AI opportunity, a specific decision or the best starting point for your team.', ['Your business question', 'Key constraints and dependencies', 'A recommended next step']],
          ['DEEPER WORKING DISCUSSION', '60', 'Work through a process or implementation idea with more time for the options, risks and pilot scope.', ['Current process and pain points', 'Possible approach and controls', 'Priorities for a pilot or roadmap']],
        ].map(([label, duration, text, bullets]) => <article key={duration} data-reveal className="flex flex-col rounded-2xl border border-ink/10 border-t-4 border-t-copper bg-white p-6 sm:p-8">
          <p className="text-[0.65rem] font-bold tracking-[0.16em] text-copper">{label}</p><h3 className="font-display mt-5 text-4xl font-semibold text-forest">{duration}<span className="ml-2 text-base font-normal text-ink/50">minutes</span></h3><p className="mt-4 text-sm leading-relaxed text-ink/65">{text}</p><ul className="my-5 space-y-2 border-t border-ink/10 pt-5 text-sm text-ink/65">{bullets.map(item => <li key={item}>•&nbsp; {item}</li>)}</ul>
          <a className="group mt-auto inline-flex items-center justify-between gap-3 rounded-full bg-forest py-2 pl-5 pr-2 text-sm font-semibold text-white" href={`/contact?topic=AI%20consulting&duration=${duration}`}>Request a {duration}-minute session <span className="rounded-full bg-copper text-forest"><Arrow /></span></a>
        </article>)}
      </div>
      <p className="mt-5 text-xs text-ink/55">These are session requests. Timing, scope and fees are agreed before a session is confirmed.</p>
    </BrandSection>
  </>;
}

export function SpeakingPage() {
  const topics = [
    ['AI for business leaders', 'Where AI can support business work, how to compare opportunities and what to ask before investing in a pilot.'],
    ['From workflows to agents', 'How an AI agent uses information and tools, where a fixed workflow is more suitable and why permissions and human review matter.'],
    ['Building with AI', 'Foundations for students and technical teams, with examples of knowledge assistants, structured outputs and the checks needed before release.'],
  ];
  const formats = [
    ['Talk and discussion', 'Introduce a topic, work through relevant examples and leave time for questions. Suitable when the audience needs a shared understanding.'],
    ['Technical session', 'Examine a system design or implementation example in more detail. Agree the audience’s technical background before choosing the scope.'],
    ['Practical workshop', 'Work on an exercise or a business opportunity with participants. Agree the tools, access, group size and expected outputs in advance.'],
  ];
  const eventDetails = [
    'The organisation, event purpose and audience, including their experience with AI.',
    'The date, location or online format, time zone and expected audience size.',
    'The preferred topic, session format and the question or skill the audience should take away.',
    'Any practical constraints, including tools, internet access and requirements for a demonstration.',
  ];
  return <>
    <PageHero eyebrow="AI SPEAKING AND WORKSHOPS" title="Help your audience understand AI they can use." intro="Practical talks and workshops for conferences, universities, colleges and corporate teams. The session is shaped around what your audience needs to understand or decide." action={{ href: '/contact?topic=Speaking', label: 'Discuss your event' }} sideTitle="A session with a clear purpose" sideText="Start with the audience, their experience and the question you want them to leave able to answer. Examples and technical depth should serve that purpose." sideIcon="◉" />
    <section className="border-t border-ink/10"><div className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 sm:py-20 md:grid-cols-[0.75fr_1.25fr] md:items-center md:gap-16 lg:px-12">
      <figure data-reveal className="relative m-0 overflow-hidden rounded-2xl bg-[#ecfaf6]"><img className="mx-auto max-h-[680px] w-full object-contain" src="/assets/personal-brand/vivek-zoholics-2026.webp" width="944" height="1666" alt="Vivek Pandey at the Zoholics India 2026 event" loading="lazy" /><figcaption className="absolute bottom-3 right-3 rounded-full bg-forest/90 px-4 py-2 text-xs text-white">Zoholics India 2026</figcaption></figure>
      <div data-reveal><Eyebrow>INDUSTRY EVENT</Eyebrow><h2 className="font-display mt-5 max-w-xl text-3xl font-semibold leading-tight tracking-[-0.04em] text-forest sm:text-4xl lg:text-5xl">Ideas are better when they meet real work.</h2><p className="mt-5 max-w-lg text-sm leading-relaxed text-ink/65 sm:text-base">A moment from Zoholics India 2026, where people working with business technology came together to learn, share and connect.</p><a className="text-link mt-6" href="#topics">Explore speaking topics <Arrow down /></a></div>
    </div></section>
    <BrandSection id="topics" title="Topics we can shape for your audience"><CardGrid items={topics} /></BrandSection>
    <BrandSection title="Choose the right session format" dark><CardGrid items={formats} dark /></BrandSection>
    <BrandSection title="What makes a session useful"><div data-reveal className="max-w-3xl space-y-4 text-sm leading-relaxed text-ink/65 sm:text-base"><p>The material should explain technical ideas in language the audience understands. A worked example needs to show the original problem, the proposed approach and the checks that determine whether the result is useful.</p><p>Demonstrations depend on the tools and access agreed for the event. Future developments can be discussed as possibilities; predictions and proposed time savings should not be presented as measured results.</p></div></BrandSection>
    <BrandSection title="Information to include in an event enquiry"><StepList items={eventDetails} /><p className="mt-5 text-sm text-ink/60">Availability, topic, scope, fees and arrangements are agreed before the event is confirmed.</p><a className="group mt-7 inline-flex items-center gap-3 rounded-full bg-forest py-2 pl-5 pr-2 text-sm font-semibold text-white" href="/contact?topic=Speaking">Discuss your event <span className="rounded-full bg-copper text-forest"><Arrow /></span></a></BrandSection>
  </>;
}

export function ContactPage() {
  const [topic, setTopic] = useState('');
  const [status, setStatus] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const aliases = new Map([
      ['AI consulting', 'AI consulting'], ['Speaking enquiry', 'Speaking'], ['Speaking', 'Speaking'],
      ['Course enquiry', 'Academy'], ['Academy', 'Academy'], ['General enquiry', 'Other'], ['Other', 'Other'],
    ]);
    setTopic(aliases.get(params.get('topic') || params.get('service')) || '');
  }, []);

  function submitEnquiry(event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const params = new URLSearchParams(window.location.search);
    const duration = ['30', '60'].includes(params.get('duration')) ? params.get('duration') : '';
    const subject = `Vivek Pandey — ${data.get('topic')}`;
    const body = [
      `Name: ${data.get('name')}`,
      `Phone: ${data.get('phone')}`,
      `Email: ${data.get('email')}`,
      `Topic: ${data.get('topic')}`,
      ...(duration ? [`Requested session: ${duration} minutes`] : []),
    ].join('\n');
    setStatus('Your email app should open with this enquiry. Review it and press Send.');
    window.location.href = `mailto:wooplix15@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  return <>
    <section className="brand-hero mx-auto max-w-7xl px-5 pb-10 pt-16 sm:px-8 sm:pb-12 sm:pt-20 lg:px-12">
      <div data-reveal><Eyebrow>CONTACT</Eyebrow><h1 className="font-display mt-5 text-4xl font-semibold tracking-[-0.045em] text-forest sm:text-5xl lg:text-6xl">Start a conversation.</h1><p className="mt-5 text-base text-ink/60 sm:text-lg">Share your details and choose a topic.</p></div>
    </section>
    <section className="border-t border-ink/10"><div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14 lg:px-12">
      <form data-reveal onSubmit={submitEnquiry} className="grid max-w-3xl gap-5 sm:grid-cols-2 sm:gap-6">
        <label className="text-xs font-semibold text-forest">Name<input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="name" autoComplete="name" maxLength="100" required /></label>
        <label className="text-xs font-semibold text-forest">Phone number<input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="phone" type="tel" autoComplete="tel" maxLength="40" required /></label>
        <label className="text-xs font-semibold text-forest">Email<input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="email" type="email" autoComplete="email" maxLength="200" required /></label>
        <label className="text-xs font-semibold text-forest">Topic<select className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="topic" value={topic} onChange={event => setTopic(event.target.value)} required><option value="" disabled>Choose a topic</option><option>AI consulting</option><option>Speaking</option><option>Academy</option><option>Other</option></select></label>
        <button className="group inline-flex min-h-12 items-center justify-between gap-4 rounded-full bg-forest py-1.5 pl-5 pr-2 text-sm font-semibold text-white transition hover:bg-[#244637] sm:col-span-2 sm:w-fit" type="submit">Continue by email <span className="rounded-full bg-copper text-forest"><Arrow /></span></button>
        <p className="text-xs leading-relaxed text-ink/55 sm:col-span-2">This opens a draft in your email app. Review it and press Send; this website does not store your details. If no email app opens, write to <a className="font-semibold text-forest underline underline-offset-2" href="mailto:wooplix15@gmail.com">wooplix15@gmail.com</a>.</p>
        <p className="text-xs text-forest sm:col-span-2" role="status" aria-live="polite">{status}</p>
      </form>
    </div></section>
  </>;
}
