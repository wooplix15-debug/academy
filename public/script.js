const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  menuButton.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
  nav.classList.toggle('is-open', !open);
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', 'Open menu');
  nav.classList.remove('is-open');
}));
document.querySelector('#year').textContent = new Date().getFullYear();
const courseDetails = document.querySelectorAll('.detail-list details');
courseDetails.forEach(detail => detail.addEventListener('toggle', () => {
  if (detail.open) courseDetails.forEach(other => { if (other !== detail) other.open = false; });
}));
