#!/usr/bin/env python3
"""
Static site generator for aicrazed.com.

Reads data/brands.json and renders the entire site into dist/.
No dependencies beyond the Python 3 standard library.

Usage: python3 build/build.py
"""
import json
import os
import shutil
import html as html_lib
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "brands.json")
DIST = os.path.join(ROOT, "dist")
PUBLIC = os.path.join(ROOT, "public")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    DATA = json.load(f)

SITE = DATA["site"]
CATEGORIES = DATA["categories"]
BRANDS = DATA["brands"]
BASE_URL = "https://" + SITE["domain"]

TODAY = "2026-09-12"


def esc(s):
    return html_lib.escape(str(s), quote=True)


def brand_by_slug(slug):
    for b in BRANDS:
        if b["slug"] == slug:
            return b
    return None


def brands_in(cat_slug):
    return [b for b in BRANDS if b["category"] == cat_slug]


def initial_mark(name):
    return esc(name.strip()[0].upper())


def official_root(url):
    """Best-effort root domain from a URL, for JSON-LD `url`."""
    from urllib.parse import urlparse

    p = urlparse(url)
    return p.scheme + "://" + p.netloc + "/"


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

_CATEGORY_NAV_SHORT = [("/category/{}/".format(slug), c.get("navLabel", c["label"])) for slug, c in CATEGORIES.items()]
_CATEGORY_NAV_FULL = [("/category/{}/".format(slug), c["label"]) for slug, c in CATEGORIES.items()]

NAV_ITEMS = _CATEGORY_NAV_SHORT + [
    ("/how-it-works/", "How It Works"),
    ("/about/", "About"),
]

FOOTER_NAV = [("/", "Home")] + _CATEGORY_NAV_FULL + [
    ("/how-it-works/", "How It Works"),
    ("/faq/", "FAQ"),
    ("/about/", "About"),
    ("/contact/", "Contact"),
]


def render_nav():
    items = "".join('<li><a href="{}">{}</a></li>'.format(href, label) for href, label in NAV_ITEMS)
    return items


def render_footer_nav():
    items = "".join('<li><a href="{}">{}</a></li>'.format(href, label) for href, label in FOOTER_NAV)
    return items


