#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extends the Guwahati/Assam site with pan-India "Best Astrologer in <State>"
and "Best Astrologer in <City>" pages, targeting the primary keyword
"best astrologer in India". Reuses all shared template functions (nav,
footer, page_shell, services_section, faq_section, etc.) from generate.py
so every page matches the existing site's design system exactly.
"""
import json
import re
import datetime
import generate as g   # runs generate.py's own build first (idempotent)
from india_data import STATES, CITIES

ROOT = g.ROOT
SITE = g.SITE
PHONE = g.PHONE
EMAIL = g.EMAIL

CITY_BY_NAME = {c[0]: c for c in CITIES}
STATE_BY_NAME = {s["name"]: s for s in STATES}


def clip(text, limit):
    """Hard-cap title/meta text to a search-engine-safe length, cutting at
    a word boundary. Google truncates titles ~60 chars and descriptions
    ~160 chars in results, so long place names (e.g. 'Andaman and Nicobar
    Islands') must not be allowed to blow past that — an untruncated
    template that only works for short names will silently break for
    long ones and get rewritten/truncated unpredictably by Google."""
    if len(text) <= limit:
        return text
    truncated = text[:limit - 1].rsplit(" ", 1)[0]
    return truncated.rstrip(",.-–—") + "…"


def slugify(name):
    s = name.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def state_slug(name):
    return f"best-astrologer-in-{STATE_BY_NAME[name]['slug']}.html"


def top11_slug_for_state(name):
    return f"top-11-best-astrologer-in-{STATE_BY_NAME[name]['slug']}.html"


def top11_slug_for_city(name):
    return f"top-11-best-astrologer-in-{slugify(name)}.html"


def city_slug(name):
    # Guwahati already has its own dedicated page from generate.py
    # (best-astrologer-in-guwahati.html); don't let the generic pan-India
    # city template overwrite it.
    return f"best-astrologer-in-{slugify(name)}.html"


# Patch nav() sitewide: rebrand the logo line to lead with "Best Astrologer
# in India" (the primary SEO target), and add a "States" dropdown so every
# page in the site links to the state/city structure — without touching
# generate.py's own Assam-specific nav.
_original_nav = g.nav

TOP_STATES_FOR_NAV = [
    "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu",
    "Uttar Pradesh", "West Bengal", "Gujarat", "Rajasthan",
]


def _nav_with_india(active=""):
    html = _original_nav(active)
    html = html.replace(
        '<p class="logo-title">{}Best Astrologer in Guwahati</p>'.format(g.LOGO_MARK),
        '<p class="logo-title">{}Best Astrologer in India</p>'.format(g.LOGO_MARK),
    )
    states_active = ' class="active"' if active == "states" else ''
    dd_items = "\n".join(
        f'                        <a href="{state_slug(n)}">Best Astrologer in {n}</a>' for n in TOP_STATES_FOR_NAV
    )
    states_dropdown = f'''<li class="has-dropdown">
                <a href="index.html#states" class="dropdown-toggle{states_active}">States &amp; Cities ▾</a>
                <div class="dropdown-menu">
{dd_items}
                    <a class="view-all" href="index.html#states">View All States &amp; Cities →</a>
                </div>
            </li>
            <li><a href="blog.html"'''
    return html.replace('<li><a href="blog.html"', states_dropdown, 1)


g.nav = _nav_with_india


def indiaify(html):
    """
    generate.py's shared components (footer, services, why-choose, process,
    pricing, testimonials, stats bar) hard-code Guwahati/Assam copy because
    that's the original single-city site. Pan-India pages (homepage, every
    state page, every city page) must not carry that boilerplate — it both
    dilutes the "best astrologer in India" targeting and duplicates the same
    off-topic block across hundreds of pages. This rewrites those specific,
    known strings to India-wide copy after the shared functions render.
    Guwahati mentions that are factual (studio address, "based in Guwahati")
    are written directly in generate_india.py and are untouched here.
    """
    reps = [
        ("Himu — Top Astrologer in Assam | Tarot • Vedic Astrology • Numerology • Vastu",
         "Himu — Top Astrologer in India | Tarot • Vedic Astrology • Numerology • Vastu"),
        ("<h4>Best Astrologer in Guwahati</h4>\n                <p class=\"footer-blurb\">Himu — Top Astrologer in Assam, offering Vedic Astrology, Tarot, Numerology &amp; Vastu.</p>",
         "<h4>Best Astrologer in India</h4>\n                <p class=\"footer-blurb\">Himu — Top Astrologer in India, offering Vedic Astrology, Tarot, Numerology &amp; Vastu.</p>"),
        ("""<div>
                <h4>Popular Locations</h4>
                <ul>
                    <li><a href="best-astrologer-in-barpeta.html">Barpeta</a></li>
                    <li><a href="best-astrologer-in-biswanath-chariali.html">Biswanath Chariali</a></li>
                    <li><a href="best-astrologer-in-bongaigaon.html">Bongaigaon</a></li>
                    <li><a href="best-astrologer-in-dhemaji.html">Dhemaji</a></li>
                </ul>
            </div>
            <div>
                <h4>More Locations</h4>
                <ul>
                    <li><a href="best-astrologer-in-dhubri.html">Dhubri</a></li>
                    <li><a href="best-astrologer-in-dibrugarh.html">Dibrugarh</a></li>
                    <li><a href="best-astrologer-in-diphu.html">Diphu</a></li>
                    <li><a href="best-astrologer-in-goalpara.html">Goalpara</a></li>
                </ul>
            </div>""",
         """<div>
                <h4>Popular States</h4>
                <ul>
                    <li><a href="best-astrologer-in-maharashtra.html">Maharashtra</a></li>
                    <li><a href="best-astrologer-in-delhi.html">Delhi</a></li>
                    <li><a href="best-astrologer-in-karnataka.html">Karnataka</a></li>
                    <li><a href="best-astrologer-in-tamil-nadu.html">Tamil Nadu</a></li>
                </ul>
            </div>
            <div>
                <h4>More States</h4>
                <ul>
                    <li><a href="best-astrologer-in-uttar-pradesh.html">Uttar Pradesh</a></li>
                    <li><a href="best-astrologer-in-west-bengal.html">West Bengal</a></li>
                    <li><a href="best-astrologer-in-gujarat.html">Gujarat</a></li>
                    <li><a href="best-astrologer-in-rajasthan.html">Rajasthan</a></li>
                </ul>
            </div>"""),
        ("© 2026 Himu — Best Astrologer in Guwahati &amp; Top Astrologer in Assam | Certified Vedic Astrologer &amp; Tarot Reader",
         "© 2026 Himu — Best Astrologer in India | Certified Vedic Astrologer &amp; Tarot Reader"),
        ("Serving Guwahati and all 35 districts of Assam, plus clients worldwide online | Numerology | Vastu Consultant",
         "Serving every state &amp; union territory of India online, plus in-person sessions in Guwahati | Numerology | Vastu Consultant"),
        ("The complete offering that makes Himu the best astrologer in Guwahati and a top astrologer in Assam",
         "The complete offering that makes Himu the best astrologer in India"),
        ("Why Clients Call Himu the Best Astrologer in Guwahati",
         "Why Clients Call Himu the Best Astrologer in India"),
        ("What sets a top astrologer in Assam apart — trust, accuracy and genuine care",
         "What sets a top astrologer in India apart — trust, accuracy and genuine care"),
        ("8+ years reading for clients across Guwahati and Assam, trained in Vedic astrology, tarot and numerology.",
         "8+ years reading for clients across India, trained in Vedic astrology, tarot and numerology."),
        ("Online consultations for all 35 districts, plus in-person sessions in Guwahati.",
         "Online consultations available across India, plus in-person sessions in Guwahati."),
        ("<h3>Available Across Assam</h3>", "<h3>Available Across India</h3>"),
        ("Truly the best astrologer in Guwahati I've consulted.", "Truly one of the best astrologers I've consulted."),
        ("Highly recommend to anyone in Assam.", "Highly recommend to anyone."),
        ("Booking the best astrologer in Guwahati is simple — here's what to expect",
         "Booking the best astrologer in India is simple — here's what to expect"),
        ("Transparent starting prices from the best astrologer in Guwahati — final fee confirmed on WhatsApp based on your exact requirement",
         "Transparent starting prices from the best astrologer in India — final fee confirmed on WhatsApp based on your exact requirement"),
        ("What Clients Across Assam Say", "What Clients Across India Say"),
        ('<span class="stat-num">35</span>\n                <span class="stat-label">Districts Served in Assam</span>',
         '<span class="stat-num">36</span>\n                <span class="stat-label">States &amp; UTs Served</span>'),
    ]
    for old, new in reps:
        html = html.replace(old, new)
    return html

# Rebuild the original Assam pages so the patched nav is applied
# consistently across the whole site. g.build_index() (best-astrologer-in-
# guwahati.html) is intentionally NOT called — this site has no dedicated
# Guwahati page. blog.html/post1.html are generic content and are kept.
g.build_blog()
g.build_post1()
# NOTE: g.build_locations() and the 34 Assam-district g.build_city() pages
# are intentionally NOT rebuilt — this pan-India site drops individual
# Assam district pages entirely per site owner's request.


# ---------------------------------------------------------------
# Shared bits
# ---------------------------------------------------------------

INDIA_FAQ_TEMPLATE = [
    ("Who is the best astrologer in {place}?",
     "Himu is a certified Vedic astrologer and tarot reader trusted by clients in {place}, offering online consultations over WhatsApp/video call for love, career, marriage, finance and family matters, along with in-person sessions for those who can visit the Guwahati studio."),
    ("Who is the top astrologer serving {place}?",
     "Himu is widely recommended as a top astrologer for clients in {place}, offering Vedic astrology, tarot reading, numerology and Vastu consultation entirely online, so distance is never a barrier to getting a reading."),
    ("Can I get an astrology or tarot consultation in {place} online?",
     "Yes. Most clients in {place} book their session over WhatsApp voice or video call. Share your name, and for astrology your date, time and place of birth, and Himu will prepare your chart before the session."),
    ("What astrology services are available for clients in {place}?",
     "Vedic astrology (Kundli/birth chart reading), tarot card reading, numerology, Vastu consultation, marriage matching (Kundli Milan) and remedies for career, finance, love and health concerns — all available online to clients in {place}."),
    ("How much does a session cost for clients in {place}?",
     "Consultation fees depend on the type of session (tarot, astrology, numerology or Vastu) and its duration. Message Himu on WhatsApp with your requirement from {place} and the exact fee and available slots will be shared."),
]


def wa(text):
    return g.wa_link(text)


def breadcrumb(items):
    lis = "\n".join(
        f'            <li aria-current="page">{label}</li>' if href is None
        else f'            <li><a href="{href}">{label}</a></li>'
        for href, label in items
    )
    return f'''<div class="breadcrumb-bar">
    <div class="container">
        <ol>
{lis}
        </ol>
    </div>
</div>'''


def ld_breadcrumb(items):
    elements = []
    for i, (href, label) in enumerate(items, start=1):
        url = f"{SITE}/" if href == "index.html" else (f"{SITE}/{href}" if href else None)
        entry = {"@type": "ListItem", "position": i, "name": label}
        if url:
            entry["item"] = url
        elements.append(entry)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


# ---------------------------------------------------------------
# State pages
# ---------------------------------------------------------------

def nearby_states(current_slug_name, n=3):
    others = [s for s in STATES if s["name"] != current_slug_name]
    offset = sum(ord(c) for c in current_slug_name) % len(others)
    picked = (others[offset:] + others[:offset])[:n]
    return [(state_slug(s["name"]), f"Best Astrologer in {s['name']}") for s in picked]


def build_state(s):
    name = s["name"]
    slug = state_slug(name)
    canonical = f"{SITE}/{slug}"
    faqs = [(q.format(place=name), a.format(place=name)) for q, a in INDIA_FAQ_TEMPLATE]
    keyword_pills = [
        f"Best Astrologer in {name}", f"Top Astrologer in {name}",
        f"Astrologer near me in {name}", "Best Astrologer in India",
        f"Vedic Astrologer {s['capital']}",
    ]
    state_cities = [c for c in CITIES if c[1] == name and city_slug(c[0]) != slug][:6]
    nearby_links = nearby_states(name)

    lc_paras = [
        f"{name}, in {s['region']}, is {s['fact']}. Clients across {name} — from {s['capital']} to smaller towns and districts — consult Himu, a certified Vedic astrologer and tarot reader, entirely online over WhatsApp and video call.",
        f"Whether you're in {s['capital']} or anywhere else in {name}, sessions are conducted remotely, so there's no need to travel. Share your date, time and place of birth ahead of an astrology reading, or simply come with a question in mind for a tarot session.",
        f"For clients who prefer to meet in person, visits to the Guwahati studio can be scheduled in advance for those travelling from {name}.",
    ]
    fact_items = [
        "Certified Vedic astrologer & tarot reader",
        "Accurate, judgement-free guidance",
        f"Flexible online scheduling for clients across {name}",
        "Evening slots for working professionals",
        "Confidential, one-on-one sessions",
    ]

    ld_service = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": f"Himu — Best Astrologer in {name}",
        "description": f"Vedic astrology, tarot reading, numerology and Vastu consultation for clients across {name}, India.",
        "image": f"{SITE}/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Anandapur Rd, Krishnanagar", "addressLocality": "Guwahati", "addressRegion": "Assam", "postalCode": "781005", "addressCountry": "IN"},
        "areaServed": {"@type": "State", "name": name},
        "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lon"]},
        "telephone": PHONE, "email": EMAIL, "url": canonical, "priceRange": "₹",
        "sameAs": ["https://www.facebook.com/tarotwithhimu", "https://www.instagram.com/tarotwithhimu"],
    }
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    crumb_items = [("index.html", "Home"), (None, name)]

    title = clip(f"Best Astrologer in {name} | Top Astrologer in India – Himu", 60)
    desc = clip(f"Best Astrologer in {name} — Himu is a top-rated, certified Vedic astrologer & tarot reader trusted by clients across {name}. Astrology, Numerology & Vastu online via WhatsApp. Book today.", 160)

    head_extra = f'''    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="best astrologer in {name}, top astrologer in {name}, astrologer near me {name}, best astrologer in India, vedic astrologer {s['capital']}, tarot reader {name}, numerologist {name}, vastu consultant {name}">
    <meta name="author" content="Himu">
    <meta name="robots" content="index, follow">
    <meta name="geo.placename" content="{name}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{SITE}/og-image.jpg">
    <meta property="og:url" content="{canonical}">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{json.dumps(ld_service, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_breadcrumb(crumb_items), ensure_ascii=False)}</script>'''

    lc_paras_html = "\n".join(f"            <p>{p}</p>" for p in lc_paras)
    fact_items_html = "\n".join(f"                <li>{i}</li>" for i in fact_items)
    keyword_spans = "\n".join(f"            <span>{k}</span>" for k in keyword_pills)
    nearby_links_html = "\n".join(f'            <a href="{href}">{label}</a>' for href, label in nearby_links)

    city_cards = ""
    if state_cities:
        cards = "\n".join(
            f'''            <a class="location-card" href="{city_slug(cn)}">
                <div class="lc-title">{cn}</div>
                <div class="lc-sub">{name}</div>
            </a>''' for cn, *_ in state_cities
        )
        city_cards = f'''<section class="locations-section">
    <div class="container">
        <div class="locations-intro">
            <h2 class="section-title">Cities We Serve in {name}</h2>
            <p class="section-subtitle">Online astrology &amp; tarot consultations available across {name}</p>
        </div>
        <div class="locations-grid">
{cards}
        </div>
    </div>
</section>'''

    wa_href = wa(f"Hello Himu, I want to book an astrology/tarot session in {name}")

    body = f'''{g.nav("locations")}

{breadcrumb(crumb_items)}

<header class="hero loc-hero">
    <div class="container">
        <div class="hero-badge">Serving {name}, {s['region']}</div>
        <h1>Best Astrologer in <span class="highlight">{name}</span> — Top Astrologer in India</h1>
        <p>Himu is a top-rated, certified astrologer bringing Vedic astrology, tarot reading, numerology and Vastu consultation to clients across {name} — online over WhatsApp/video call, or in person in Guwahati.</p>
        <div class="hero-buttons">
            <a href="{wa_href}" class="btn-primary" target="_blank" rel="noopener">Book a Reading in {name}</a>
            <a href="tel:{PHONE}" class="btn-outline">Call Now</a>
        </div>
        <div class="keywords">
{keyword_spans}
        </div>
    </div>
</header>

<div class="badges-strip">
    <div class="container">
        <span class="rating-chip">★★★★★ 4.9/5 — 186+ Readings</span>
        <span>Vedic &amp; Tarot Certified</span>
        <span>Online Sessions via WhatsApp</span>
        <span>Clients Across India</span>
        <span>Same-Day Slots Available</span>
    </div>
</div>

{g.stats_bar()}

{g.services_section()}

<section class="local-context">
    <div class="container lc-grid">
        <div>
            <h2>Astrology Guidance for {name}</h2>
{lc_paras_html}
        </div>
        <div class="local-fact-card">
            <h3>Why clients from {name} choose Himu</h3>
            <ul>
{fact_items_html}
            </ul>
        </div>
    </div>
</section>

{g.why_choose_section()}

{city_cards}

{g.process_section()}

{g.pricing_section()}

{g.testimonials_section(subtitle=f"Real feedback from clients across {name} and the rest of India who booked the best astrologer in India")}

{g.faq_section(f"FAQs — Best Astrologer in {name}", faqs)}

<section class="cta">
    <div class="container">
        <h2>Ready to get clarity, {name}?</h2>
        <p>Book an online tarot or astrology session today — same-day slots often available, with evening times for working professionals.</p>
        <div class="cta-buttons">
            <a href="{wa_href}" class="btn-wa" target="_blank" rel="noopener">WhatsApp Now</a>
            <a href="tel:{PHONE}" class="btn-call">Call for Appointment</a>
        </div>
        <p class="cta-note">Same-day online readings available | Evening slots for working professionals</p>
    </div>
</section>

<section class="nearby-section">
    <div class="container">
        <h2>Also Serving Other States</h2>
        <div class="nearby-links">
            <a href="{top11_slug_for_state(name)}">Top 11 Best Astrologer in {name} →</a>
{nearby_links_html}
            <a href="index.html">View All States →</a>
        </div>
    </div>
</section>

{g.footer()}'''
    html = indiaify(g.page_shell(head_extra, body, wa_href))
    open(f"{ROOT}/{slug}", "w", encoding="utf-8").write(html)


# ---------------------------------------------------------------
# City pages (pan-India)
# ---------------------------------------------------------------

def nearby_cities(current_name, current_state, n=3):
    same_state = [c for c in CITIES if c[1] == current_state and c[0] != current_name]
    pool = same_state if len(same_state) >= n else same_state + [c for c in CITIES if c[0] != current_name]
    offset = sum(ord(ch) for ch in current_name) % max(len(pool), 1)
    picked = (pool[offset:] + pool[:offset])[:n]
    return [(city_slug(c[0]), f"Best Astrologer in {c[0]}") for c in picked]


def build_city_india(entry):
    name, state, lat, lon, fact = entry
    slug = city_slug(name)
    if name == "Guwahati":
        return  # Guwahati already has its own dedicated page (best-astrologer-in-guwahati.html)
    if slug in STATE_SLUGS:
        return  # Delhi/Chandigarh/Puducherry: the state (UT) page already covers this
    canonical = f"{SITE}/{slug}"
    place_label = f"{name}, {state}"
    faqs = [(q.format(place=place_label), a.format(place=place_label)) for q, a in INDIA_FAQ_TEMPLATE]
    keyword_pills = [
        f"Best Astrologer in {name}", f"Top Astrologer in {name}",
        f"Astrologer near me in {name}", f"Tarot Reader {name}",
        f"Vastu Consultant {name}",
    ]
    nearby = nearby_cities(name, state)

    lc_paras = [
        f"{name}, {state}, is {fact}. Clients across {name} consult Himu, a certified Vedic astrologer and tarot reader based in Guwahati, entirely online over WhatsApp and video call.",
        f"Sessions are conducted primarily online, so distance from Guwahati is never a barrier to getting clarity on love, career, marriage, finance or family matters. Share your date, time and place of birth ahead of an astrology reading, or come with an open question for a tarot session.",
        f"For clients who prefer an in-person reading, visits to the Guwahati studio can be scheduled in advance for those travelling from {name}.",
    ]
    fact_items = [
        "Certified Vedic astrologer & tarot reader",
        "Accurate, judgement-free guidance",
        f"Flexible online scheduling for clients in {name}",
        "Evening slots for working professionals",
        "Confidential, one-on-one sessions",
    ]

    ld_service = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": f"Himu — Best Astrologer in {name}",
        "description": f"Vedic astrology, tarot reading, numerology and Vastu consultation for clients in {name}, {state}.",
        "image": f"{SITE}/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Anandapur Rd, Krishnanagar", "addressLocality": "Guwahati", "addressRegion": "Assam", "postalCode": "781005", "addressCountry": "IN"},
        "areaServed": {"@type": "City", "name": name},
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
        "telephone": PHONE, "email": EMAIL, "url": canonical, "priceRange": "₹",
        "sameAs": ["https://www.facebook.com/tarotwithhimu", "https://www.instagram.com/tarotwithhimu"],
    }
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    crumb_items = [("index.html", "Home"), (state_slug(state), state), (None, name)]

    title = clip(f"Best Astrologer in {name} | Top Astrologer in India – Himu", 60)
    desc = clip(f"Best Astrologer in {name}, {state} — Himu is a top-rated Vedic astrologer & tarot reader trusted by clients across {name}. Astrology, Numerology & Vastu online via WhatsApp. Book today.", 160)

    head_extra = f'''    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="best astrologer in {name}, top astrologer in {name}, astrologer near me {name}, best astrologer in India, tarot reader {name}, numerologist {name}, vastu consultant {name}">
    <meta name="author" content="Himu">
    <meta name="robots" content="index, follow">
    <meta name="geo.placename" content="{name}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{SITE}/og-image.jpg">
    <meta property="og:url" content="{canonical}">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{json.dumps(ld_service, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_breadcrumb(crumb_items), ensure_ascii=False)}</script>'''

    lc_paras_html = "\n".join(f"            <p>{p}</p>" for p in lc_paras)
    fact_items_html = "\n".join(f"                <li>{i}</li>" for i in fact_items)
    keyword_spans = "\n".join(f"            <span>{k}</span>" for k in keyword_pills)
    nearby_links_html = "\n".join(f'            <a href="{href}">{label}</a>' for href, label in nearby)

    wa_href = wa(f"Hello Himu, I want to book an astrology/tarot session in {name}")

    body = f'''{g.nav("locations")}

{breadcrumb(crumb_items)}

<header class="hero loc-hero">
    <div class="container">
        <div class="hero-badge">Serving {name}, {state}</div>
        <h1>Best Astrologer in <span class="highlight">{name}</span> — Top Astrologer in India</h1>
        <p>Himu is a top-rated, certified astrologer in Guwahati bringing Vedic astrology, tarot reading, numerology and Vastu consultation to clients in {name} — online over WhatsApp/video call, or in person in Guwahati.</p>
        <div class="hero-buttons">
            <a href="{wa_href}" class="btn-primary" target="_blank" rel="noopener">Book a Reading in {name}</a>
            <a href="tel:{PHONE}" class="btn-outline">Call Now</a>
        </div>
        <div class="keywords">
{keyword_spans}
        </div>
    </div>
</header>

<div class="badges-strip">
    <div class="container">
        <span class="rating-chip">★★★★★ 4.9/5 — 186+ Readings</span>
        <span>Vedic &amp; Tarot Certified</span>
        <span>Online Sessions via WhatsApp</span>
        <span>Clients Across India</span>
        <span>Same-Day Slots Available</span>
    </div>
</div>

{g.stats_bar()}

{g.services_section()}

<section class="local-context">
    <div class="container lc-grid">
        <div>
            <h2>Astrology Guidance for {name}</h2>
{lc_paras_html}
        </div>
        <div class="local-fact-card">
            <h3>Why clients from {name} choose Himu</h3>
            <ul>
{fact_items_html}
            </ul>
        </div>
    </div>
</section>

{g.why_choose_section()}

{g.process_section()}

{g.pricing_section()}

{g.testimonials_section(subtitle=f"Real feedback from clients across {name} and India who booked the best astrologer in India")}

{g.faq_section(f"FAQs — Best Astrologer in {name}", faqs)}

<section class="cta">
    <div class="container">
        <h2>Ready to get clarity, {name}?</h2>
        <p>Book an online tarot or astrology session today — same-day slots often available, with evening times for working professionals.</p>
        <div class="cta-buttons">
            <a href="{wa_href}" class="btn-wa" target="_blank" rel="noopener">WhatsApp Now</a>
            <a href="tel:{PHONE}" class="btn-call">Call for Appointment</a>
        </div>
        <p class="cta-note">Same-day online readings available | Evening slots for working professionals</p>
    </div>
</section>

<section class="nearby-section">
    <div class="container">
        <h2>Also Serving Nearby Areas</h2>
        <div class="nearby-links">
            <a href="{top11_slug_for_city(name)}">Top 11 Best Astrologer in {name} →</a>
{nearby_links_html}
            <a href="{state_slug(state)}">View All of {state} →</a>
        </div>
    </div>
</section>

{g.footer()}'''
    html = indiaify(g.page_shell(head_extra, body, wa_href))
    open(f"{ROOT}/{slug}", "w", encoding="utf-8").write(html)


# ---------------------------------------------------------------
# India homepage (index.html) — the primary "best astrologer in India" page
# ---------------------------------------------------------------

INDIA_FAQ = [
    ("Who is the best astrologer in India?",
     "Himu is a certified Vedic astrologer and tarot reader based in Guwahati, trusted by clients across India for accurate, judgement-free guidance on love, career, marriage, finance and family matters — available online via WhatsApp/video call from any state, or in person in Guwahati."),
    ("How can I consult a top astrologer in India online?",
     "Message Himu on WhatsApp with your name, date of birth (and time/place of birth for a Vedic astrology reading), and the city you're writing from. Available slots and fees will be shared, and the session is conducted over WhatsApp voice or video call."),
    ("Which cities and states does Himu serve?",
     "Clients from every state and union territory in India are served online — from Delhi, Mumbai and Bengaluru to smaller towns across the country — plus in-person sessions for clients who can visit the Guwahati studio."),
    ("What is the difference between tarot reading and Vedic astrology?",
     "Vedic astrology uses your exact date, time and place of birth to map planetary positions and predict long-term life patterns, while tarot reading uses card spreads for intuitive guidance on a specific question or situation. Many clients combine both."),
    ("How much does an astrology or tarot session cost?",
     "Fees vary by session type — tarot, Vedic astrology, numerology or Vastu — and duration. Message Himu on WhatsApp with what you need and the exact price and available slots will be shared before you book."),
    ("What can astrology and tarot help with?",
     "Common areas include love and relationships, marriage compatibility (Kundli matching), career and job changes, financial decisions, family matters, and planetary remedies for ongoing difficulties."),
]


def build_india_page():
    slug = "index.html"
    canonical = f"{SITE}/"

    regions = {}
    for s in STATES:
        regions.setdefault(s["region"], []).append(s)

    region_blocks = []
    for region, states in regions.items():
        cards = "\n".join(
            f'''            <a class="location-card" href="{state_slug(s['name'])}">
                <div class="lc-title">{s['name']}</div>
                <div class="lc-sub">Capital: {s['capital']}</div>
            </a>''' for s in states
        )
        region_blocks.append(f'''        <div class="division-block">
            <h3>{region}</h3>
            <div class="locations-grid">
{cards}
            </div>
        </div>''')

    top_cities = CITIES[:24]
    city_cards = "\n".join(
        f'''            <a class="location-card" href="{city_slug(c[0])}">
                <div class="lc-title">{c[0]}</div>
                <div class="lc-sub">{c[1]}</div>
            </a>''' for c in top_cities
    )

    ld_service = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Himu Astrology — Best Astrologer in India",
        "description": "Best Astrologer in India. Certified Vedic Astrologer, Tarot Reader, Numerologist and Vastu Consultant, Himu, serving clients across every state and union territory of India, online and in Guwahati.",
        "image": f"{SITE}/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Anandapur Rd, Krishnanagar", "addressLocality": "Guwahati", "addressRegion": "Assam", "postalCode": "781005", "addressCountry": "IN"},
        "areaServed": {"@type": "Country", "name": "India"},
        "geo": {"@type": "GeoCoordinates", "latitude": 26.1445, "longitude": 91.7362},
        "telephone": PHONE, "email": EMAIL, "url": canonical, "priceRange": "₹",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "186"},
        "sameAs": ["https://www.facebook.com/tarotwithhimu", "https://www.instagram.com/tarotwithhimu"],
    }
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in INDIA_FAQ]}

    title = clip("Best Astrologer in India | Top Astrologer, Vedic Astrology & Tarot – Himu", 60)
    desc = clip("Best Astrologer in India — Himu is a certified Vedic astrologer & tarot reader serving every state and union territory online via WhatsApp. Astrology, Numerology & Vastu consultations. Book today.", 160)

    head_extra = f'''    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="best astrologer in India, top astrologer in India, online astrologer India, best vedic astrologer India, best tarot reader India, best numerologist India, vastu consultant India">
    <meta name="author" content="Himu">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{SITE}/og-image.jpg">
    <meta property="og:url" content="{canonical}">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{json.dumps(ld_service, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>'''

    wa_href = wa("Hello Himu, I want to book an astrology/tarot session")

    body = f'''{g.nav("home")}

<header class="hero">
    <div class="container hero-container">
        <div class="hero-content">
            <div class="hero-badge">Trusted Across All 28 States &amp; 8 Union Territories</div>
            <h1>Best Astrologer in <span class="highlight">India</span><br>Vedic Astrology, Tarot &amp; Vastu — Online</h1>
            <p>Himu — certified Vedic astrologer &amp; tarot reader based in Guwahati, trusted by clients across every state and union territory of India. Accurate predictions for love, career, marriage, finance and life purpose, delivered online over WhatsApp.</p>
            <div class="hero-buttons">
                <a href="{wa_href}" class="btn-primary" target="_blank" rel="noopener">Book a Reading</a>
                <a href="#states" class="btn-outline">Find Your State</a>
            </div>
            <div class="keywords">
                <span>Best Astrologer in India</span>
                <span>Top Astrologer in India</span>
                <span>Online Astrologer India</span>
                <span>Vastu Consultant India</span>
            </div>
        </div>
        <div class="hero-image">
            {g.hero_visual_svg()}
            <p class="hero-tagline">"Accurate. Empathetic. Life-changing insights."</p>
        </div>
    </div>
</header>

<div class="badges-strip">
    <div class="container">
        <span class="rating-chip">★★★★★ 4.9/5 — 186+ Readings</span>
        <span>Vedic &amp; Tarot Certified</span>
        <span>Online Sessions via WhatsApp</span>
        <span>Serving All States &amp; UTs of India</span>
        <span>Same-Day Slots Available</span>
    </div>
</div>

{g.stats_bar()}

{g.services_section()}

{g.why_choose_section()}

{g.process_section()}

<section id="states" class="locations-section">
    <div class="container">
        <div class="locations-intro">
            <h2 class="section-title">Best Astrologer — Every State &amp; Union Territory</h2>
            <p class="section-subtitle">Find your state below for local astrology &amp; tarot guidance, available online anywhere in India</p>
        </div>
        <div class="location-search-wrap">
            <input type="text" id="locationSearch" class="location-search" placeholder="Search your state…" aria-label="Search your state">
        </div>
{chr(10).join(region_blocks)}
    </div>
</section>

<section class="locations-section">
    <div class="container">
        <div class="locations-intro">
            <h2 class="section-title">Best Astrologer in Your City</h2>
            <p class="section-subtitle">Popular cities across India — tap yours for local astrology &amp; tarot guidance</p>
        </div>
        <div class="locations-grid">
{city_cards}
        </div>
    </div>
</section>

{g.pricing_section()}

{g.testimonials_section(subtitle="Real feedback from clients across India who booked the best astrologer in India")}

{g.faq_section("Frequently Asked Questions — Best Astrologer in India", INDIA_FAQ)}

<section class="cta">
    <div class="container">
        <h2>Ready to get clarity, wherever you are in India?</h2>
        <p>Book an online tarot or astrology session today with India's trusted Vedic astrologer — same-day slots often available.</p>
        <div class="cta-buttons">
            <a href="{wa_href}" class="btn-wa" target="_blank" rel="noopener">WhatsApp Now</a>
            <a href="tel:{PHONE}" class="btn-call">Call for Appointment</a>
        </div>
        <p class="cta-note">Same-day online readings available | Evening slots for working professionals</p>
    </div>
</section>

{g.footer()}'''
    html = indiaify(g.page_shell(head_extra, body, wa_href))
    open(f"{ROOT}/{slug}", "w", encoding="utf-8").write(html)


# ---------------------------------------------------------------
# Run
# ---------------------------------------------------------------

for s in STATES:
    build_state(s)
print(f"{len(STATES)} state pages built")

STATE_SLUGS = {state_slug(s["name"]) for s in STATES}

for c in CITIES:
    build_city_india(c)
print(f"{len(CITIES)} pan-India city pages built (Guwahati/Delhi/Chandigarh/Puducherry skipped, already covered)")

build_india_page()
print("index.html (India homepage) built")


# ---------------------------------------------------------------
# Combined sitemap.xml (Assam pages + pan-India pages)
# ---------------------------------------------------------------
def build_full_sitemap():
    TODAY = datetime.date.today().isoformat()
    pages = [("index.html", "1.0"), ("blog.html", "0.6"), ("post1.html", "0.6")]
    pages += [(state_slug(s["name"]), "0.85") for s in STATES]
    pages += [(city_slug(c[0]), "0.8") for c in CITIES if city_slug(c[0]) not in {state_slug(s["name"]) for s in STATES}]

    entries = []
    seen = set()
    for path, priority in pages:
        if path in seen:
            continue
        seen.add(path)
        loc = f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"
        entries.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{priority}</priority>
  </url>''')

    sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>
'''
    open(f"{ROOT}/sitemap.xml", "w", encoding="utf-8").write(sitemap_xml)
    print(f"sitemap.xml rebuilt ({len(entries)} urls)")


build_full_sitemap()
