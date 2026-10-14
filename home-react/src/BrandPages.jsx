import { useEffect, useState } from 'react';
import { buildEnquiryMailto } from './enquiryEmail.js';

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
    ['Generative AI for knowledge work', 'Find where people spend time searching, drafting, summarising or preparing decisions. Shape a useful assistant around approved information and human review.'],
    ['Agentic AI with guardrails', 'Explore when an agent can use tools and take bounded actions, where a fixed workflow is safer and which permissions, checks and recovery paths are needed.'],
    ['Business automation that fits', 'Connect the process, systems and people before choosing the technology. Define a pilot with a clear boundary, owner and way to review whether it helps.'],
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
    <PageHero eyebrow="AI CONSULTING" title="Turn AI ambition into a practical operating plan." intro="Bring a process, a recurring problem or an implementation idea. We will examine the work, compare Generative AI, Agentic AI and business automation, then identify a responsible first step." action={{ href: '#sessions', label: 'Choose a consulting session' }} sideTitle="For leaders and delivery teams" sideText="Start with one business question: which task needs to improve, who owns it and how will you know that the change helped?" sideIcon="✳" />
    <BrandSection title="Where AI can create useful leverage" intro="The right answer may be a model, an agent, an automation or a simpler change. The work starts with the process and its constraints."><CardGrid items={focusAreas} /></BrandSection>
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
          <a className="group mt-auto inline-flex items-center justify-between gap-3 rounded-full bg-forest py-2 pl-5 pr-2 text-sm font-semibold text-white" href={buildEnquiryMailto({ topic: 'AI consulting', duration })}>Request a {duration}-minute session <span className="rounded-full bg-copper text-forest"><Arrow /></span></a>
        </article>)}
      </div>
      <p className="mt-5 text-xs text-ink/55">These are session requests. Timing, scope and fees are agreed before a session is confirmed.</p>
    </BrandSection>
  </>;
}