def layout(title, description, path, body, extra_head="", json_ld="", robots="index, follow", og_image="/og-image.png"):
    canonical = BASE_URL + path
    nav = render_nav()
    footer_nav = render_footer_nav()
    year = "2026"
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="aicrazed">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{base_url}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{base_url}{og_image}">
<meta name="robots" content="{robots}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script>
(function(){{
  try {{ if (localStorage.getItem('aicrazed-fonts-optout') === '1') return; }} catch(e) {{}}
  var head = document.head;
  ['https://fonts.googleapis.com', 'https://fonts.gstatic.com'].forEach(function(href, i){{
    var l = document.createElement('link');
    l.rel = 'preconnect';
    l.href = href;
    if (i === 1) l.crossOrigin = '';
    head.appendChild(l);
  }});
  var stylesheet = document.createElement('link');
  stylesheet.rel = 'stylesheet';
  stylesheet.href = 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Inter:wght@400;500;600;700&display=swap';
  head.appendChild(stylesheet);
}})();
</script>
<link rel="stylesheet" href="/css/main.css">
{extra_head}
{json_ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-header__bar">
    <a class="logo" href="/">aicrazed<span>.</span></a>
    <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav aria-label="Primary">
      <ul class="site-nav" id="site-nav">{nav}</ul>
    </nav>
  </div>
</header>
<div class="indie-ribbon">
  <strong>Independent directory</strong> &mdash; aicrazed is not affiliated with, endorsed by, or operated by any company listed on this site.
</div>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <a class="logo" href="/">aicrazed<span>.</span></a>
      <nav aria-label="Footer">
        <ul class="footer-nav">{footer_nav}</ul>
      </nav>
    </div>
    <div class="footer-legal">
      <p>aicrazed is an independent customer service directory. We are not affiliated with, endorsed by, sponsored by, or in any way officially connected with any of the companies listed on this site, or any of their subsidiaries or affiliates. All product and company names are trademarks&trade; or registered&reg; trademarks of their respective holders.</p>
      <p>&copy; {year} aicrazed.com. Contact info is checked against each company&rsquo;s own official website &mdash; see the &ldquo;verified&rdquo; stamp on each listing for the source and date.</p>
      <ul class="footer-legal-links">
        <li><a href="/privacy/">Privacy Policy</a></li>
        <li><a href="/terms/">Terms of Service</a></li>
        <li><a href="/trademark-notice/">Trademark Notice</a></li>
        <li><a href="/editorial-policy/">Editorial Policy</a></li>
        <li><a href="/accessibility/">Accessibility</a></li>
        <li><button type="button" id="fonts-optout-toggle" class="footer-legal-toggle">Turn off Google Fonts</button></li>
      </ul>
    </div>
  </div>
</footer>
<script src="/js/search.js" defer></script>
<script src="/js/hours.js" defer></script>
<script src="/js/fonts-optout.js" defer></script>
<script src="/js/nav-toggle.js" defer></script>
</body>
</html>
""".format(
        title=esc(title),
        description=esc(description),
        canonical=canonical,
        extra_head=extra_head,
        json_ld=json_ld,
        robots=robots,
        base_url=BASE_URL,
        og_image=og_image,
        nav=nav,
        footer_nav=footer_nav,
        body=body,
        year=year,
    )


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

def render_home():
    index = []
    for b in BRANDS:
        index.append(
            {
                "name": b["name"],
                "slug": b["slug"],
                "categoryLabel": CATEGORIES[b["category"]]["label"],
                "aliases": b["aliases"],
            }
        )
    index_json = json.dumps(index)

    featured_slugs = SITE.get("featuredBrands", [])
    featured = [brand_by_slug(s) for s in featured_slugs]
    featured = [b for b in featured if b]  # drop any stale slugs

    cards = ""
    for b in featured:
        cards += """<a class="brand-card" href="/brand/{slug}/">
  <span class="brand-card__mark" aria-hidden="true">{mark}</span>
  <span class="brand-card__name">{name}</span>
  <span class="brand-card__cat">{cat}</span>
</a>""".format(slug=b["slug"], mark=initial_mark(b["name"]), name=esc(b["name"]), cat=esc(CATEGORIES[b["category"]]["label"]))

    body = """
<section class="hero container">
  <p class="eyebrow">Customer Service Directory</p>
  <h1>Find the real support number.</h1>
  <form class="search-form" id="search-form" role="search" autocomplete="off">
    <label for="search-input" class="visually-hidden">Search for a company</label>
    <input
      class="search-input"
      id="search-input"
      type="text"
      placeholder="Search a company &mdash; e.g. Netflix, Amazon, Verizon"
      aria-autocomplete="list"
      aria-controls="search-results"
      aria-expanded="false">
    <button class="search-submit" type="submit" aria-label="Search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
    <div class="search-results" id="search-results" role="listbox" hidden></div>
  </form>
  <p class="search-hint">Sourced from each company&rsquo;s official site &mdash; press Enter to jump to the top match.</p>
  <script type="application/json" id="brand-index">{index_json}</script>
</section>

<section class="section container">
  <div class="section-head">
    <h2>Most searched</h2>
  </div>
  <div class="brand-grid">
    {cards}
  </div>
  <div class="cat-nav-pills" style="margin-top:24px;">{cat_pills}</div>
</section>

<section class="how-strip">
  <div class="container">
    <div class="section-head" style="border:none;margin-bottom:32px;">
      <h2>How this works</h2>
    </div>
    <div class="how-steps">
      <div class="how-step">
        <div class="num">01</div>
        <h3>Search or browse</h3>
        <p>Type a company name or pick one from the grid. We cover the brands people search for most when something&rsquo;s gone wrong.</p>
      </div>
      <div class="how-step">
        <div class="num">02</div>
        <h3>We verify the source</h3>
        <p>Every number, chat link, and hours listing is checked against that company&rsquo;s own official site, with the date and source link shown on the page.</p>
      </div>
      <div class="how-step">
        <div class="num">03</div>
        <h3>You contact them directly</h3>
        <p>Tap to call or open the official chat. We never collect your account details, payment info, or personal data along the way.</p>
      </div>
    </div>
  </div>
</section>

<section class="section container">
  <div class="disclaimer-block">
    <span class="mark" aria-hidden="true">i</span>
    <p><strong>aicrazed is independent.</strong> We are not affiliated with, endorsed by, or operated by any company listed on this site. We link to official, publicly available contact channels so you don&rsquo;t have to dig for them yourself. Read more on <a href="/how-it-works/">how we verify listings</a>.</p>
  </div>
</section>
""".format(
        cards=cards,
        index_json=index_json,
        cat_pills="".join(
            '<a class="cat-pill" href="/category/{}/">{}</a>'.format(slug, esc(c["label"]))
            for slug, c in CATEGORIES.items()
        ),
    )

    org_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "aicrazed",
        "url": BASE_URL + "/",
        "logo": BASE_URL + "/logo.png",
        "description": SITE["description"],
        "email": SITE["contactEmail"],
        "address": {"@type": "PostalAddress", **SITE["address"]},
    }
    website_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "aicrazed",
        "url": BASE_URL + "/",
    }
    json_ld = '<script type="application/ld+json">{}</script>\n<script type="application/ld+json">{}</script>'.format(
        json.dumps(org_ld), json.dumps(website_ld)
    )

    return layout(
        title="aicrazed — Independent Customer Service Directory",
        description=SITE["description"],
        path="/",
        body=body,
        json_ld=json_ld,
    )


# ---------------------------------------------------------------------------
# Brand page
# ---------------------------------------------------------------------------

def render_phone_field(b):
    if b.get("phone"):
        tel_href = "tel:" + "".join(ch for ch in b["phone"] if ch.isdigit() or ch == "+")
        note = "<p class='stat-sub' style='margin-top:10px;'>{}</p>".format(esc(b["phoneNote"])) if b.get("phoneNote") else ""
        return """<div class="contact-field">
  <label for="phone-link">Official phone number</label>
  <a class="phone-number" id="phone-link" href="{tel}">{display}<span class="tap-hint" aria-hidden="true">Tap to call</span></a>
  {note}
</div>""".format(tel=tel_href, display=esc(b["phone"]), note=note)
    else:
        alt = esc(b["phoneAltNote"]) if b.get("phoneAltNote") else ""
        return """<div class="contact-field">
  <label>Official phone number</label>
  <p class="no-phone-verdict">{name} publishes no phone number &mdash; use the official chat below.</p>
  <p class="stat-sub">{alt} Any &ldquo;support number&rdquo; for {name} circulating elsewhere is not confirmed and may be a scam.</p>
</div>""".format(name=esc(b["name"]), alt=alt)


def render_hours_field(b):
    h = b["hours"]
    mode = h.get("mode", "detailed")

    if mode == "unspecified":
        return """<div class="contact-field">
  <label>Support hours</label>
  <p class="no-phone-note">{text}</p>
</div>""".format(text=esc(h["text"]))

    if mode == "247":
        return """<div class="contact-field" id="hours-widget" data-tz="UTC" data-247="true" data-start="00:00" data-end="00:00" data-days="daily">
  <label>Support hours</label>
  <span class="hours-value" id="hours-value">Open 24 hours a day, every day</span>
  <span class="hours-status" id="hours-status" hidden><span class="dot" aria-hidden="true"></span><span></span></span>
</div>"""

    return """<div class="contact-field" id="hours-widget" data-tz="{tz}" data-247="false" data-start="{start}" data-end="{end}" data-days="{days}">
  <label>Support hours <span style="text-transform:none;letter-spacing:0;color:var(--ink-faint);">(your local time)</span></label>
  <span class="hours-value" id="hours-value">Loading&hellip;</span>
  <span class="hours-status" id="hours-status" hidden><span class="dot" aria-hidden="true"></span><span></span></span>
</div>""".format(
        tz=esc(h["tz"]),
        start=esc(h["start"]),
        end=esc(h["end"]),
        days=esc(h["days"]),
    )


_TZ_LABELS = {
    "America/Los_Angeles": "Pacific time",
    "America/New_York": "Eastern time",
    "America/Chicago": "Central time",
    "America/Denver": "Mountain time",
}


def _fmt_12h(hhmm):
    h, m = map(int, hhmm.split(":"))
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return "{}:{:02d} {}".format(h12, m, period)


def hours_static_text(b):
    h = b["hours"]
    mode = h.get("mode", "detailed")
    name = b["name"]
    if mode == "247":
        return "{} offers support 24 hours a day, every day.".format(name)
    if mode == "unspecified":
        return h["text"]
    start = _fmt_12h(h["start"])
    end = _fmt_12h(h["end"])
    tz = _TZ_LABELS.get(h["tz"], h["tz"])
    days = "Monday through Friday" if h.get("days") == "weekdays" else "every day"
    return "{}&rsquo;s stated support hours are {}&ndash;{} {}, {}.".format(name, start, end, tz, days)


def brand_faq_items(b):
    name = b["name"]
    if b.get("phone"):
        note = " " + b["phoneNote"] if b.get("phoneNote") else ""
        phone_a = "Yes &mdash; {name}&rsquo;s verified customer service number is {phone}.{note}".format(
            name=name, phone=b["phone"], note=note
        )
    else:
        alt = " " + b["phoneAltNote"] if b.get("phoneAltNote") else ""
        phone_a = "No. {name} does not publish a public customer service phone number.{alt} Use the official chat link on this page instead.".format(
            name=name, alt=alt
        )

    issue_names = [ci["issue"] for ci in b["commonIssues"]]
    if len(issue_names) >= 3:
        issues_text = "{}; {}; and {}".format(issue_names[0], issue_names[1], issue_names[2])
    else:
        issues_text = "; ".join(issue_names)

    return [
        ("Does {} have a customer service phone number?".format(name), phone_a),
        ("What are {}&rsquo;s support hours?".format(name), hours_static_text(b)),
        (
            "What can I contact {} about?".format(name),
            "Common reasons people contact {name} include: {issues}.".format(name=name, issues=issues_text),
        ),
    ]


def render_brand(b):
    cat = CATEGORIES[b["category"]]
    issues = "".join(
        '<details class="faq-item"><summary>{issue}</summary><p>{solution}</p></details>'.format(
            issue=esc(ci["issue"]), solution=esc(ci["solution"])
        )
        for ci in b["commonIssues"]
    )
    avg_wait = b.get("avgWaitTime") or "Not officially published"
    best_time = b.get("bestTimeToCall") or "Early or late in the day, local time"

    scam_note = b.get("scamWarningNote") or (
        "aicrazed will never ask you for a password, one-time passcode, gift card, or payment over the phone or in chat. "
        "Neither will {name}&rsquo;s real support team. If someone claiming to represent {name} asks for these, hang up "
        "&mdash; you&rsquo;ve reached a scammer, not support.".format(name=esc(b["name"]))
    )

    json_ld_obj = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": b["name"],
        "url": official_root(b["chatUrl"]),
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "areaServed": "US",
                "availableLanguage": ["English"],
                **({"telephone": b["phone"]} if b.get("phone") else {}),
                "url": b["chatUrl"],
            }
        ],
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": cat["label"], "item": BASE_URL + "/category/" + cat["slug"] + "/"},
            {"@type": "ListItem", "position": 3, "name": b["name"], "item": BASE_URL + "/brand/" + b["slug"] + "/"},
        ],
    }
    faq_items = brand_faq_items(b)
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html_lib.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html_lib.unescape(a)}}
            for q, a in faq_items
        ],
    }
    webpage_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "{} Customer Service".format(b["name"]),
        "url": BASE_URL + "/brand/" + b["slug"] + "/",
        "dateModified": b["verifiedDate"],
        "about": {"@type": "Organization", "name": b["name"]},
    }
    json_ld = "\n".join(
        '<script type="application/ld+json">{}</script>'.format(json.dumps(obj))
        for obj in (json_ld_obj, breadcrumb_ld, faq_ld, webpage_ld)
    )
    faq_html = "".join(
        '<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'.format(q=q, a=a)
        for q, a in faq_items
    )

    related = [r for r in brands_in(b["category"]) if r["slug"] != b["slug"]][:4]
    if related:
        related_links = "".join(
            '<a class="related-link" href="/brand/{slug}/">{name}</a>'.format(slug=r["slug"], name=esc(r["name"]))
            for r in related
        )
        related_html = """<div class="related-brands">
      <h3 class="label-heading">Other {cat_label} brands</h3>
      <div class="related-links">{links}</div>
    </div>""".format(cat_label=esc(cat["label"]), links=related_links)
    else:
        related_html = ""

    body = """
<div class="container">
  <p class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/category/{cat_slug}/">{cat_label}</a> &rsaquo; {name}</p>
</div>

<section class="brand-hero container">
  <div class="brand-hero__top">
    <span class="brand-hero__mark" aria-hidden="true">{mark}</span>
    <div>
      <h1>{name} customer service</h1>
      <p class="cat-label">{cat_label} &middot; Independent contact guide</p>
    </div>
  </div>

  <div class="contact-panel">
    <div class="contact-panel__grid">
      <div class="contact-panel__main">
        {phone_field}
        <div class="contact-field">
          <label>Official chat &amp; help center</label>
          <a class="chat-link" href="{chat_url}" rel="nofollow noopener" target="_blank">{chat_label} &rarr;</a>
        </div>
        {hours_field}
      </div>
      <div class="contact-panel__aside">
        <div class="stamp">
          <div class="stamp__inner">
            <div class="stamp__word">Verified</div>
            <div class="stamp__check" aria-hidden="true">&#10003;</div>
            <div class="stamp__date">{verified_date}</div>
          </div>
        </div>
        <p class="stamp-caption">Checked against {name}&rsquo;s official site on {verified_date}. <a href="{source_url}" rel="nofollow noopener" target="_blank">View source &rarr;</a></p>
      </div>
    </div>
  </div>

  <div class="scam-box">
    <span class="scam-box__icon" aria-hidden="true">!</span>
    <div>
      <h2>Before you call or chat</h2>
      <p>{scam_note}</p>
      <ul>
        <li>We never ask for your password, one-time code, or payment details.</li>
        <li>The links above go to {name}&rsquo;s own official domain &mdash; check your browser&rsquo;s address bar.</li>
        <li>If a search result or ad shows a different number for {name}, treat it as unverified until you confirm it on their official site.</li>
      </ul>
    </div>
  </div>

  <div class="issues-section">
    <h2 class="label-heading">Common issues &amp; how to resolve them</h2>
    <p class="stat-sub" style="margin-bottom:16px;">General guidance based on what usually works for this kind of issue &mdash; not {name}&rsquo;s official policy.</p>
    <div class="faq-list">{issues}</div>
  </div>

  <div class="info-grid info-grid--stats">
    <div class="info-col">
      <h3 class="label-heading">Average wait time</h3>
      <div class="stat-value" style="font-size:1.5rem;">{avg_wait}</div>
      <p class="stat-sub">{name} doesn&rsquo;t publish wait-time data &mdash; this isn&rsquo;t a verified figure.</p>
    </div>
    <div class="info-col">
      <h3 class="label-heading">Best time to contact</h3>
      <div class="stat-value" style="font-size:1.4rem;">{best_time}</div>
      <p class="stat-sub">General rule of thumb, not brand-specific data: contacting outside peak hours tends to mean a shorter wait.</p>
    </div>
  </div>

  <div class="faq-list" style="margin-top:48px;border-top:1px solid var(--rule);">
    <h2 class="label-heading" style="margin:28px 0 4px;">Quick answers</h2>
    {faq_html}
  </div>

  {related_html}
</section>
""".format(
        cat_slug=cat["slug"],
        cat_label=esc(cat["label"]),
        name=esc(b["name"]),
        mark=initial_mark(b["name"]),
        phone_field=render_phone_field(b),
        chat_url=esc(b["chatUrl"]),
        chat_label=esc(b["chatLabel"]),
        hours_field=render_hours_field(b),
        verified_date=esc(b["verifiedDate"]),
        source_url=esc(b["sourceUrl"]),
        related_html=related_html,
        scam_note=scam_note,
        issues=issues,
        avg_wait=esc(avg_wait),
        best_time=esc(best_time),
        faq_html=faq_html,
    )

    title = "{} Customer Service: Phone & Chat | aicrazed".format(b["name"])
    description = "Official {} customer service: phone number (if published), live chat, support hours, and common issues — verified {}.".format(
        b["name"], b["verifiedDate"]
    )
    return layout(
        title=title,
        description=description,
        path="/brand/{}/".format(b["slug"]),
        body=body,
        json_ld=json_ld,
        og_image="/og/{}.png".format(b["slug"]),
    )


# ---------------------------------------------------------------------------
# Original line-art icons (no stock photos, no brand logos)
# ---------------------------------------------------------------------------

_ICON_ATTRS = 'width="64" height="64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'

CATEGORY_ICONS = {
    "retail": '<svg viewBox="0 0 120 120" {attrs}><path d="M30 40 L34 20 Q36 12 44 12 H76 Q84 12 86 20 L90 40"/><rect x="24" y="40" width="72" height="60" rx="4"/><path d="M44 52 Q44 64 60 64 Q76 64 76 52"/></svg>',
    "social": '<svg viewBox="0 0 120 120" {attrs}><path d="M20 30 H100 Q108 30 108 38 V74 Q108 82 100 82 H50 L28 100 V82 H20 Q12 82 12 74 V38 Q12 30 20 30 Z"/><circle cx="45" cy="56" r="3" fill="currentColor" stroke="none"/><circle cx="60" cy="56" r="3" fill="currentColor" stroke="none"/><circle cx="75" cy="56" r="3" fill="currentColor" stroke="none"/></svg>',
    "email": '<svg viewBox="0 0 120 120" {attrs}><rect x="14" y="30" width="92" height="64" rx="4"/><path d="M18 34 L60 68 L102 34"/></svg>',
    "streaming": '<svg viewBox="0 0 120 120" {attrs}><rect x="14" y="20" width="92" height="64" rx="6"/><path d="M52 36 L74 52 L52 68 Z" fill="currentColor" stroke="none"/><path d="M40 96 H80"/></svg>',
    "telecom": '<svg viewBox="0 0 120 120" {attrs}><path d="M40 36 Q60 20 80 36"/><path d="M30 46 Q60 16 90 46"/><path d="M60 20 V36"/><circle cx="60" cy="14" r="4" fill="currentColor" stroke="none"/><rect x="48" y="60" width="24" height="40" rx="3"/></svg>',
}
for _k in CATEGORY_ICONS:
    CATEGORY_ICONS[_k] = CATEGORY_ICONS[_k].format(attrs=_ICON_ATTRS)

ABOUT_ICON = '<svg viewBox="0 0 120 120" {attrs}><circle cx="52" cy="52" r="32"/><path d="M76 76 L100 100"/><path d="M38 52 L48 62 L68 40"/></svg>'.format(attrs=_ICON_ATTRS)

HOW_IT_WORKS_ICON = '<svg viewBox="0 0 200 60" width="180" height="54" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="20" cy="30" r="10"/><path d="M30 30 H90"/><circle cx="100" cy="30" r="10"/><path d="M110 30 H170"/><circle cx="180" cy="30" r="10"/></svg>'


# ---------------------------------------------------------------------------
# Category page
# ---------------------------------------------------------------------------

def render_category(cat_slug):
    cat = CATEGORIES[cat_slug]
    members = brands_in(cat_slug)
    pills = ""
    for slug, c in CATEGORIES.items():
        cls = "cat-pill is-active" if slug == cat_slug else "cat-pill"
        pills += '<a class="{cls}" href="/category/{slug}/">{label}</a>'.format(cls=cls, slug=slug, label=esc(c["label"]))

    if not members:
        rows = """<p style="padding:32px 4px;color:var(--ink-faint);">No verified listings in this category yet &mdash; we&rsquo;re working on it. <a href="/contact/" style="color:var(--ink-soft);">Tell us which company to add next</a>.</p>"""
    else:
        rows = ""
    for b in members:
        meta = "Phone + official chat" if b.get("phone") else "Official chat &amp; help center (no public phone line)"
        rows += """<a class="cat-row" href="/brand/{slug}/">
  <span class="cat-row__left">
    <span class="cat-row__mark" aria-hidden="true">{mark}</span>
    <span>
      <span class="cat-row__name">{name}</span><br>
      <span class="cat-row__meta">{meta}</span>
    </span>
  </span>
  <span class="cat-row__arrow" aria-hidden="true">&rarr;</span>
</a>""".format(slug=b["slug"], mark=initial_mark(b["name"]), name=esc(b["name"]), meta=meta)

    body = """
<section class="cat-hero container">
  <p class="breadcrumb" style="padding:0 0 12px;"><a href="/">Home</a> &rsaquo; {label}</p>
  <div class="page-icon">{icon}</div>
  <p class="eyebrow">Category</p>
  <h1>{label}</h1>
  <p class="lede" style="margin:0;max-width:60ch;">{desc}</p>
  <div class="cat-nav-pills" style="margin-top:20px;">{pills}</div>
</section>
<section class="section container">
  <div class="cat-list">
    {rows}
  </div>
</section>
<section class="container">
  <div class="prose" style="max-width:68ch;border-top:1px solid var(--rule);padding-top:32px;">
    <h2 class="label-heading">About {label} support</h2>
    <p>{intro}</p>
  </div>
</section>
""".format(label=esc(cat["label"]), desc=esc(cat["description"]), intro=cat["intro"], pills=pills, rows=rows, icon=CATEGORY_ICONS[cat_slug])

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": cat["label"], "item": BASE_URL + "/category/" + cat_slug + "/"},
        ],
    }
    json_ld = '<script type="application/ld+json">{}</script>'.format(json.dumps(breadcrumb_ld))

    title = "{} Customer Service Contacts | aicrazed".format(cat["label"])
    description = "Verified official customer service contacts for {} companies: phone numbers, chat links, and support hours.".format(cat["label"])
    return layout(title=title, description=description, path="/category/{}/".format(cat_slug), body=body, json_ld=json_ld)


# ---------------------------------------------------------------------------
# About / Contact / How It Works
# ---------------------------------------------------------------------------

def static_page_ld(name, path):
    """WebPage + BreadcrumbList schema for general content/legal pages that
    aren't a brand, category, or the homepage (those get richer schema of
    their own elsewhere in this file)."""
    webpage_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": BASE_URL + path,
        "isPartOf": {"@type": "WebSite", "name": "aicrazed", "url": BASE_URL + "/"},
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": BASE_URL + path},
        ],
    }
    return "\n".join(
        '<script type="application/ld+json">{}</script>'.format(json.dumps(obj))
        for obj in (webpage_ld, breadcrumb_ld)
    )

def render_about():
    body = """
