"""Build the personal website service pages from editable content.

Run from the repository root. The Academy and student chapters are untouched.
"""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
PAGES = json.loads((ROOT / 'website/personal-brand-pages.json').read_text())

def icon(name='arrow-up-right'):
    return f'<span class="link-icon" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><use href="/assets/brand-icons.svg#{name}"></use></svg></span>'

def link(label, href, cls='action'):
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{escape(label)} {icon()}</a>'

def identity():
    return '<a class="identity" href="/" aria-label="Vivek Pandey home"><span class="identity-mark">vp.</span><span>Vivek Pandey<small>AI CONSULTING · SPEAKING · EDUCATION</small></span></a>'

def header(active='/'):
    routes = [('/', 'Home'), ('/ai-consulting', 'Consulting'), ('/ai-speaking', 'Speaking'), ('/ai-courses', 'Courses'), ('/about', 'About')]
    nav = ''.join(f'<a href="{route}"'+(' aria-current="page"' if route == active else '')+f'>{label}</a>' for route, label in routes)
    nav += '<a class="nav-action" href="/contact"'+(' aria-current="page"' if active == '/contact' else '')+'>Contact '+icon()+'</a>'
    return '<header class="brand-header"><div class="shell nav-wrap">'+identity()+'<button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="brand-nav"><span></span><span></span></button><nav id="brand-nav" aria-label="Main navigation">'+nav+'</nav></div></header>'

def footer():
    return '<footer class="brand-footer"><div class="shell">'+identity()+'<div><a href="/contact">Contact '+icon()+'</a><a href="/academy">Wooplix Academy '+icon()+'</a></div><p>© <span data-brand-year>2026</span> Vivek Pandey</p></div></footer>'

def head(title, description):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#17251f"><title>{escape(title)} | Vivek Pandey</title><meta name="description" content="{escape(description,quote=True)}"><meta property="og:title" content="{escape(title,quote=True)} | Vivek Pandey"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><link rel="icon" href="/assets/vp-mark.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="/personal-brand.css"></head>'''

def section_markup(section, course=False):
    classes = 'detail-section shell' + (' course-selection' if course else '')
    out = f'<section class="{classes}"><h2>{escape(section["title"])}</h2>'
    if section.get('intro'):
        out += f'<p class="section-intro">{escape(section["intro"])}</p>'
    if section.get('cards'):
        out += '<div class="detail-cards">'
        for number, card in enumerate(section['cards'], 1):
            out += f'<article><span class="detail-card-index" aria-hidden="true">{number:02d}</span><h3>{escape(card["title"])}</h3><p>{escape(card["text"])}</p>'
            if card.get('href'):
                out += link(card['link'], card['href'], 'text-action')
            out += '</article>'
        out += '</div>'
    if section.get('items'):
        out += '<ol class="detail-steps">'+''.join(f'<li><span aria-hidden="true">{i:02d}</span><p>{escape(item)}</p></li>' for i, item in enumerate(section['items'],1))+'</ol>'
    if section.get('paragraphs'):
        out += '<div class="detail-prose">'+''.join(f'<p>{escape(p)}</p>' for p in section['paragraphs'])+'</div>'
    return out+'</section>'

def build():
    home = (PUBLIC / 'index.html').read_text()
    sessions = re.search(r'<section class="sessions-block.*?</section>',home,re.S).group(0).replace('/enquire?', '/contact?')
    home = re.sub(r'<header class="brand-header">.*?</header>',header(),home,count=1,flags=re.S)
    home = re.sub(r'<footer class="brand-footer">.*?</footer>',footer(),home,count=1,flags=re.S)
    for target in ['consulting','speaking','courses']:
        route={'consulting':'ai-consulting','speaking':'ai-speaking','courses':'ai-courses'}[target]
        home = home.replace(f'href="#{target}"',f'href="/{route}"')
    home = home.replace('/enquire?', '/contact?')
    home = home.replace('<div class="about-principles">',link('More about Vivek','/about','text-action')+'<div class="about-principles">') if 'More about Vivek' not in home else home
    (PUBLIC / 'index.html').write_text(home)
    for slug, page in PAGES.items():
        out = head(page['title'],page['intro'])+'\n<body class="brand-detail"><a class="skip" href="#main">Skip to content</a>'+header('/'+slug)+'<main id="main">'
        out += f'<section class="detail-hero shell"><div><p class="overline">{escape(page["label"])}</p><h1>{escape(page["headline"])}</h1><p class="detail-intro">{escape(page["intro"])}</p>'+link(page['cta'],page['cta_href'])+'</div>'
        out += f'<aside class="detail-summary"><svg class="summary-icon" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><use href="/assets/brand-icons.svg#{page["icon"]}"></use></svg><h2>{escape(page["summary_title"])}</h2><p>{escape(page["summary"])}</p></aside></section>'
        out += ''.join(section_markup(s,slug=='ai-courses' and i==0) for i,s in enumerate(page['sections']))
        if slug=='ai-consulting':
            out += sessions
        else:
            out += '<section class="detail-next shell"><h2>Start with your question.</h2>'+link('Ask about a course' if slug=='ai-courses' else page['cta'],'/contact?service=Course%20enquiry' if slug=='ai-courses' else page['cta_href'])+'</section>'
        out += '</main>'+footer()+'<script src="/personal-brand.js" defer></script></body></html>\n'
        (PUBLIC/(slug+'.html')).write_text(out)
    contact=(PUBLIC/'enquire.html').read_text()
    contact=re.sub(r'<header class="brand-header">.*?</header>',header('/contact'),contact,count=1,flags=re.S)
    contact=re.sub(r'<footer class="brand-footer">.*?</footer>',footer(),contact,count=1,flags=re.S)
    contact=contact.replace('<title>Enquire | Vivek Pandey</title>','<title>Contact Vivek Pandey | Consulting and Speaking Enquiries</title>')
    contact=contact.replace('Tell me what you want to work on.','Contact Vivek Pandey.')
    (PUBLIC/'contact.html').write_text(contact)
    print('Built About, Consulting, Speaking, Courses and Contact; updated Home navigation.')

if __name__=='__main__':
    build()
