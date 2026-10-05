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
const yearLabel = document.querySelector('#year');
if (yearLabel) yearLabel.textContent = new Date().getFullYear();
document.querySelectorAll('[data-chapters]').forEach(button => {
  button.addEventListener('click', () => {
    const open = button.dataset.chapters === 'open';
    document.querySelectorAll('.module-list details').forEach(chapter => { chapter.open = open; });
  });
});
function openLinkedChapter() {
  const target = document.getElementById(window.location.hash.slice(1));
  if (target?.matches('details.module')) target.open = true;
}
window.addEventListener('hashchange', openLinkedChapter);
openLinkedChapter();
const courseDetails = document.querySelectorAll('.detail-list details');
courseDetails.forEach(detail => detail.addEventListener('toggle', () => {
  if (detail.open) courseDetails.forEach(other => { if (other !== detail) other.open = false; });
}));