<section class="page-hero container">
  <div class="page-icon">{icon}</div>
  <p class="eyebrow">About</p>
  <h1>A directory, not a call center.</h1>
</section>
<section class="section container">
  <div class="prose">
    <p>aicrazed exists because searching for a company&rsquo;s support number too often lands you on a page built to look official but designed to route your call to a paid line, or worse, to someone posing as support. We built a plain, sourced alternative.</p>
    <h2>What we do</h2>
    <p>For each company listed, we find the phone number, chat link, and support hours published on that company&rsquo;s own official website, and we link straight there. Where a company doesn&rsquo;t publish a phone number, we say so plainly instead of inventing one.</p>
    <h2>What we don&rsquo;t do</h2>
    <p>We are not affiliated with, endorsed by, or operated by any company listed on this site. We do not provide customer support ourselves, we do not process payments, refunds, or account changes, and we never ask you for account credentials or payment details.</p>
    <h2>How listings stay current</h2>
    <p>Each brand page shows a &ldquo;verified&rdquo; date and a link to the official source page the information was checked against. Companies change phone systems and support hours without notice; if you find a listing that&rsquo;s out of date, <a href="/contact/">let us know</a> and we&rsquo;ll recheck it.</p>
    <p>Read more about our verification approach on the <a href="/how-it-works/">How It Works</a> page.</p>
    <h2>Who runs this</h2>
    <p>aicrazed is operated from {street}, {city} {postal}, {country}. Reach us at <a href="mailto:{email}">{email}</a> &mdash; see the <a href="/contact/">Contact page</a> for what we can and can&rsquo;t help with directly.</p>
  </div>
