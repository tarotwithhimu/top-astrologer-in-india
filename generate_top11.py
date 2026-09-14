#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds "Top 11 Best Astrologer in ___" pages for every state/UT and city.
Delhi uses real, user-supplied data (see top11_data.DELHI_TOP11); every
other page uses clearly-marked placeholder entries for the user to
replace with real local research before publishing.
"""
import json
import generate as g
import generate_india as gi
from india_data import STATES, CITIES
from top11_data import HIMU_ENTRY, DELHI_TOP11, placeholder_entries

ROOT = g.ROOT
SITE = g.SITE
PHONE = g.PHONE
EMAIL = g.EMAIL


def build_ranked_list(entries):
    cards = []
    for i, e in enumerate(entries, start=1):
        own_cls = " ranked-card-own" if e.get("is_own") else ""
        phone_html = ""
        if e.get("phone"):
            digits = e["phone"] if e["phone"].startswith("+") else f"+91{e['phone'].lstrip('0')}"
            phone_html = f'<a class="ranked-phone" href="tel:{digits}">{e["phone"]}</a>'
        cta = ""
        if e.get("is_own"):
            cta = f'<a class="btn-secondary" href="{gi.wa(f"Hello Himu, I found you on the Top 11 Best Astrologer list and want to book a session")}" target="_blank" rel="noopener">WhatsApp Now →</a>'
        rating_html = f'★ {e["rating"]} ({e["reviews"]} reviews)' if e["rating"] != "—" else "Rating: —"
        cards.append(f'''            <li class="ranked-card{own_cls}">
                <span class="ranked-num">{i}</span>
                <div class="ranked-body">
                    <h3>{e['name']}</h3>
                    <p class="ranked-meta">{rating_html} · {e['area']} · {e['hours']}</p>
                    <p class="ranked-note">{e['note']}</p>
                    {phone_html}
                    {cta}
                </div>
            </li>''')
    return f'''<section class="local-context">
    <div class="container">
        <ol class="ranked-list">
{chr(10).join(cards)}
        </ol>
    </div>
</section>'''


def entries_for(place_name, is_delhi):
    if is_delhi:
        entries = [HIMU_ENTRY] + DELHI_TOP11
    else:
        placeholders = placeholder_entries(10)
        entries = [HIMU_ENTRY] + placeholders
    return entries[:11]


TOP11_FAQ_TEMPLATE = [
    ("How was this Top 11 list put together?",
     "This list combines Tarot with Himu's own online astrology practice with other astrologers who come up prominently for {place} searches. It's a starting reference, not an official or certified ranking — always verify current details (hours, reviews, pricing) directly before booking."),
    ("Is Tarot with Himu based in {place}?",
     "Tarot with Himu is based in Guwahati, Assam, and serves clients in {place} entirely online — over WhatsApp voice or video call — so location is not a barrier to booking a session."),
    ("How do I book a session with Tarot with Himu?",
     "Message on WhatsApp with your name and, for a Vedic astrology reading, your date, time and place of birth. Available slots and fees will be shared before you confirm."),
]


def build_top11_page(place_name, place_type, slug, crumb_parent, entries, is_delhi):
    canonical = f"{SITE}/{slug}"
    faqs = [(q.format(place=place_name), a.format(place=place_name)) for q, a in TOP11_FAQ_TEMPLATE]
    crumb_items = [("index.html", "Home"), crumb_parent, (None, f"Top 11 Best Astrologer in {place_name}")]

    title = gi.clip(f"Top 11 Best Astrologer in {place_name} — Ranked List | Himu", 60)
    desc = gi.clip(f"Top 11 best astrologer in {place_name} — a ranked list of trusted astrologers serving {place_name}, including Tarot with Himu's online Vedic astrology &amp; tarot consultations.", 160)

    ld_item_list = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": f"Top 11 Best Astrologer in {place_name}",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": e["name"]} for i, e in enumerate(entries, start=1)
        ],
    }
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

    head_extra = f'''    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="top 11 best astrologer in {place_name}, best astrologer in {place_name}, top astrologer {place_name}">
    <meta name="author" content="Himu">
    <meta name="robots" content="{'index, follow' if is_delhi else 'noindex, follow'}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{json.dumps(ld_item_list, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(gi.ld_breadcrumb(crumb_items), ensure_ascii=False)}</script>'''

    disclaimer = "" if is_delhi else f'''<div class="badges-strip">
    <div class="container">
        <span>⚠ Draft list — placeholder entries below are for template/layout purposes only and should be replaced with real, verified local listings before this page is published.</span>
    </div>
</div>

'''
    source_note = (
        "Rankings reflect prominent local search results as of the data collection date, alongside Tarot with Himu's own online practice; it is an informal reference, not a certified or official ranking."
        if is_delhi else
        "This page is a template — the placeholder entries need to be replaced with real, currently-accurate local listings (name, rating, review count, hours) before publishing."
    )

    wa_href = gi.wa(f"Hello Himu, I found you on the Top 11 Best Astrologer in {place_name} list")

    body = f'''{g.nav("india")}

{gi.breadcrumb(crumb_items)}

<header class="hero loc-hero">
    <div class="container">
        <div class="hero-badge">{place_type}: {place_name}</div>
        <h1>Top 11 Best Astrologer in <span class="highlight">{place_name}</span></h1>
        <p>{source_note}</p>
        <div class="hero-buttons">
            <a href="{wa_href}" class="btn-primary" target="_blank" rel="noopener">Book With Tarot with Himu</a>
            <a href="tel:{PHONE}" class="btn-outline">Call Now</a>
        </div>
    </div>
</header>

{disclaimer}{build_ranked_list(entries)}

{g.faq_section(f"FAQs — Top 11 Best Astrologer in {place_name}", faqs)}

<section class="cta">
    <div class="container">
        <h2>Book the Top-Ranked Online Option — Tarot with Himu</h2>
        <p>Online Vedic astrology, tarot, numerology &amp; Vastu consultations, available to clients in {place_name} over WhatsApp.</p>
        <div class="cta-buttons">
            <a href="{wa_href}" class="btn-wa" target="_blank" rel="noopener">WhatsApp Now</a>
            <a href="tel:{PHONE}" class="btn-call">Call for Appointment</a>
        </div>
    </div>
</section>

{g.footer()}'''
    html = gi.indiaify(g.page_shell(head_extra, body, wa_href))
    open(f"{ROOT}/{slug}", "w", encoding="utf-8").write(html)


# ---------------------------------------------------------------
# Run: states
# ---------------------------------------------------------------
state_slugs_built = []
state_slugs_indexable = []
for s in STATES:
    name = s["name"]
    is_delhi = (name == "Delhi")
    entries = entries_for(name, is_delhi)
    slug = gi.top11_slug_for_state(name)
    build_top11_page(name, "State/UT", slug, (gi.state_slug(name), name), entries, is_delhi)
    state_slugs_built.append(slug)
    if is_delhi:
        state_slugs_indexable.append(slug)
print(f"{len(state_slugs_built)} state Top-11 pages built")

# ---------------------------------------------------------------
# Run: cities (skip the 3 that collapse into their state/UT page)
# ---------------------------------------------------------------
city_slugs_built = []
city_slugs_indexable = []  # none currently — no city-level page has real data yet
for c in CITIES:
    name, state = c[0], c[1]
    if gi.city_slug(name) in gi.STATE_SLUGS:
        continue  # Delhi/Chandigarh/Puducherry: state page already covers this
    is_delhi_city = False  # real Delhi handled via the state page above
    entries = entries_for(name, is_delhi_city)
    slug = gi.top11_slug_for_city(name)
    build_top11_page(name, "City", slug, (gi.city_slug(name), name), entries, is_delhi_city)
    city_slugs_built.append(slug)
print(f"{len(city_slugs_built)} city Top-11 pages built")


# ---------------------------------------------------------------
# Extend sitemap.xml with ONLY the indexable Top-11 URLs. Placeholder
# pages are marked noindex above (they aren't ready to publish yet), so
# they must not be submitted for crawling/indexing either — 135 near-
# identical thin pages in the sitemap is exactly the pattern search
# engines flag as low-quality at scale.
# ---------------------------------------------------------------
import re as _re
import datetime as _dt

sitemap_path = f"{ROOT}/sitemap.xml"
existing = open(sitemap_path, encoding="utf-8").read()
TODAY = _dt.date.today().isoformat()
new_entries = []
for slug in state_slugs_indexable + city_slugs_indexable:
    new_entries.append(f'''  <url>
    <loc>{SITE}/{slug}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>0.7</priority>
  </url>''')
updated = existing.replace("</urlset>", "\n".join(new_entries) + "\n</urlset>")
open(sitemap_path, "w", encoding="utf-8").write(updated)
print(f"sitemap.xml extended with {len(new_entries)} Top-11 URLs")
