/* Shared, progressive motion. Content stays readable if JavaScript fails. */
(() => {
  'use strict';
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!Element.prototype.animate || !('IntersectionObserver' in window)) return;
  const running = new Set();
  const seen = new WeakSet();
  const animate = (element, delay = 0) => {
    if (preference.matches || seen.has(element)) return;
    seen.add(element);
    // Don't move focused controls or content already reached through a hash link.
    if (element.contains(document.activeElement) || element.matches(':target')) return;
    const effect = element.animate([
      { opacity: 0.35, transform: 'translateY(18px)' },
      { opacity: 1, transform: 'translateY(0)' }
    ], { duration: 650, delay, easing: 'cubic-bezier(.22,1,.36,1)' });
    running.add(effect);
    effect.finished.then(() => running.delete(effect)).catch(() => running.delete(effect));
  };
  const selectors = [
    '.hero-intro', '.hero-actions', '.statement-grid', '.section-heading',
    '.stat-grid > div', '.service-card', '.timeline article', '.wooplix-card',
    '.framework-card', '.work-tiles article', '.cta-section',
    '.academy-hero-copy', '.learning-card', '.academy-proof > div',
    '.programme-card', '.program-card', '.course-card', '.academy-section-head',
    '.course-row', '.library-heading', '.method-grid > article', '.academy-teams', '.academy-contact',
    '.detail-intro', '.detail-summary', '.detail-prose', '.detail-cards > article',
    '.detail-steps > li', '.session-grid > article', '.event-feature-copy', '.detail-next',
    '.brand-hero', '.page-hero', '.enquiry-title', '.enquiry-form',
    '.service-panel', '.service-grid > article', '.feature-grid > article',
    '.book-hero', '.book-chapter', '.course-hero', '.syllabus-unit', '.curriculum-header', '.curriculum-course',
    '.book-section > h2', '.book-section > h3', '.book-next',
    '.home-intro', '.career-heading', '.career-timeline li', '.home-section-head',
    '.home-service-list > a', '.affiliation-card', '.home-proof', '.home-session-options > a'
  ].join(',');
  const observer = new IntersectionObserver(entries => {
    let order = 0;
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      animate(entry.target, Math.min(order++ * 65, 195));
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -24px 0px' });
  const candidates = [...document.querySelectorAll(selectors)];
  // Animate one level only; nesting animations makes text hard to follow.
  candidates.filter(element => !candidates.some(parent => parent !== element && parent.contains(element)))
    .forEach(element => observer.observe(element));
  preference.addEventListener('change', () => {
    if (preference.matches) running.forEach(effect => effect.cancel());
  });
  window.addEventListener('beforeprint', () => running.forEach(effect => effect.cancel()));
})();