</section>
""".format(
        icon=ABOUT_ICON,
        street=esc(SITE["address"]["streetAddress"]),
        city=esc(SITE["address"]["addressLocality"]),
        postal=esc(SITE["address"]["postalCode"]),
        country="India",
        email=esc(SITE["contactEmail"]),
    )
    return layout(
        title="About aicrazed | Independent Customer Service Directory",
        description="aicrazed is an independent directory of official customer service contacts. Learn what we do, what we don't, and how we keep listings current.",
        path="/about/",
        json_ld=static_page_ld("About", "/about/"),
        body=body,
    )


def render_contact():
    body = """
<section class="page-hero container">
  <p class="eyebrow">Contact</p>
  <h1>Get in touch</h1>
</section>
<section class="section container">
  <div class="prose">
    <div class="contact-card">
      <h2>Report an outdated or incorrect listing</h2>
      <p>If a phone number, chat link, or hours listing is wrong, tell us which brand and what changed, and we&rsquo;ll recheck it against the official source.</p>
      <a href="mailto:{email}">{email}</a>
    </div>
    <div class="contact-card">
      <h2>Request a brand be added</h2>
      <p>Let us know which company you couldn&rsquo;t find, and we&rsquo;ll look into adding a verified listing.</p>
      <a href="mailto:{email}">{email}</a>
    </div>
    <p style="margin-top:24px;">aicrazed is an independent directory and cannot access, change, or look up your account with any listed company &mdash; for that, please use the official contact channel shown on that company&rsquo;s page.</p>
    <div class="contact-card">
      <h2>Mailing address</h2>
      <p style="margin:0;">aicrazed<br>{street}<br>{city} {postal}<br>{country}</p>
    </div>
  </div>