export function SpeakingPage() {
  const topics = [
    ['AI that earns its place in the business', 'A clear way for leaders to identify useful opportunities, ask better questions and move from enthusiasm to a sensible pilot.'],
    ['Generative AI, agents and automation', 'Understand the difference between a helpful assistant, a bounded agent and a dependable workflow—and when each approach fits.'],
    ['Building responsibly with AI', 'Practical ideas for technical teams and students, including approved information, structured outputs, human review and recovery paths.'],
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
    <PageHero eyebrow="AI SPEAKING AND WORKSHOPS" title="Make AI clear, useful and actionable for your audience." intro="Practical talks and workshops for conferences, universities, colleges and corporate teams. Each session is shaped around what the audience needs to understand, discuss or decide." action={{ href: '/contact?topic=Speaking#main', label: 'Book Vivek Pandey' }} sideTitle="A session with a clear purpose" sideText="Start with the audience, their experience and the question you want them to leave able to answer. Examples and technical depth should serve that purpose." sideIcon="◉" />
    <section className="border-t border-ink/10"><div className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 sm:py-20 md:grid-cols-[0.75fr_1.25fr] md:items-center md:gap-16 lg:px-12">
      <figure data-reveal className="relative m-0 overflow-hidden rounded-2xl bg-[#ecfaf6]"><img className="mx-auto max-h-[680px] w-full object-contain" src="/assets/personal-brand/life-at-wooplix-06.jpg" width="1200" height="800" alt="Vivek Pandey in conversation at a NASSCOM event" loading="lazy" /><figcaption className="absolute bottom-3 right-3 rounded-full bg-forest/90 px-4 py-2 text-xs text-white">NASSCOM event</figcaption></figure>
      <div data-reveal><Eyebrow>INDUSTRY EVENT</Eyebrow><h2 className="font-display mt-5 max-w-xl text-3xl font-semibold leading-tight tracking-[-0.04em] text-forest sm:text-4xl lg:text-5xl">Ideas are better when they meet real work.</h2><p className="mt-5 max-w-lg text-sm leading-relaxed text-ink/65 sm:text-base">A conversation at a NASSCOM event is a useful reminder: the best sessions connect new technology to the questions people are already asking.</p><a className="text-link mt-6" href="#topics">Explore speaking topics <Arrow down /></a></div>
    </div></section>
    <BrandSection id="topics" title="Topics we can shape for your audience"><CardGrid items={topics} /></BrandSection>
    <BrandSection title="Choose the right session format" dark><CardGrid items={formats} dark /></BrandSection>
    <BrandSection title="What makes a session useful"><div data-reveal className="max-w-3xl space-y-4 text-sm leading-relaxed text-ink/65 sm:text-base"><p>The material should explain technical ideas in language the audience understands. A worked example needs to show the original problem, the proposed approach and the checks that determine whether the result is useful.</p><p>Demonstrations depend on the tools and access agreed for the event. Future developments can be discussed as possibilities; predictions and proposed time savings should not be presented as measured results.</p></div></BrandSection>
     <BrandSection title="Information to include in an event enquiry"><StepList items={eventDetails} /><p className="mt-5 text-sm text-ink/60">Availability, topic, scope, fees and arrangements are agreed before the event is confirmed.</p><a className="group mt-7 inline-flex items-center gap-3 rounded-full bg-forest py-2 pl-5 pr-2 text-sm font-semibold text-white" href="/contact?topic=Speaking#main">Book Vivek Pandey <span className="rounded-full bg-copper text-forest"><Arrow /></span></a></BrandSection>
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
    const mailto = buildEnquiryMailto({
      topic: data.get('topic'), duration,
      name: data.get('name'), phone: data.get('phone'), email: data.get('email'),
      eventType: data.get('eventType'), eventDate: data.get('eventDate'), location: data.get('location'),
      audienceSize: data.get('audienceSize'), speakingTopic: data.get('speakingTopic'),
    });
    setStatus('Your email app should open with a ready-to-edit message. Review the details, then press Send.');
    window.location.href = mailto;
  }

  return <>
    <section className="brand-hero mx-auto max-w-7xl px-5 pb-10 pt-16 sm:px-8 sm:pb-12 sm:pt-20 lg:px-12">
      <div data-reveal><Eyebrow>CONTACT</Eyebrow><h1 className="font-display mt-5 text-4xl font-semibold tracking-[-0.045em] text-forest sm:text-5xl lg:text-6xl">Start a conversation.</h1><p className="mt-5 text-base text-ink/60 sm:text-lg">Choose an email template, or add your details below.</p></div>
    </section>
    <section className="border-t border-ink/10"><div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14 lg:px-12">
      <div className="email-template-links" aria-label="Email templates">
        {[
          ['30-minute session', 'AI consulting', '30'],
          ['60-minute session', 'AI consulting', '60'],
          ['Speaking enquiry', 'Speaking', ''],
          ['Course enquiry', 'Academy', ''],
        ].map(([label, selectedTopic, session]) => <a key={label} href={buildEnquiryMailto({ topic: selectedTopic, duration: session })}>{label}<span aria-hidden="true">＋</span></a>)}
      </div>
       <form data-reveal onSubmit={submitEnquiry} className="contact-form grid max-w-3xl gap-5 sm:grid-cols-2 sm:gap-6">
         <label className="text-xs font-semibold text-forest">Name<input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="name" autoComplete="name" maxLength="100" required /></label>
         <label className="text-xs font-semibold text-forest">Phone number<input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="phone" type="tel" autoComplete="tel" maxLength="40" required /></label>
         <label className="text-xs font-semibold text-forest">Email<input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="email" type="email" autoComplete="email" maxLength="200" required /></label>
         <label className="text-xs font-semibold text-forest">Topic<select className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="topic" value={topic} onChange={event => setTopic(event.target.value)} required><option value="" disabled>Choose a topic</option><option>AI consulting</option><option>Speaking</option><option>Academy</option><option>Other</option></select></label>
         <label className="text-xs font-semibold text-forest">Event type <span className="font-normal text-ink/45">(for speaking)</span><select className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="eventType" required={topic === 'Speaking'}><option value="">Choose an event type</option><option>Conference or summit</option><option>Corporate session</option><option>University or college</option><option>Workshop</option><option>Panel or roundtable</option><option>Other</option></select></label>
         <label className="text-xs font-semibold text-forest">Event date <span className="font-normal text-ink/45">(for speaking)</span><input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="eventDate" type="date" required={topic === 'Speaking'} /></label>
         <label className="text-xs font-semibold text-forest">Location <span className="font-normal text-ink/45">(city or online)</span><input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="location" maxLength="160" placeholder="City, venue or online" required={topic === 'Speaking'} /></label>
         <label className="text-xs font-semibold text-forest">Audience size <span className="font-normal text-ink/45">(estimate)</span><input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="audienceSize" type="number" min="1" max="1000000" inputMode="numeric" placeholder="e.g. 80" required={topic === 'Speaking'} /></label>
         <label className="text-xs font-semibold text-forest sm:col-span-2">Speaking topic <span className="font-normal text-ink/45">(what should the audience take away?)</span><input className="mt-2 block min-h-12 w-full rounded-lg border border-ink/20 bg-white px-4 text-base font-normal outline-none transition focus:border-forest focus:ring-2 focus:ring-copper/30" name="speakingTopic" maxLength="200" placeholder="Generative AI, agentic AI, business automation..." required={topic === 'Speaking'} /></label>
         <button className="group inline-flex min-h-12 items-center justify-between gap-4 rounded-full bg-forest py-1.5 pl-5 pr-2 text-sm font-semibold text-white transition hover:bg-[#244637] sm:col-span-2 sm:w-fit" type="submit">Open email draft <span className="rounded-full bg-copper text-forest"><Arrow /></span></button>
         <p className="text-xs leading-relaxed text-ink/55 sm:col-span-2">Your email app opens a prefilled draft addressed to <a className="font-semibold text-forest underline underline-offset-2" href="mailto:wooplix15@gmail.com">wooplix15@gmail.com</a>. Review it and press Send. Nothing is stored by this website.</p>
        <p className="text-xs text-forest sm:col-span-2" role="status" aria-live="polite">{status}</p>
      </form>
    </div></section>
  </>;
}
