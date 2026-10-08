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

const enquiryForm = document.querySelector('#enquiry-form');
if (enquiryForm) {
  const parameters = new URLSearchParams(window.location.search);
  const services = ['AI consulting', 'Speaking enquiry', 'Course enquiry', 'General enquiry'];
  if (services.includes(parameters.get('service'))) enquiryForm.elements.service.value = parameters.get('service');
  if (['30', '60'].includes(parameters.get('duration'))) enquiryForm.elements.duration.value = parameters.get('duration');
  const status = document.querySelector('#enquiry-status');
  function composeEnquiry() {
    const data = new FormData(enquiryForm);
    const duration = data.get('duration');
    const session = duration === 'Not specified' ? duration : `${duration} minutes`;
    return {
      subject: `Vivek Pandey — ${data.get('service')}${duration === 'Not specified' ? '' : ` (${session})`}`,
      body: `Name: ${data.get('name')}\nEmail: ${data.get('email')}\nOrganisation: ${data.get('organisation') || 'Not specified'}\nEnquiry: ${data.get('service')}\nPreferred session: ${session}\nTime zone: ${data.get('timezone') || 'Not specified'}\n\n${data.get('message')}\n\nPlease confirm availability, scope and fees.`
    };
  }
  enquiryForm.addEventListener('submit', event => {
    event.preventDefault();
    const enquiry = composeEnquiry();
    const emailDraft = `mailto:wooplix15@gmail.com?subject=${encodeURIComponent(enquiry.subject)}&body=${encodeURIComponent(enquiry.body)}`;
    window.location.href = emailDraft;
    status.textContent = 'Email draft requested. Review and send it in your email app. If the app did not open, copy the enquiry and email it to wooplix15@gmail.com.';
  });
  document.querySelector('#copy-enquiry')?.addEventListener('click', async () => {
    if (!enquiryForm.reportValidity()) return;
    const enquiry = composeEnquiry();
    try {
      await navigator.clipboard.writeText(`To: wooplix15@gmail.com\nSubject: ${enquiry.subject}\n\n${enquiry.body}`);
      status.textContent = 'Enquiry copied. Paste it into an email to wooplix15@gmail.com. It has not been sent.';
    } catch {
      status.textContent = 'Copy is unavailable in this browser. Open an email draft or email your brief directly to wooplix15@gmail.com.';
    }
  });
}