</section>
""".format(
        email=esc(SITE["contactEmail"]),
        street=esc(SITE["address"]["streetAddress"]),
        city=esc(SITE["address"]["addressLocality"]),
        postal=esc(SITE["address"]["postalCode"]),
        country="India",
    )
    return layout(
        title="Contact aicrazed",
        description="Report an outdated listing, request a brand be added, or get in touch with aicrazed.",
        path="/contact/",
        json_ld=static_page_ld("Contact", "/contact/"),
        body=body,
    )


def render_how_it_works():
    body = """
<section class="page-hero container">
  <div class="page-icon page-icon--wide">{icon}</div>
  <p class="eyebrow">How It Works</p>
  <h1>How we verify every listing.</h1>
</section>
<section class="section container">
  <div class="prose">
    <h2>1. We source from the company&rsquo;s own site</h2>
    <p>Every phone number, chat link, and hours listing on aicrazed is pulled directly from that company&rsquo;s own official help or contact page &mdash; never from forums, other directories, or ads. The exact source page is linked from every brand listing.</p>
    <h2>2. We say when something isn&rsquo;t published</h2>
    <p>Many companies, especially social platforms and email providers, don&rsquo;t publish a public phone number at all. Rather than guess, we say so directly and point you to the official chat or help center instead.</p>
    <h2>3. We date-stamp every check</h2>
    <p>Each brand page carries a &ldquo;verified on&rdquo; stamp with the date we last checked it against the source. Support lines and hours change; if you spot something stale, <a href="/contact/">tell us</a>.</p>
    <h2>4. We don&rsquo;t ask for anything</h2>
    <p>aicrazed doesn&rsquo;t collect account numbers, passwords, or payment details, and we never will. We link you to the official channel and step out of the way.</p>

    <h2>Spotting a fake support site</h2>
    <p>This category attracts sites built to look official. A few signals worth checking before you trust any support number you find online:</p>
    <ul>
      <li><strong>Check the domain, not the design.</strong> A page can look polished and still not belong to the company. Look at the actual web address.</li>
      <li><strong>Be wary of numbers that only appear in ads.</strong> Search ads are a common way scam &ldquo;support lines&rdquo; get placed above real results.</li>
      <li><strong>Real support won&rsquo;t ask for remote access to your device,</strong> gift cards, wire transfers, or your password to &ldquo;verify&rdquo; you.</li>
      <li><strong>When in doubt, go direct.</strong> Type the company&rsquo;s known web address in yourself rather than clicking a search result or ad.</li>
    </ul>
    <p>More questions? Check the <a href="/faq/">FAQ</a>. For the formal sourcing and correction standard behind all of this, see our <a href="/editorial-policy/">Editorial Policy</a>.</p>
  </div>
</section>
""".format(icon=HOW_IT_WORKS_ICON)
    return layout(
        title="How It Works | aicrazed Verification Process",
        description="How aicrazed verifies customer service contact info, and how to spot a fake support site.",
        path="/how-it-works/",
        json_ld=static_page_ld("How It Works", "/how-it-works/"),
        body=body,
    )


# ---------------------------------------------------------------------------
# Legal pages
# ---------------------------------------------------------------------------

def render_privacy():
    body = """
<section class="page-hero container">
  <p class="eyebrow">Legal</p>
  <h1>Privacy Policy</h1>
