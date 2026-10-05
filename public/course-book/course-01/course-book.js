(() => {
  const sections = [...document.querySelectorAll('.book-section')];
  const links = [...document.querySelectorAll('.reader-sidebar nav a')];
  const key = 'wooplix-course01-' + location.pathname + '-section';
  const setCurrent = id => links.forEach(a => {
    if (a.hash === '#' + id) a.setAttribute('aria-current', 'location');
    else a.removeAttribute('aria-current');
  });
  const observer = new IntersectionObserver(entries => {
    const current = entries.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!current) return;
    const id = current.target.querySelector('h2').id;
    setCurrent(id);
    try { localStorage.setItem(key, id); } catch (_) {}
  }, {rootMargin: '-110px 0px -55% 0px'});
  sections.forEach(s => observer.observe(s));
  try {
    const saved = localStorage.getItem(key);
    if (saved && document.getElementById(saved) && !location.hash) {
      const note = document.querySelector('.save-note');
      const a = document.createElement('a'); a.href = '#' + saved; a.textContent = 'Resume where you left off →';
      note.replaceChildren(a);
    }
  } catch (_) {}
  const button = document.querySelector('[data-print]');
  let printStates = [];
  const openSolutions = () => {
    printStates = [...document.querySelectorAll('.solutions')].map(el => [el, el.open]);
    printStates.forEach(([el]) => { el.open = true; });
  };
  const restore = () => printStates.forEach(([el, wasOpen]) => {el.open = wasOpen;});
  window.addEventListener('beforeprint', openSolutions);
  window.addEventListener('afterprint', restore);
  button?.addEventListener('click', () => { window.print(); });
})();
