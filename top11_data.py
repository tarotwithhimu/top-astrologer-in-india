# -*- coding: utf-8 -*-
# Data for "Top 11 Best Astrologer in ___" listicle pages.
#
# DELHI_TOP11 is real, sourced from a Google search-results screenshot the
# user supplied (business name / rating / review count / area / hours are
# factual, publicly-listed business-directory info). Review lines are
# paraphrased, not quoted, and Himu's own listing is added using the
# same stats used elsewhere on this site.
#
# Every other state/city uses PLACEHOLDER_NAMES — clearly-marked stand-ins
# the user will replace with real local research before publishing.

HIMU_ENTRY = dict(
    name="Tarot with Himu",
    rating="4.9", reviews="186",
    area="Guwahati (online consultations available across India)",
    hours="Open 24 hours (online)",
    note="Certified Vedic astrologer &amp; tarot reader — accurate, judgement-free guidance over WhatsApp/video call.",
    is_own=True, phone="+916901529861",
)

DELHI_TOP11 = [
    dict(name="All Problem Solutions Astrologer", rating="4.9", reviews="625",
         area="New Delhi, Delhi", hours="Open 24 hours", phone="07048949535",
         note="Known for being highly trustworthy and thorough with client problems."),
    dict(name="Ajay Shastri Astrologer", rating="5.0", reviews="529",
         area="New Delhi, Delhi", hours="Open 24 hours", phone="09540501707",
         note="On-site visits not available; consultations by phone/online."),
    dict(name="Acharya V Shastri", rating="4.9", reviews="413",
         area="New Delhi, Delhi", hours="Closed · Opens 10 am", phone="09205638684",
         note="Clients describe him as knowledgeable with a positive, encouraging approach."),
    dict(name="Astrologer Mahavir Shastri", rating="4.9", reviews="753",
         area="New Delhi, Delhi", hours="Open 24 hours", phone="07065728832",
         note="Frequently mentioned by clients as genuine and among the best in the city."),
    dict(name="Astro Guru Nirish", rating="4.8", reviews="566",
         area="New Delhi, Delhi", hours="Open 24 hours", phone="08828267456",
         note="Clients cite repeated consultations and horoscope predictions that held up over time."),
    dict(name="Samadhan Jyotish Karyalaya", rating="5.0", reviews="198",
         area="New Delhi, Delhi", hours="Open 24 hours", phone="08054537878",
         note="On-site services available at their Delhi office."),
    dict(name="Anant Gyan", rating="4.8", reviews="188",
         area="LIG Flat, Krishna Apartment, New Delhi", hours="Open 24 hours", phone=None,
         note="On-site consultations available."),
    dict(name="Astrologyexperts | Jyotish Acharya", rating="4.9", reviews="348",
         area="Delhi", hours="Closed · Opens 9:30 am", phone="09353555025",
         note="Clients highlight accurate guidance and a strong local reputation."),
    dict(name="Dr Prem Kumar Sharma", rating="4.9", reviews="408",
         area="New Delhi, Delhi", hours="Closed · Opens 9:30 am", phone="09015607139",
         note="Noted by clients for deep subject knowledge and consistently accurate predictions."),
    dict(name="Vastu Saar - Best Astrologer", rating="5.0", reviews="129",
         area="New Delhi, Delhi", hours="Open 24 hours", phone=None,
         note="Specialises in Vastu alongside general astrology consultations."),
]

PLACEHOLDER_NOTE = "[Placeholder — replace with a real local listing before publishing]"

def placeholder_entries(n=10):
    return [
        dict(name=f"Astrologer {chr(65+i)}", rating="—", reviews="—",
             area="[Add city/area]", hours="[Add hours]", phone=None,
             note=PLACEHOLDER_NOTE)
        for i in range(n)
    ]