</section>
<section class="section container">
  <div class="prose">
    <p><strong>Effective date: September 8, 2026</strong></p>

    <p>aicrazed (&ldquo;aicrazed,&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;) publishes an independent directory of publicly available customer service contact information. This policy explains what little information we collect, and why.</p>

    <h2>Information we collect</h2>
    <p><strong>Information you send us.</strong> If you email us at <a href="mailto:help@aicrazed.com">help@aicrazed.com</a> &mdash; to report an outdated listing, request a brand be added, or ask a question &mdash; we receive your email address and whatever else you choose to include in that message. We use it only to respond to you and to investigate or correct the listing you wrote in about.</p>
    <p><strong>Information collected automatically.</strong> Like most websites, our hosting provider's servers log standard technical information with each request &mdash; things like IP address, browser type, the page requested, and the time of the request. We use these logs only to keep the site running securely and to understand aggregate traffic patterns (for example, which pages are popular). We do not use this information to build individual profiles or to track you across other sites.</p>
    <p><strong>Cookies and local storage.</strong> aicrazed itself sets no cookies &mdash; no advertising cookies, no tracking cookies, no third-party analytics. That&rsquo;s also why you won&rsquo;t see a cookie banner here: there&rsquo;s nothing to ask your consent for on our end. (The one exception is the font request described just below.) Some pages use your browser&rsquo;s local storage for small, on-device conveniences, like remembering a UI preference; that data stays on your device and is never sent to us.</p>
    <p><strong>Fonts.</strong> This site loads typefaces from Google Fonts rather than storing them ourselves. That means your browser makes a direct request to Google&rsquo;s servers to fetch them, which exposes your IP address to Google under its own privacy practices &mdash; not ours, and not something we control. No cookie is set by this request, but the IP address itself is personal data under laws like the GDPR, and courts in some jurisdictions have held that sending it to Google this way can require consent. If that matters to you, click &ldquo;Turn off Google Fonts&rdquo; in the footer of any page &mdash; it stops your browser from ever making that request, on this device, and the site falls back to your system&rsquo;s own fonts. See <a href="https://policies.google.com/privacy" rel="nofollow noopener" target="_blank">Google&rsquo;s Privacy Policy</a> for how Google handles the request when it does happen.</p>

    <h2>External links</h2>
    <p>Every brand page on aicrazed links out to that company&rsquo;s own official website, phone line, or chat channel. Once you leave aicrazed.com, that company&rsquo;s own privacy policy governs &mdash; we don&rsquo;t control, and aren&rsquo;t responsible for, the privacy practices of any third-party site we link to.</p>

    <h2>How we use information</h2>
    <ul>
      <li>To respond to your emails and correct or verify listings</li>
      <li>To keep the site secure and diagnose technical problems</li>
      <li>To understand aggregate, non-identifying usage patterns</li>
    </ul>
    <p>We do not sell personal information, and we do not share it with third parties for their own marketing purposes. We may disclose information if required by law, or to protect the rights, property, or safety of aicrazed, our users, or the public.</p>

    <h2>Data retention</h2>
    <p>We keep emails only as long as needed to address what you wrote in about, then delete them on a routine basis. Server logs are retained for a limited period consistent with standard hosting practice.</p>

    <h2>Children&rsquo;s privacy</h2>
    <p>aicrazed is not directed to children under 13, and we do not knowingly collect personal information from children.</p>

    <h2>Your choices</h2>
    <p>You&rsquo;re never required to email us to use this site. Depending on where you live, you may have rights under applicable law (such as the California Consumer Privacy Act or the EU/UK GDPR) to request access to, correction of, or deletion of personal information we hold about you. To exercise any of these rights, contact <a href="mailto:help@aicrazed.com">help@aicrazed.com</a>.</p>

    <h2>Who operates this site</h2>
    <p>aicrazed is operated from N-33, Sailing Club Road, Batla House, New Delhi 110025, India. That&rsquo;s the address to use for any formal privacy request that needs one.</p>

    <h2>Changes to this policy</h2>
    <p>If we change this policy, we&rsquo;ll update this page and change the effective date above.</p>

    <h2>Contact</h2>
    <p>Questions about this policy: <a href="mailto:help@aicrazed.com">help@aicrazed.com</a>.</p>
  </div>
</section>
"""
    return layout(
        title="Privacy Policy | aicrazed",
        description="How aicrazed collects, uses, and protects information — and what we don't collect.",
        path="/privacy/",
        json_ld=static_page_ld("Privacy Policy", "/privacy/"),
        body=body,
    )


def render_terms():
    body = """
<section class="page-hero container">
  <p class="eyebrow">Legal</p>
  <h1>Terms of Service</h1>
</section>
<section class="section container">
  <div class="prose">
    <p><strong>Effective date: September 8, 2026</strong></p>

    <p>These terms govern your use of aicrazed.com (the &ldquo;Site&rdquo;). By using the Site, you agree to them. If you don&rsquo;t agree, please don&rsquo;t use the Site.</p>

    <h2>What aicrazed is</h2>
    <p>aicrazed is an independent, informational directory of publicly available customer service contact details &mdash; phone numbers, chat links, and support hours &mdash; that we source from each listed company&rsquo;s own official website. <strong>aicrazed is not affiliated with, endorsed by, sponsored by, or otherwise officially connected with any company listed on this Site</strong>, or with any of their subsidiaries or affiliates.</p>

    <h2>Informational use only</h2>
    <p>The Site is provided for general informational purposes only. It is not a substitute for contacting a company directly through its own official channels, and it is not financial, legal, medical, or professional advice of any kind.</p>

    <h2>Accuracy of listings</h2>
    <p>We make a genuine effort to verify each listing against the relevant company&rsquo;s own official website, and we show the date of that check and a link to the source on every brand page. That said:</p>
    <ul>
      <li>Companies change phone numbers, hours, and support channels without notice, and our listings can fall out of date between checks.</li>
      <li>We do not guarantee the accuracy, completeness, or current validity of any phone number, chat link, hours, or other information on the Site.</li>
      <li>Before relying on any listing for something important &mdash; especially anything involving your account, payment, or personal information &mdash; confirm it directly on the company&rsquo;s own official website.</li>
    </ul>
    <p>If you find a listing that&rsquo;s wrong or out of date, please <a href="/contact/">tell us</a> so we can recheck it.</p>

    <h2>Third-party sites and services</h2>
    <p>The Site links to phone numbers, chat tools, and websites operated by third parties we have no control over. We aren&rsquo;t responsible for the content, security, availability, or conduct of any third-party company, phone line, or chat channel, or for any outcome of your interaction with one.</p>

    <h2>Trademarks</h2>
    <p>All company names, brand names, and trademarks referenced on the Site belong to their respective owners and are used solely to identify the company each listing describes. See our <a href="/trademark-notice/">Trademark Notice</a> for details.</p>

    <h2>Acceptable use</h2>
    <p>You agree not to:</p>
    <ul>
      <li>Use the Site to impersonate aicrazed or any company listed on it</li>
      <li>Use contact information from the Site to harass, defraud, or spam any person or company</li>
      <li>Scrape, copy, or republish the Site&rsquo;s content at scale without permission</li>
      <li>Attempt to interfere with, disrupt, or gain unauthorized access to the Site or its infrastructure</li>
    </ul>

    <h2>No warranties</h2>
    <p>The Site is provided &ldquo;as is&rdquo; and &ldquo;as available,&rdquo; without warranties of any kind, express or implied, including warranties of accuracy, merchantability, fitness for a particular purpose, or non-infringement.</p>

    <h2>Limitation of liability</h2>
    <p>To the fullest extent permitted by law, aicrazed will not be liable for any indirect, incidental, special, or consequential damages, or any loss of money, data, or goodwill, arising from your use of the Site or your reliance on any listing &mdash; including losses resulting from a scam or fraudulent contact you encountered elsewhere, even if a search led you to aicrazed first.</p>

    <h2>Changes</h2>
    <p>We may update these terms from time to time. Continued use of the Site after a change means you accept the updated terms. We&rsquo;ll update the effective date above whenever we do.</p>

    <h2>Contact</h2>
    <p>Questions about these terms: <a href="mailto:help@aicrazed.com">help@aicrazed.com</a>.</p>
  </div>
</section>
"""
    return layout(
        title="Terms of Service | aicrazed",
        description="The terms that govern your use of aicrazed's independent customer service directory.",
        path="/terms/",
        json_ld=static_page_ld("Terms of Service", "/terms/"),
        body=body,
    )


def render_trademark():
    body = """
<section class="page-hero container">
  <p class="eyebrow">Legal</p>
  <h1>Trademark Notice</h1>
