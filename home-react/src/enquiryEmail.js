const recipient = 'wooplix15@gmail.com';

// Build an email draft locally. The visitor's email app sends it after review.
export function buildEnquiryMailto({ topic = 'Other', duration = '', name = '', phone = '', email = '' } = {}) {
  const kind = ['AI consulting', 'Speaking', 'Academy', 'Other'].includes(topic) ? topic : 'Other';
  const minutes = kind === 'AI consulting' && ['30', '60'].includes(String(duration)) ? String(duration) : '';
  const titles = {
    'AI consulting': minutes ? `${minutes}-minute AI consulting session request` : 'AI consulting enquiry',
    Speaking: 'Speaking enquiry',
    Academy: 'Academy course enquiry',
    Other: 'Website enquiry',
  };
  const requests = {
    'AI consulting': minutes ? `I would like to request a ${minutes}-minute AI consulting session.` : 'I would like to discuss an AI consulting opportunity.',
    Speaking: 'I would like to discuss a speaking session or workshop.',
    Academy: 'I would like to learn more about an Academy course.',
    Other: 'I would like to get in touch.',
  };
  const details = {
    'AI consulting': ['What I need help with: [one or two sentences]', 'Preferred date and time: [add your preference]', 'Time zone: [add your time zone]'],
    Speaking: ['Event or organisation: [add the name]', 'Date and location / online: [add details]', 'Audience and topic: [a short description]'],
    Academy: ['Course I am interested in: [add the course name]', 'Learning goal: [one or two sentences]', 'Learning for: [myself / my team]'],
    Other: ['My question: [one or two sentences]'],
  };
  const cleanName = String(name).trim();
  const subjectName = cleanName.replace(/[\r\n]+/g, ' ');
  const subject = titles[kind] + (subjectName ? ` — ${subjectName}` : '');
  const body = [
    'Hello Vivek,', '', requests[kind], '',
    `Name: ${cleanName || '[your name]'}`,
    `Email: ${String(email).trim() || '[your email]'}`,
    `Phone: ${String(phone).trim() || '[your number, optional]'}`,
    '', ...details[kind], '', 'Thank you,', cleanName || '[your name]',
  ].join('\r\n');
  return `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