</section>
<section class="section container">
  <div class="prose">
    <p><strong>Effective date: September 8, 2026</strong></p>

    <p>aicrazed is an independent directory. We are <strong>not affiliated with, endorsed by, sponsored by, or otherwise officially connected with</strong> any of the companies named on this Site, or any of their subsidiaries or affiliates.</p>

    <h2>Ownership of trademarks</h2>
    <p>All company names, product names, and brand names that appear on aicrazed &mdash; for example, the companies listed in our directory &mdash; are the trademarks or registered trademarks of their respective owners. Nothing on this Site should be read as a claim of ownership over, or any right to, those marks.</p>

    <h2>Why we use them</h2>
    <p>We reference a company&rsquo;s name only to identify which company a given listing&rsquo;s official contact information belongs to &mdash; the same way a phone book or a review would name the business it&rsquo;s describing. This is necessary to provide the directory service at all, and it&rsquo;s done factually, without implying sponsorship, endorsement, or partnership.</p>
    <p>We deliberately don&rsquo;t use any company&rsquo;s logo or visual branding on aicrazed. Every listing is identified by name only, styled entirely in aicrazed&rsquo;s own visual design, so nothing on the Site could be mistaken for a company&rsquo;s own materials.</p>

    <h2>Rights holders</h2>
    <p>If you represent a company listed on aicrazed and have a concern about how your trademark is used here, contact us at <a href="mailto:help@aicrazed.com">help@aicrazed.com</a>. We&rsquo;ll review promptly, and we&rsquo;re glad to correct, adjust, or remove a listing at the rights holder&rsquo;s request.</p>
  </div>
</section>
"""
    return layout(
        title="Trademark Notice | aicrazed",
        description="aicrazed is independent and not affiliated with any company it lists. How and why we reference brand names.",
        path="/trademark-notice/",
        json_ld=static_page_ld("Trademark Notice", "/trademark-notice/"),
        body=body,
    )


def render_editorial_policy():
    body = """
<section class="page-hero container">
  <p class="eyebrow">Legal</p>
  <h1>Editorial Policy</h1>
</section>
<section class="section container">
  <div class="prose">
    <p><strong>Effective date: September 12, 2026</strong></p>

    <p>This page sets out the standard every listing on aicrazed is held to. It exists so the standard is written down in one place, not just implied by the site&rsquo;s design.</p>

    <h2>Sourcing</h2>
    <p>Every phone number, chat link, and hours listing is checked directly against that company&rsquo;s own official website &mdash; its help center, contact page, or support article. We do not use forums, review sites, other directories, or advertisements as a source for any fact published here, even when they&rsquo;d be faster to cite.</p>

    <h2>When we can&rsquo;t verify something</h2>
    <p>Sometimes an official source can&rsquo;t be confirmed &mdash; a page is geo-blocked, temporarily unreachable, or gives conflicting information across regions. When that happens we do one of two things: state the uncertainty plainly on the page, or leave the company out of the directory entirely until it can be confirmed. We do not fill a gap with a plausible-sounding guess. For example, Disney+ is not currently listed: its official help center was inaccessible from our research environment at the time we tried to verify it, and rather than publish a guess, we left it out. We&rsquo;ll add it once we can confirm its listing directly.</p>

    <h2>What we say when a company publishes nothing</h2>
    <p>Many companies, especially social platforms and email providers, don&rsquo;t publish a public phone number at all. We say so directly on the page rather than substituting a number found elsewhere &mdash; a great deal of the fraud in this category comes from exactly that substitution.</p>

    <h2>Dates and freshness</h2>
    <p>Every brand page shows the date it was last checked. That date is never advanced without an actual recheck against the source &mdash; it is not refreshed automatically just to look current, in the sitemap or anywhere else.</p>

    <h2>No visual impersonation</h2>
    <p>aicrazed does not use any company&rsquo;s logo, icon, or visual branding. Every listing is identified by name only, in aicrazed&rsquo;s own design system, so no page could be mistaken for a company&rsquo;s own site or materials. See the <a href="/trademark-notice/">Trademark Notice</a> for the legal detail.</p>

    <h2>Corrections</h2>
    <p>If a listing is wrong or out of date, tell us on the <a href="/contact/">Contact page</a> with the company name and what changed. We recheck it against the official source and update the page &mdash; we don&rsquo;t just take a report at face value without confirming it ourselves.</p>

    <h2>Independence</h2>
    <p>aicrazed is not affiliated with, endorsed by, sponsored by, or operated by any company listed on this site. This is stated on every page, not only here.</p>
  </div>
</section>
"""
    return layout(
        title="Editorial Policy | aicrazed",
        description="The sourcing, verification, and correction standards every aicrazed listing is held to.",
        path="/editorial-policy/",
        json_ld=static_page_ld("Editorial Policy", "/editorial-policy/"),
        body=body,
    )


def render_accessibility():
    body = """
<section class="page-hero container">
  <p class="eyebrow">Legal</p>
  <h1>Accessibility Statement</h1>
</section>
<section class="section container">
  <div class="prose">
    <p><strong>Last reviewed: September 8, 2026</strong></p>

    <p>People come to aicrazed mid-problem, often stressed, and sometimes using assistive technology. Making the Site usable for everyone isn&rsquo;t a separate feature &mdash; it&rsquo;s the point.</p>

    <h2>Our standard</h2>
    <p>We aim to meet <strong>WCAG 2.1 Level AA</strong>, the widely used benchmark for web accessibility.</p>

    <h2>What we&rsquo;ve built in</h2>
    <ul>
      <li>Semantic HTML and a proper heading hierarchy on every page</li>
      <li>Color contrast of at least 4.5:1 for body text</li>
      <li>Visible keyboard focus states throughout &mdash; nothing relies on a mouse</li>
      <li>A keyboard-navigable search with proper ARIA roles for its results</li>
      <li>Large, tap-to-call phone numbers, sized and spaced for one-handed mobile use</li>
      <li>A responsive layout that works from small phones up to wide desktops</li>
    </ul>

    <h2>Ongoing work</h2>
    <p>aicrazed is a growing directory, and we keep testing new pages as we add them. If you run into a barrier &mdash; a missing label, a focus trap, low contrast we missed &mdash; it&rsquo;s a real gap we want to fix, not something to work around.</p>

    <h2>Tell us</h2>
    <p>Email <a href="mailto:help@aicrazed.com">help@aicrazed.com</a> with the page URL and what happened. We&rsquo;ll aim to respond within a few business days.</p>
  </div>
</section>
"""
    return layout(
        title="Accessibility Statement | aicrazed",
        description="aicrazed's commitment to WCAG 2.1 AA accessibility, what's built in today, and how to report a barrier.",
        path="/accessibility/",
        json_ld=static_page_ld("Accessibility Statement", "/accessibility/"),
        body=body,
    )


FAQ_ITEMS = [
    (
        "Is aicrazed affiliated with the companies you list?",
        "No. aicrazed is an independent directory. We are not affiliated with, endorsed by, sponsored by, or operated by any company listed on this site, or any of their subsidiaries or affiliates.",
    ),
    (
        "How do you verify a phone number or chat link?",
        "We check it directly against that company’s own official website — never forums, other directories, or ads. Every brand page shows a “verified on” date and links straight to the exact source page we checked. See How It Works for the full process.",
    ),
    (
        "Why don’t some companies show a phone number?",
        "Because they don’t publish one. Many social platforms, streaming services, and email providers only offer chat or a help center — no phone line at all. Rather than guess or reuse a number we found elsewhere, we say so plainly and point you to the official channel that does exist.",
    ),
    (
        "What if a listing is out of date?",
        "Companies change phone systems, hours, and support channels without notice, so it happens. Tell us which brand and what changed on the Contact page, and we’ll recheck it against the official source.",
    ),
    (
        "Is aicrazed free to use?",
        "Yes, always. There’s no account, no paywall, and nothing to sign up for — search or browse, then contact the company directly.",
    ),
    (
        "Do you collect my personal information?",
        "We don’t track you, and we don’t use advertising or analytics cookies. If you email us, we only use that to respond and to fix the listing you wrote in about. Full details are in the Privacy Policy.",
    ),
    (
        "I think I called a scam number — what do I do?",
        "Hang up or end the chat immediately, and don’t share anything further — especially a password, one-time code, gift card, or payment. Then contact the company through the verified channel on its aicrazed page. If you already shared payment or account details, contact your bank or card issuer right away, and consider reporting it to the FTC at reportfraud.ftc.gov.",
    ),
    (
        "How do I request a company be added?",
        "Email us on the Contact page with the company name, and we’ll look into adding a verified listing.",
    ),
]


def render_faq():
    items_html = ""
    faq_ld = []
    for q, a in FAQ_ITEMS:
        items_html += """<details class="faq-item">
  <summary>{q}</summary>
  <p>{a}</p>
</details>""".format(q=q, a=a)
        faq_ld.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )

    json_ld_obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_ld}
    json_ld = '<script type="application/ld+json">{}</script>\n{}'.format(
        json.dumps(json_ld_obj), static_page_ld("FAQ", "/faq/")
    )

    body = """
<section class="page-hero container">
  <p class="eyebrow">FAQ</p>
  <h1>Frequently asked questions.</h1>
</section>
<section class="section container">
  <div class="prose faq-list">
    {items}
  </div>
</section>
""".format(items=items_html)

    return layout(
        title="FAQ | aicrazed",
        description="Common questions about aicrazed: affiliation, how listings are verified, missing phone numbers, privacy, and what to do if you spot a scam.",
        path="/faq/",
        body=body,
        json_ld=json_ld,
    )


def render_404():
    body = """
<section class="page-hero container" style="text-align:center;padding:80px 0 40px;">
  <p class="eyebrow">404</p>
  <h1>We don&rsquo;t have a listing at this address.</h1>
  <p class="lede" style="max-width:46ch;margin:16px auto 32px;">The page you&rsquo;re looking for may have moved, or the company you want isn&rsquo;t in our directory yet.</p>
  <a class="btn btn--accent" href="/">Search the directory</a>
</section>
"""
    return layout(
        title="Page Not Found | aicrazed",
        description="This page doesn't exist on aicrazed.",
        path="/404.html",
        body=body,
        robots="noindex",
    )


def render_llms_txt():
    lines = [
        "# aicrazed",
        "",
        "> Independent directory of official customer service phone numbers, chat links, and support hours. "
        "Not affiliated with any company listed. Every listing is checked directly against that company's own "
        "official website, with a verification date and source link shown on the page.",
        "",
        "Key facts about this site, for anyone (human or automated) summarizing or citing it:",
        "- aicrazed has no phone/chat relationship with any listed company; we link to their official channels.",
        "- When a company does not publish a public phone number, we say so explicitly rather than guessing.",
        "- Each brand page states the date it was last checked and links to the exact official source page.",
        "",
    ]
    for slug, cat in CATEGORIES.items():
        members = brands_in(slug)
        if not members:
            continue
        lines.append("## {}".format(cat["label"]))
        lines.append("")
        for b in members:
            phone_bit = "phone: {}".format(b["phone"]) if b.get("phone") else "no public phone number"
            lines.append(
                "- [{name}]({url}): {phone_bit}, verified {date}.".format(
                    name=b["name"],
                    url=BASE_URL + "/brand/" + b["slug"] + "/",
                    phone_bit=phone_bit,
                    date=b["verifiedDate"],
                )
            )
        lines.append("")

    lines.append("## Site")
    lines.append("")
    for path, label in [
        ("/", "Home"),
        ("/how-it-works/", "How It Works"),
        ("/faq/", "Frequently Asked Questions"),
        ("/about/", "About"),
        ("/contact/", "Contact"),
    ]:
        lines.append("- [{}]({}{})".format(label, BASE_URL, path))

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST, exist_ok=True)

    # Static assets
    shutil.copytree(os.path.join(PUBLIC, "css"), os.path.join(DIST, "css"))
    shutil.copytree(os.path.join(PUBLIC, "js"), os.path.join(DIST, "js"))
    favicon_src = os.path.join(PUBLIC, "favicon.svg")
    if os.path.exists(favicon_src):
        shutil.copy(favicon_src, os.path.join(DIST, "favicon.svg"))
    og_image_src = os.path.join(PUBLIC, "og-image.png")
    if os.path.exists(og_image_src):
        shutil.copy(og_image_src, os.path.join(DIST, "og-image.png"))
    og_dir_src = os.path.join(PUBLIC, "og")
    if os.path.isdir(og_dir_src):
        shutil.copytree(og_dir_src, os.path.join(DIST, "og"))
    logo_src = os.path.join(PUBLIC, "logo.png")
    if os.path.exists(logo_src):
        shutil.copy(logo_src, os.path.join(DIST, "logo.png"))

    # Pages
    write("index.html", render_home())
    write("about/index.html", render_about())
    write("contact/index.html", render_contact())
    write("how-it-works/index.html", render_how_it_works())
    write("privacy/index.html", render_privacy())
    write("terms/index.html", render_terms())
    write("trademark-notice/index.html", render_trademark())
    write("editorial-policy/index.html", render_editorial_policy())
    write("accessibility/index.html", render_accessibility())
    write("faq/index.html", render_faq())
    write("404.html", render_404())

    for cat_slug in CATEGORIES:
        write("category/{}/index.html".format(cat_slug), render_category(cat_slug))

    for b in BRANDS:
        write("brand/{}/index.html".format(b["slug"]), render_brand(b))

    # robots.txt + sitemap.xml
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: {}/sitemap.xml\n".format(BASE_URL))
    write("llms.txt", render_llms_txt())

    static_pages = ["/", "/about/", "/contact/", "/how-it-works/", "/faq/", "/privacy/", "/terms/", "/trademark-notice/", "/editorial-policy/", "/accessibility/"]

    # (path, lastmod) pairs. Static pages use the site's last-edit date (TODAY);
    # brand pages use the date we actually last checked that listing — never
    # inflated to "today" just to look fresher than the content really is.
    url_entries = [(u, TODAY) for u in static_pages]
    for slug, cat in CATEGORIES.items():
        members = brands_in(slug)
        cat_lastmod = max((b["verifiedDate"] for b in members), default=TODAY)
        url_entries.append(("/category/{}/".format(slug), cat_lastmod))
    for b in BRANDS:
        url_entries.append(("/brand/{}/".format(b["slug"]), b["verifiedDate"]))

    sitemap_entries = "".join(
        "<url><loc>{}{}</loc><lastmod>{}</lastmod></url>\n".format(BASE_URL, u, lastmod)
        for u, lastmod in url_entries
    )
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{}</urlset>\n'.format(
            sitemap_entries
        ),
    )

    print("Built {} pages into {}".format(len(static_pages) + 1 + len(CATEGORIES) + len(BRANDS), DIST))


if __name__ == "__main__":
    build()
