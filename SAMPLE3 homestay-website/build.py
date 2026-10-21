#!/usr/bin/env python3
"""
Homestay / Resort website generator.
Edit the CONTENT block below, run `python3 build.py`, upload the `site/` folder.
All pages, room pages, sitemap, robots.txt, schema and SVG placeholder art are generated.
"""
import os, math, json, random, shutil, html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")

# =====================================================================
# CONTENT  (SAMPLE DATA — replace every value with the real property's)
# =====================================================================
S = dict(
    name="Sahyadri Mist Retreat",
    short="Sahyadri Mist",
    tagline="Wake up above the clouds, deep in the Western Ghats.",
    sub="A family-run forest homestay in Dandeli, Karnataka — private cottages, river-fresh air, bonfire nights and home-cooked Malnad food.",
    domain="https://www.example.com",          # <- your live domain, no trailing slash
    phone="+91 99999 99999", phone_raw="+919999999999", wa="919999999999",
    email="stay@example.com",
    address="Kulgi Road, near Ambikanagar, Dandeli, Uttara Kannada, Karnataka 581325",
    lat=15.2700, lng=74.6200,
    ga="G-XXXXXXXXXX",                         # <- Google Analytics 4 ID (leave to disable)
    price_from="₹2,200",
    checkin="12:00 PM", checkout="11:00 AM",
    rating="4.9", reviews_count="212",
    social=dict(instagram="https://instagram.com/", facebook="https://facebook.com/"),
)

ROOMS = [
    dict(slug="canopy-suite", name="Canopy Suite", tag="Signature", price=6500, unit="night",
         short="Treetop suite with a private deck facing the misty valley.",
         desc="Our most-loved stay. A raised timber suite with floor-to-ceiling windows, a king bed dressed in handloom linen, a private deck for sunrise chai and an outdoor rain-shower. Built for couples who want the forest all to themselves.",
         cap="2 adults + 1 child", bed="1 King bed", size="420 sq ft",
         amen=[("fire","Private deck"),("snow","Air conditioning"),("shower","Rain shower"),("wifi","Fast Wi-Fi"),("coffee","Tea & coffee kit"),("mountain","Valley view")],
         incl=["Welcome drink on arrival","Complimentary breakfast for two","Evening tea with snacks","Bonfire access","Guided sunrise walk","Free parking"],
         imgs=["canopy-1","canopy-2","canopy-3"]),
    dict(slug="riverside-cottage", name="Riverside Cottage", tag="Most popular", price=4800, unit="night",
         short="Stone-and-wood cottage a few steps from the river.",
         desc="A cosy standalone cottage with a sit-out facing the water. Fall asleep to the sound of the river and wake to birdsong. Ideal for couples and small friend groups.",
         cap="2 adults + 2 children", bed="1 Queen + 1 sofa bed", size="360 sq ft",
         amen=[("leaf","Garden sit-out"),("snow","Air conditioning"),("shower","Hot water 24x7"),("wifi","Wi-Fi"),("tv","Smart TV"),("bird","River & birds")],
         incl=["Welcome drink","Complimentary breakfast","Evening tea & pakoras","Bonfire access","Free parking","Daily housekeeping"],
         imgs=["river-1","river-2","river-3"]),
    dict(slug="garden-family-room", name="Garden Family Room", tag="Families", price=5200, unit="night",
         short="Spacious two-bed room opening onto the lawn and play area.",
         desc="Generous space for the whole family: two double beds, a study corner and a door that opens straight onto our lawn. Kids love the swings and the free-roaming farm ducks.",
         cap="4 adults + 1 child", bed="2 Double beds", size="480 sq ft",
         amen=[("leaf","Lawn access"),("snow","Air conditioning"),("shower","Hot water"),("wifi","Wi-Fi"),("tv","Smart TV"),("shield","Kid-safe grounds")],
         incl=["Welcome drink","Complimentary breakfast for four","Kids' activity kit","Bonfire access","Free parking","Early check-in (on request)"],
         imgs=["garden-1","garden-2","garden-3"]),
    dict(slug="hilltop-loft", name="Hilltop Loft Dorm", tag="Budget friendly", price=2200, unit="person",
         short="Social loft with six comfy bunks, great for backpackers and groups.",
         desc="A bright loft with six deluxe bunks, personal lockers, charging points and a wraparound balcony. The best-value way to wake up in the hills.",
         cap="Up to 6 guests", bed="6 Bunk beds", size="520 sq ft",
         amen=[("power","Charging points"),("shower","Hot water"),("wifi","Wi-Fi"),("mountain","Balcony view"),("shield","Lockers"),("coffee","Common kitchenette")],
         incl=["Breakfast","Bed linen & towel","Bonfire access","Free parking","Access to common lounge"],
         imgs=["loft-1","loft-2","loft-3"]),
]

EXPERIENCES = [
    ("sunrise","Sunrise Forest Walk","Follow our naturalist through mist-draped trails as the jungle wakes up — hornbills, giant squirrels and the smell of wet earth.","90 min · Daily"),
    ("river","River Kayak & Dip","Paddle the slow bend of the river, then cool off at a quiet swimming spot only locals know.","2 hrs · Seasonal"),
    ("fire","Bonfire & Stories","Gather round the fire with tea, grilled corn and tales of the Ghats under a sky full of stars.","Evenings · Daily"),
    ("birds","Birdwatching","Over 150 recorded species. Binoculars and a field guide are on us.","Dawn · Daily"),
    ("farm","Farm & Village Tour","Meet our farm, pick seasonal produce and learn how the village lives and cooks.","2 hrs · On request"),
    ("trail","Spice Plantation Trail","Walk through pepper, cardamom and areca groves with a guide who explains it all.","2 hrs · On request"),
]

AMENITIES = [("wifi","Wi-Fi","Fast fibre"),("car","Free parking","Secure, on site"),("food","Home-style meals","Fresh from our kitchen"),("fire","Bonfire","Every evening"),
             ("leaf","Gardens","Lawns & orchard"),("shower","Hot water","24 × 7"),("snow","AC rooms","In suites & cottages"),("power","Power backup","Never in the dark"),
             ("mountain","Valley views","From every deck"),("bird","Birdlife","150+ species"),("shield","Safe & secure","CCTV at gate, host on site"),("coffee","Tea & coffee","Always on tap")]

MEALS = [("Morning","Breakfast","Neer dosa with coconut chutney, Akki rotti, seasonal fruit, filter coffee"),
         ("Noon","Lunch","North-Karnataka thali: Jolada rotti, Ennegayi, Kosambari, rice & sambar"),
         ("Evening","Tea & Snacks","Hot pakoras, roasted corn and masala chai by the fire"),
         ("Night","Dinner","Chef's grill, Malnad-style curries, Obbattu for dessert — veg & non-veg")]

REVIEWS = [  # SAMPLE — replace with real guest reviews only
    ("Ananya R.","Bengaluru","5","Woke up to clouds below the deck. The Canopy Suite is unreal — quiet, private and spotless. The host family treated us like their own.","Oct 2026"),
    ("Mohammed & Sana","Pune","5","The bonfire night and the food were the highlights. Jolada rotti with ennegayi is something I'll dream about. Very reasonable too.","Sep 2026"),
    ("Rahul K.","Hyderabad","5","Came with two kids and parents. Everyone found something to love — walks, ducks, swings, and a peaceful room. Great value.","Aug 2026"),
    ("Priya S.","Mumbai","5","Genuinely warm hospitality. The sunrise bird walk was the best part. Easy to find, easy to relax.","Jul 2026"),
    ("Vikram & friends","Goa","4","Loft dorm was perfect for our group of six. Clean, fun, loads of charging points. Would come back for the kayaking.","Jun 2026"),
    ("Deepa N.","Hubballi","5","A short drive for us but felt a world away. Food was fresh, staff were lovely, and the river is magical.","May 2026"),
]

FAQS = [
    ("How do I book a stay?","Tap the WhatsApp button or fill the enquiry form with your dates and guests. We confirm availability and share a payment link within a few hours."),
    ("What are check-in and check-out times?","Check-in is from 12:00 PM and check-out is by 11:00 AM. Early check-in or late check-out can be arranged subject to availability."),
    ("Is food included?","Breakfast is included with all rooms. Lunch and dinner are freshly prepared on request — veg and non-veg options available."),
    ("How far are we from Dandeli town and the nearest station?","About 14 km from Dandeli town (25 min). Alur/Alnavar railway station is ~30 km and Hubballi airport ~85 km. We can arrange pickups."),
    ("Is the property family and child friendly?","Yes. Garden Family Room, kid-safe grounds, extra beds and activity kits are available."),
    ("Do you allow pets?","Well-behaved pets are welcome in the Riverside Cottage on prior request. A small cleaning fee applies."),
    ("Is there mobile network and Wi-Fi?","Major networks work at the main lawn and most rooms. Wi-Fi is available across the property, though we encourage you to unplug."),
    ("What is the cancellation policy?","Free cancellation up to 7 days before check-in. See our Policies page for full details."),
]

POLICIES = [
    ("Check-in & Check-out",["Check-in: 12:00 PM onwards","Check-out: by 11:00 AM","Early check-in / late check-out on request, subject to availability","Valid government photo ID required for all adults"]),
    ("Cancellation & Refunds",["Free cancellation up to 7 days before arrival","50% refund for 3–6 days before arrival","No refund within 72 hours or on no-show","Date changes allowed once, subject to availability"]),
    ("Booking & Payment",["A 30% advance confirms your booking","Balance payable at check-in (UPI / cash / card)","Rates are per room per night unless stated","Taxes as applicable"]),
    ("House Rules",["Quiet hours from 10:30 PM","Smoking only in designated outdoor areas","Alcohol is allowed in rooms and by the bonfire; please drink responsibly","Please respect the forest — no loud music, no littering, no feeding wildlife","Pets allowed on prior request"]),
]

DISTANCES = [("Dandeli town","14 km · 25 min"),("Kali River rafting point","6 km · 12 min"),("Syntheri Rocks","28 km · 45 min"),("Alnavar railway station","30 km · 40 min"),("Hubballi airport","85 km · 2 hrs"),("Goa (Dabolim)","170 km · 4 hrs")]

# gallery: (image key, category, caption)
GALLERY = [("hero","Property","Sunrise over the valley"),("canopy-1","Rooms","Canopy Suite"),("exp-fire","Experiences","Bonfire evenings"),("food-1","Food","Neer dosa breakfast"),
           ("river-1","Rooms","Riverside Cottage"),("nat-1","Nature","Misty mornings"),("exp-river","Experiences","River kayaking"),("garden-1","Rooms","Garden Family Room"),
           ("food-2","Food","North-Karnataka thali"),("loft-1","Rooms","Hilltop Loft"),("nat-2","Nature","Golden hour on the ridge"),("intro-2","Property","The main lawn"),
           ("exp-sunrise","Experiences","Forest walk"),("food-3","Food","Evening snacks"),("nat-3","Nature","Monsoon green"),("exp-birds","Experiences","Birdwatching")]

# =====================================================================
# SVG PLACEHOLDER ART  (swap for real photos: replace file, keep name,
# or change IMG_EXT to 'webp'/'jpg' and drop your photos in assets/img/)
# =====================================================================
IMG_EXT = "svg"
PALS = {
 "dawn":  dict(sky=("#1a2b4a","#e8827a","#ffd59a"), sun=("#fff1c9",), hills=["#7a6a8c","#4f6b7a","#2f5a55","#1a4038","#0d2a24"]),
 "gold":  dict(sky=("#3a2a4a","#f39a4a","#ffe08a"), sun=("#fff6d2",), hills=["#a8664a","#7a5a45","#4f5a3a","#2c4a2c","#12301f"]),
 "noon":  dict(sky=("#3b8fb8","#8fd0e0","#e8f6ee"), sun=("#ffffff",), hills=["#9cc7b0","#6fae8c","#3f8a63","#1f6045","#0e3b2c"]),
 "mist":  dict(sky=("#8aa6a8","#c6d5d0","#eef2ea"), sun=("#fffbe8",), hills=["#a9bfb5","#7fa396","#4f7c6b","#2c5a4c","#123a30"]),
 "dusk":  dict(sky=("#2a1f4a","#b5476a","#f6a65a"), sun=("#ffd7a0",), hills=["#6a4a6a","#4a3a5a","#2e3452","#1c2a3e","#0c1626"]),
 "night": dict(sky=("#050f1f","#0f2a3f","#1d4a52"), sun=("#e8f1ff",), hills=["#16384a","#0f2c3a","#0b2230","#081923","#050f16"]),
 "river": dict(sky=("#2f7a8a","#7fc5c0","#e9f5dc"), sun=("#ffffff",), hills=["#7fb69a","#4f9a7c","#2f7a62","#165a47","#0a3a2d"]),
}

def hill(w, h, base, amp, freq, ph):
    pts = []
    n = 48
    for i in range(n + 1):
        x = w * i / n
        y = base + amp * math.sin(freq * i / n * 2 * math.pi + ph) + amp * .45 * math.sin(freq * 2.3 * i / n * 2 * math.pi + ph * 1.7)
        pts.append("%.1f,%.1f" % (x, y))
    return "M0,%d L%s L%d,%d Z" % (h, " L".join(pts), w, h)

def trees(w, base, rnd, color, count, size):
    out = []
    for _ in range(count):
        x = rnd.uniform(0, w); s = rnd.uniform(.6, 1.3) * size; y = base + rnd.uniform(-10, 40)
        out.append('<path d="M%.0f,%.0f l%.0f,%.0f l-%.0f,0 l%.0f,%.0f l-%.0f,0 l%.0f,%.0f l-%.0f,0z" fill="%s"/>' % (
            x, y - s, s * .22, s * .4, s * .12, s * .2, s * .35, s * .2, s * .3, s * .3, s * .6, color))
    return "".join(out)

def svg_land(pal, seed, sun_xy=(.72, .32), stars=False, extra=""):
    W, H = 1600, 1000
    rnd = random.Random(seed); p = PALS[pal]
    a, b, c = p["sky"]
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">' % (W, H),
         '<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".55" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (a, b, c),
         '<radialGradient id="g"><stop offset="0" stop-color="%s" stop-opacity=".95"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (p["sun"][0], p["sun"][0]),
         '<filter id="bl"><feGaussianBlur stdDeviation="22"/></filter></defs>',
         '<rect width="%d" height="%d" fill="url(#s)"/>' % (W, H)]
    sx, sy = sun_xy[0] * W, sun_xy[1] * H
    o.append('<circle cx="%d" cy="%d" r="300" fill="url(#g)"/><circle cx="%d" cy="%d" r="62" fill="%s"/>' % (sx, sy, sx, sy, p["sun"][0]))
    if stars:
        for _ in range(90):
            o.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fff" opacity="%.2f"/>' % (rnd.uniform(0, W), rnd.uniform(0, H * .55), rnd.uniform(.8, 2.2), rnd.uniform(.3, 1)))
    for i, col in enumerate(p["hills"]):
        base = 480 + i * 110 + rnd.uniform(-20, 20)
        o.append('<path d="%s" fill="%s"/>' % (hill(W, H, base, 38 + i * 6, rnd.uniform(1, 2.2), rnd.uniform(0, 6)), col))
        if i in (1, 2):
            o.append('<ellipse cx="%d" cy="%d" rx="620" ry="44" fill="#fff" opacity=".28" filter="url(#bl)"/>' % (rnd.uniform(300, 1300), base + 60))
        if i >= 3:
            o.append(trees(W, base + 10, rnd, col, 14 + i * 4, 90 + i * 22))
    o.append(extra)
    o.append("</svg>")
    return "".join(o)

def svg_room(seed, warm="#f6b95a", wall="#241812", pal="dawn"):
    W, H = 1600, 1000
    rnd = random.Random(seed); p = PALS[pal]; a, b, c = p["sky"]
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">' % (W, H),
         '<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="#3b2619"/></linearGradient>' % wall,
         '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".6" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (a, b, c),
         '<radialGradient id="l"><stop offset="0" stop-color="%s" stop-opacity=".85"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (warm, warm),
         '<clipPath id="c"><rect x="560" y="120" width="620" height="520" rx="14"/></clipPath></defs>',
         '<rect width="%d" height="%d" fill="url(#w)"/>' % (W, H),
         '<g clip-path="url(#c)"><rect x="560" y="120" width="620" height="520" fill="url(#s)"/>']
    for i, col in enumerate(p["hills"][:4]):
        o.append('<path d="%s" fill="%s" transform="translate(560,%d)"/>' % (hill(620, 520, 300 + i * 60, 30, rnd.uniform(1, 2), rnd.uniform(0, 6)), col, 120))
    o.append('</g><rect x="560" y="120" width="620" height="520" rx="14" fill="none" stroke="#6b4a2f" stroke-width="16"/><path d="M870 120V640M560 380H1180" stroke="#6b4a2f" stroke-width="8"/>')
    o.append('<rect x="0" y="790" width="1600" height="210" fill="#4a2f1e"/><rect x="0" y="780" width="1600" height="14" fill="#2c1b11"/>')
    # bed
    o.append('<rect x="260" y="560" width="1080" height="250" rx="22" fill="#e9dcc4"/><rect x="260" y="470" width="1080" height="140" rx="26" fill="#8a4a32"/>')
    o.append('<rect x="300" y="520" width="300" height="100" rx="30" fill="#fff4df"/><rect x="640" y="520" width="300" height="100" rx="30" fill="#fff4df"/>')
    o.append('<rect x="260" y="650" width="1080" height="160" rx="18" fill="#c8523a"/><rect x="260" y="650" width="1080" height="30" fill="#e6ab3c" opacity=".85"/>')
    # lamps
    for x in (150, 1450):
        o.append('<circle cx="%d" cy="470" r="220" fill="url(#l)"/><rect x="%d" y="440" width="40" height="60" rx="8" fill="%s"/><rect x="%d" y="500" width="8" height="260" fill="#2c1b11"/>' % (x, x - 20, warm, x - 4))
    o.append("</svg>")
    return "".join(o)

def svg_food(seed, plate="#f7efe0", food="#e6ab3c", bg="#2a1810", style=0):
    W, H = 1600, 1000
    rnd = random.Random(seed)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">' % (W, H),
         '<defs><radialGradient id="b" cx=".5" cy=".5" r=".8"><stop offset="0" stop-color="#6a3b22"/><stop offset="1" stop-color="%s"/></radialGradient>' % bg,
         '<radialGradient id="p"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="%s"/></radialGradient></defs>' % plate,
         '<rect width="1600" height="1000" fill="url(#b)"/>']
    for _ in range(26):
        o.append('<rect x="%.0f" y="%.0f" width="%.0f" height="5" rx="2" fill="#000" opacity=".12" transform="rotate(%d %d 500)"/>' % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(200, 700), -8, 800))
    o.append('<ellipse cx="800" cy="560" rx="470" ry="440" fill="#000" opacity=".3"/>')
    o.append('<circle cx="800" cy="500" r="430" fill="url(#p)"/><circle cx="800" cy="500" r="330" fill="none" stroke="#d6c4a4" stroke-width="6"/>')
    if style == 0:  # dosa + chutneys
        o.append('<path d="M560 520 Q800 150 1040 520 Q800 640 560 520Z" fill="#f0c071"/><path d="M620 500 Q800 270 980 500" fill="none" stroke="#d99a45" stroke-width="10"/>')
        o.append('<circle cx="640" cy="690" r="80" fill="#fff"/><circle cx="640" cy="690" r="62" fill="#e8f0d8"/><circle cx="960" cy="690" r="80" fill="#fff"/><circle cx="960" cy="690" r="62" fill="#e86a3c"/>')
    elif style == 1:  # thali
        cols = ["#e6ab3c", "#c8523a", "#7fb069", "#f4e3b8", "#9a3c2a", "#e8d9b0"]
        for i, c in enumerate(cols):
            ang = i / len(cols) * 2 * math.pi
            x = 800 + 240 * math.cos(ang); y = 500 + 240 * math.sin(ang)
            o.append('<circle cx="%.0f" cy="%.0f" r="90" fill="#c9b690"/><circle cx="%.0f" cy="%.0f" r="74" fill="%s"/>' % (x, y, x, y, c))
        o.append('<circle cx="800" cy="500" r="110" fill="#fff"/><circle cx="800" cy="500" r="90" fill="#f4e3b8"/>')
    else:  # snacks / grill
        for i in range(7):
            x = 560 + i * 80; o.append('<rect x="%d" y="380" width="46" height="240" rx="23" fill="%s" transform="rotate(%d %d 500)"/>' % (x, food if i % 2 else "#c8523a", -14 + i * 4, x))
        o.append('<circle cx="800" cy="770" r="50" fill="#7fb069"/>')
    for _ in range(3):  # steam
        x = rnd.uniform(620, 980)
        o.append('<path d="M%.0f 260 q30 -60 0 -120 q-30 -60 0 -120" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".14"/>' % x)
    o.append("</svg>")
    return "".join(o)

def exp_extra(kind):
    if kind == "fire":
        return ('<g><ellipse cx="800" cy="860" rx="190" ry="34" fill="#000" opacity=".4"/>'
                '<path d="M800 560 C720 680 740 780 800 820 C860 780 880 680 800 560Z" fill="#f39a4a"/><path d="M800 650 C760 720 770 780 800 805 C830 780 840 720 800 650Z" fill="#ffe08a"/>'
                '<circle cx="800" cy="700" r="260" fill="#f39a4a" opacity=".18"/></g>')
    if kind == "river":
        return '<path d="M-100 1000 C300 760 700 900 1100 720 S1700 640 1700 640 L1700 1000Z" fill="#7fc5c0" opacity=".85"/><path d="M0 930 C400 840 800 960 1200 820" stroke="#fff" stroke-width="5" fill="none" opacity=".5"/>'
    if kind == "birds":
        return "".join('<path d="M%d %d q20 -22 40 0 q20 -22 40 0" stroke="#12201c" stroke-width="5" fill="none" stroke-linecap="round"/>' % (400 + i * 170, 220 + (i % 3) * 70) for i in range(6))
    return ""

def make_images():
    d = os.path.join(OUT, "assets", "img"); os.makedirs(d, exist_ok=True)
    L = {  # name -> svg
        "hero": svg_land("dawn", 1, (.66, .34), extra=""),
        "intro-1": svg_land("gold", 2, (.3, .4)),
        "intro-2": svg_land("noon", 3, (.8, .22)),
        "about": svg_land("mist", 4, (.5, .3)),
        "loc": svg_land("noon", 5),
        "nat-1": svg_land("mist", 11, (.4, .33)), "nat-2": svg_land("gold", 12, (.2, .45)), "nat-3": svg_land("river", 13, (.8, .25)),
        "exp-sunrise": svg_land("dawn", 21, (.5, .4)),
        "exp-river": svg_land("river", 22, (.7, .3), extra=exp_extra("river")),
        "exp-fire": svg_land("night", 23, (.2, .2), stars=True, extra=exp_extra("fire")),
        "exp-birds": svg_land("noon", 24, (.3, .25), extra=exp_extra("birds")),
        "exp-farm": svg_land("gold", 25, (.75, .38)),
        "exp-trail": svg_land("river", 26, (.25, .3)),
        "food-1": svg_food(31, style=0), "food-2": svg_food(32, style=1, bg="#241a10"), "food-3": svg_food(33, style=2, bg="#1d2a1a"), "food-4": svg_food(34, style=1, bg="#2a1418"),
        "canopy-1": svg_room(41, pal="dawn"), "canopy-2": svg_room(42, pal="gold"), "canopy-3": svg_land("mist", 43, (.6, .3)),
        "river-1": svg_room(51, warm="#ffd08a", wall="#1d2a24", pal="river"), "river-2": svg_land("river", 52, (.3, .3), extra=exp_extra("river")), "river-3": svg_room(53, pal="mist"),
        "garden-1": svg_room(61, warm="#ffe0a0", wall="#2a1d14", pal="noon"), "garden-2": svg_land("noon", 62, (.7, .2)), "garden-3": svg_room(63, pal="gold"),
        "loft-1": svg_room(71, warm="#ffb870", wall="#1c1e2a", pal="dusk"), "loft-2": svg_land("dusk", 72, (.4, .5), stars=True), "loft-3": svg_room(73, pal="dawn"),
    }
    for k, v in L.items():
        with open(os.path.join(d, "%s.%s" % (k, IMG_EXT)), "w", encoding="utf-8") as f:
            f.write(v)
    return list(L)

# =====================================================================
# ICONS (24px stroke icons)
# =====================================================================
ICONS = {
 "wifi":'<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r=".8"/>',
 "car":'<path d="M3 15l2-6a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l2 6v4h-3v-2H6v2H3z"/><circle cx="7.5" cy="14" r="1"/><circle cx="16.5" cy="14" r="1"/>',
 "food":'<path d="M6 3v8a2 2 0 0 0 2 2v8M10 3v8M8 3v8M17 3c-2 2-3 5-3 8h3v10"/>',
 "fire":'<path d="M12 22c-4 0-7-3-7-7 0-3 2-5 3-7 1 2 2 2 3 2 0-3 1-6 4-8 0 4 4 6 4 12 0 4-3 8-7 8z"/>',
 "leaf":'<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15zM5 19l8-8"/>',
 "shower":'<path d="M4 4h6a4 4 0 0 1 4 4M9 9l1 1M12 12l1 1M7 12l1 1M10 15l1 1M5 15l1 1"/><circle cx="14" cy="8" r="1"/>',
 "snow":'<path d="M12 2v20M4 6l16 12M20 6L4 18M9 3l3 2 3-2M9 21l3-2 3 2"/>',
 "power":'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "mountain":'<path d="M2 20l7-12 4 6 3-4 6 10z"/>',
 "bird":'<path d="M3 12c4-6 10-6 14-1l4-2-2 5c-1 5-6 8-11 6-3-1-5-4-5-8z"/><circle cx="15" cy="10" r=".7"/>',
 "shield":'<path d="M12 2l8 3v6c0 5-3 9-8 11-5-2-8-6-8-11V5z"/><path d="M9 12l2 2 4-4"/>',
 "coffee":'<path d="M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 10h2a2 2 0 0 1 0 5h-2M7 2v3M11 2v3M15 2v3"/>',
 "tv":'<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8M12 17v4"/>',
 "bed":'<path d="M3 18V7M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="1.5"/>',
 "users":'<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-4 3-6 6-6s6 2 6 6M16 5a3 3 0 0 1 0 6M18 14c2 .7 3 2.5 3 6"/>',
 "size":'<path d="M4 4h16v16H4zM4 9h5M9 4v5"/>',
 "pin":'<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
 "phone":'<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
 "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}
def ico(name, cls="ico"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, ICONS.get(name, ICONS["leaf"]))

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C9 3 3.3 8.7 3.3 15.7c0 2.5.7 4.8 2 6.8L3 29l6.7-2.2a12.7 12.7 0 0 0 6.3 1.7c7 0 12.7-5.700 12.700-12.700S23 3 16 3zm0 23.200c-2 0-3.900-.6-5.500-1.600l-.4-.2-4 1.300 1.300-3.900-.3-.4a10.400 10.400 0 1 1 8.900 4.800zm5.700-7.800c-.3-.2-1.900-.9-2.200-1s-.5-.2-.7.200-.8 1-1 1.200-.4.200-.7.100a8.500 8.500 0 0 1-4.200-3.700c-.3-.6.300-.5.900-1.700.1-.2 0-.4 0-.5l-1-2.300c-.3-.6-.5-.5-.7-.5h-.6a1.200 1.200 0 0 0-.9.400 3.700 3.700 0 0 0-1.100 2.700c0 1.600 1.100 3.100 1.300 3.300s2.300 3.500 5.600 4.900c2.100.9 2.900 1 3.900.8.600-.1 1.900-.8 2.200-1.500s.3-1.400.2-1.500-.3-.2-.6-.4z"/></svg>'

# =====================================================================
# HELPERS
# =====================================================================
def esc(s): return html.escape(str(s), quote=True)
def wa(msg): return "https://wa.me/%s?text=%s" % (S["wa"], quote(msg))
def money(n): return "₹{:,}".format(n)
def img(key, alt, cls="", lazy=True, w=1600, h=1000, fetch=False):
    attrs = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"' + (' fetchpriority="high"' if fetch else "")
    c = ' class="%s"' % cls if cls else ""
    return '<img src="/assets/img/%s.%s" alt="%s" width="%d" height="%d"%s%s>' % (key, IMG_EXT, esc(alt), w, h, c, attrs)

NAV = [("about/", "About"), ("stay/", "Stay"), ("experiences/", "Experiences"), ("gallery/", "Gallery"), ("dining/", "Dining"), ("reviews/", "Reviews"), ("contact/", "Contact")]
URLS = []

def schema_lodging():
    return {
        "@context": "https://schema.org", "@type": "LodgingBusiness", "name": S["name"], "description": S["sub"],
        "url": S["domain"] + "/", "image": S["domain"] + "/assets/img/hero." + IMG_EXT, "telephone": S["phone_raw"], "email": S["email"],
        "priceRange": "₹2,200 – ₹6,500",
        "address": {"@type": "PostalAddress", "streetAddress": S["address"], "addressRegion": "Karnataka", "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": S["lat"], "longitude": S["lng"]},
        "checkinTime": S["checkin"], "checkoutTime": S["checkout"],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": S["rating"], "reviewCount": S["reviews_count"]},
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": a[1], "value": True} for a in AMENITIES],
        "sameAs": list(S["social"].values()),
    }

def layout(path, title, desc, body, og="hero", schema=None, hero_preload=False):
    url = S["domain"] + "/" + path
    URLS.append(url)
    sch = ""
    for s in ([schema_lodging()] if path == "" else []) + (schema or []):
        sch += '<script type="application/ld+json">%s</script>\n' % json.dumps(s, ensure_ascii=False)
    gtag = ""
    if S["ga"] and "XXXX" not in S["ga"]:
        gtag = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
                '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","%s");</script>') % (S["ga"], S["ga"])
    nav = "".join('<a href="/%s">%s</a>' % (p, n) for p, n in NAV)
    enq_msg = "Hi %s! I'd like to check availability and prices." % S["name"]
    foot_links = "".join('<li><a href="/%s">%s</a></li>' % (p, n) for p, n in [("about/", "About"), ("stay/", "Stay"), ("experiences/", "Experiences"), ("gallery/", "Gallery"), ("dining/", "Dining")])
    foot_links2 = "".join('<li><a href="/%s">%s</a></li>' % (p, n) for p, n in [("location/", "Location"), ("reviews/", "Reviews"), ("faq/", "FAQ"), ("policies/", "Policies"), ("contact/", "Contact")])
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta name="theme-color" content="#0b2a24">
<meta property="og:type" content="website"><meta property="og:site_name" content="%(name)s">
<meta property="og:title" content="%(title)s"><meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s"><meta property="og:image" content="%(domain)s/assets/img/%(og)s.%(ext)s">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500&family=Manrope:wght@500;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
%(sch)s%(gtag)s
</head>
<body>
<header class="hdr"><div class="wrap">
  <a class="logo" href="/" aria-label="%(name)s home"><i>%(initial)s</i>%(short)s</a>
  <nav class="nav" aria-label="Main">%(nav)s</nav>
  <a class="btn btn-gold" href="/contact/" data-track="header_enquire">Enquire now</a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span></button>
</div></header>
<main>
%(body)s
</main>
<footer><div class="wrap">
  <div class="fgrid">
    <div><a class="logo" href="/"><i>%(initial)s</i>%(short)s</a><p style="margin-top:16px;max-width:34ch">%(tagline)s</p></div>
    <div><h4>Explore</h4><ul>%(fl)s</ul></div>
    <div><h4>Know more</h4><ul>%(fl2)s</ul></div>
    <div><h4>Reach us</h4><ul>
      <li><a href="tel:%(praw)s">%(phone)s</a></li><li><a href="mailto:%(email)s">%(email)s</a></li><li>%(addr)s</li>
      <li><a href="%(ig)s" rel="noopener" target="_blank">Instagram</a> · <a href="%(fb)s" rel="noopener" target="_blank">Facebook</a></li></ul></div>
  </div>
  <div class="fbot"><span>© <span id="yr">2026</span> %(name)s. All rights reserved.</span><span>Check-in %(ci)s · Check-out %(co)s</span></div>
</div></footer>
<div class="wa-menu" id="wam">
  <a href="%(wa1)s" target="_blank" rel="noopener" data-track="wa_availability">Check availability</a>
  <a href="%(wa2)s" target="_blank" rel="noopener" data-track="wa_price">Ask about prices</a>
  <a href="%(wa3)s" target="_blank" rel="noopener" data-track="wa_rooms">Room information</a>
  <a href="%(wa4)s" target="_blank" rel="noopener" data-track="wa_booking">Booking question</a>
</div>
<a class="wa-float" href="%(wa1)s" aria-label="Chat on WhatsApp" aria-controls="wam">%(wasvg)s<span>Chat with us</span></a>
<script>window.SITE={name:%(namejs)s,wa:"%(wanum)s"};</script>
<script src="/assets/js/main.js" defer></script>
</body></html>""" % dict(
        title=esc(title), desc=esc(desc), url=url, name=esc(S["name"]), domain=S["domain"], og=og, ext=IMG_EXT, sch=sch, gtag=gtag,
        initial=esc(S["name"][0]), short=esc(S["short"]), nav=nav, body=body, tagline=esc(S["tagline"]), fl=foot_links, fl2=foot_links2,
        praw=S["phone_raw"], phone=esc(S["phone"]), email=esc(S["email"]), addr=esc(S["address"]), ig=S["social"]["instagram"], fb=S["social"]["facebook"],
        ci=S["checkin"], co=S["checkout"],
        wa1=wa(enq_msg), wa2=wa("Hi! Could you share your room rates for my dates?"), wa3=wa("Hi! I'd like details about your rooms and what's included."),
        wa4=wa("Hi! I have a question about booking."), wasvg=WA_SVG, namejs=json.dumps(S["name"]), wanum=S["wa"])

def write(path, content):
    p = os.path.join(OUT, path, "index.html") if not path.endswith((".xml", ".txt", ".html")) else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def phero(title, sub, crumbs, bg):
    cr = '<div class="crumbs"><a href="/">Home</a> / %s</div>' % crumbs
    return '<section class="phero" style="padding-bottom:60px">%s<div class="wrap">%s<h1>%s</h1><p>%s</p></div></section>' % (img(bg, "", "bg", lazy=False, fetch=True), cr, title, sub)

def cta_block(title="Your quiet corner of the Ghats is waiting.", p="Tell us your dates and we'll check availability within a few hours — no payment needed to enquire."):
    return """<section class="cta"><div class="wrap rv">
<h2>%s</h2><p>%s</p>
<div class="cta-row"><a class="btn btn-gold" href="/contact/" data-track="final_cta_enquire">Check availability</a>
<a class="btn btn-wa" href="%s" target="_blank" rel="noopener" data-track="final_cta_wa">%s WhatsApp us</a>
<a class="btn btn-ghost" href="tel:%s">Call %s</a></div></div></section>""" % (title, p, wa("Hi! I'd like to check availability."), WA_SVG, S["phone_raw"], esc(S["phone"]))

def room_card(r):
    ams = "".join("<span>%s</span>" % esc(a[1]) for a in r["amen"][:4])
    price = '<div class="price">%s <small>/ %s</small></div>' % (money(r["price"]), r["unit"])
    return """<article class="rcard rv"><a class="ph" href="/stay/%(slug)s/" aria-label="View %(name)s">%(img)s<span class="tag">%(tag)s</span>%(price)s</a>
<div class="bd"><h3>%(name)s</h3><p>%(short)s</p>
<div class="meta"><span>%(i1)s %(cap)s</span><span>%(i2)s %(bed)s</span></div>
<div class="am-mini">%(ams)s</div>
<div class="acts"><a class="btn btn-line" href="/stay/%(slug)s/">View room</a>
<a class="btn btn-gold" href="%(wa)s" target="_blank" rel="noopener" data-track="room_enquire_%(slug)s">Enquire</a></div></div></article>""" % dict(
        slug=r["slug"], name=esc(r["name"]), img=img(r["imgs"][0], r["name"] + " at " + S["name"], w=800, h=600), tag=esc(r["tag"]), price=price, short=esc(r["short"]),
        i1=ico("users"), i2=ico("bed"), cap=esc(r["cap"]), bed=esc(r["bed"]), ams=ams, wa=wa("Hi! I'd like to enquire about the %s." % r["name"]))

def rev_card(rv, i):
    n, c, st, t, dt = rv
    return '<article class="rev"><div class="stars" aria-label="%s out of 5">%s</div><p>%s</p><div class="who"><div class="av">%s</div><div><b>%s</b><small>%s · %s</small></div></div></article>' % (
        st, "★" * int(st) + "☆" * (5 - int(st)), esc(t), esc(n[0]), esc(n), esc(c), esc(dt))

def exp_card(i, e):
    k, t, d, tm = e
    return '<article class="xcard rv d%d">%s<div class="in"><div class="n">0%d</div><h3>%s</h3><p>%s</p><span class="time">%s</span></div></article>' % (
        i % 3 + 1, img("exp-" + k, t + " at " + S["name"], w=800, h=1000), i + 1, esc(t), esc(d), esc(tm))

def am_grid(items):
    return '<div class="amgrid">%s</div>' % "".join(
        '<div class="am rv"><div class="ic">%s</div><b>%s</b><small>%s</small></div>' % (ico(a[0], ""), esc(a[1]), esc(a[2])) for a in items)

def gallery_html(items, cats=True):
    cs = ["all"] + sorted({g[1] for g in items})
    f = '<div class="filters center">%s</div>' % "".join('<button class="fbtn%s" data-cat="%s">%s</button>' % (" on" if c == "all" else "", c, c.title()) for c in cs) if cats else ""
    figs = "".join('<figure data-cat="%s">%s<figcaption>%s</figcaption></figure>' % (g[1], img(g[0], g[2] + " — " + S["name"], w=800, h=600), esc(g[2])) for g in items)
    lb = '<dialog class="lb"><button class="x" aria-label="Close">✕</button><button class="pv" aria-label="Previous">‹</button><button class="nx" aria-label="Next">›</button><div><img alt="" src=""><p></p></div></dialog>'
    return f + '<div class="masonry">%s</div>%s' % (figs, lb)

def meals_html(light=False):
    return '<div class="menu-list">%s</div>' % "".join('<div class="mi rv"><div class="t">%s</div><div><b>%s</b><small>%s</small></div></div>' % (esc(a), esc(b), esc(c)) for a, b, c in MEALS)

def map_html():
    return '<iframe title="Map showing %s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.openstreetmap.org/export/embed.html?bbox=%s%%2C%s%%2C%s%%2C%s&layer=mapnik&marker=%s%%2C%s"></iframe>' % (
        esc(S["name"]), S["lng"] - .08, S["lat"] - .05, S["lng"] + .08, S["lat"] + .05, S["lat"], S["lng"])

def dist_html():
    return '<div class="dist">%s</div>' % "".join("<div>%s<span>%s</span></div>" % (esc(a), esc(b)) for a, b in DISTANCES)

def enquiry_form(label="contact_form", rooms=True):
    opts = "".join('<option>%s</option>' % esc(r["name"]) for r in ROOMS)
    return """<form class="enq" data-enquiry="%s">
<h3>Send an enquiry</h3>
<label>Your name<input name="name" required autocomplete="name" placeholder="Full name"></label>
<label>Phone<input name="phone" type="tel" required autocomplete="tel" placeholder="+91 …"></label>
<label>Check-in<input name="checkin" type="date" required></label>
<label>Check-out<input name="checkout" type="date" required></label>
<label>Guests<select name="guests"><option>2 guests</option><option>1 guest</option><option>3 guests</option><option>4 guests</option><option>5–6 guests</option><option>7+ guests</option></select></label>
<label>Room<select name="room"><option>Not sure yet</option>%s</select></label>
<label class="full">Message<textarea name="message" placeholder="Any special requests, occasions, food preferences…"></textarea></label>
<div class="full"><button class="btn btn-wa" type="submit">%s Send on WhatsApp</button></div>
<p class="note">This opens WhatsApp with your details pre-filled so we can reply fast. Prefer email? Write to <a href="mailto:%s"><b>%s</b></a>.</p>
</form>""" % (label, opts, WA_SVG, S["email"], esc(S["email"]))

# =====================================================================
# PAGES
# =====================================================================
def page_home():
    marq = "".join("<span>%s</span>" % t for t in ["Misty mornings", "Private cottages", "Bonfire nights", "Malnad cuisine", "River & forest trails", "Birdsong alarm clocks", "Family-run hospitality"] * 2)
    rooms = "".join(room_card(r) for r in ROOMS)
    xps = "".join(exp_card(i, e) for i, e in enumerate(EXPERIENCES))
    revs = "".join(rev_card(r, i) for i, r in enumerate(REVIEWS))
    gal = "".join('<figure data-cat="x">%s<figcaption>%s</figcaption></figure>' % (img(g[0], g[2] + " — " + S["name"], w=800, h=600), esc(g[2])) for g in GALLERY[:9])
    body = """
<section class="hero" style="padding-bottom:50px">%(hero)s<div class="mist"></div><div class="mist m2"></div>
<div class="wrap">
  <div class="hero-badge"><span><b>★ %(rating)s</b> · %(rc)s+ guest reviews · Dandeli, Karnataka</span></div>
  <h1>Wake up <em>above</em> the clouds.</h1>
  <p class="sub">%(sub)s</p>
  <div class="cta-row">
    <a class="btn btn-gold" href="/contact/" data-track="hero_enquire">Check availability →</a>
    <a class="btn btn-wa" href="%(wa)s" target="_blank" rel="noopener" data-track="hero_wa">%(wasvg)s WhatsApp us</a>
    <a class="btn btn-ghost" href="/stay/">Explore stays</a>
  </div>
  <form class="qbar" data-enquiry="hero_quickbar" aria-label="Quick enquiry">
    <label>Check-in<input type="date" name="checkin" required></label>
    <label>Check-out<input type="date" name="checkout" required></label>
    <label>Guests<select name="guests"><option>2 guests</option><option>1 guest</option><option>3 guests</option><option>4 guests</option><option>5–6 guests</option><option>7+ guests</option></select></label>
    <label>Stay<select name="room"><option>Any room</option>%(opts)s</select></label>
    <button class="btn btn-gold" type="submit">Enquire</button>
  </form>
</div><div class="scroll-cue">Scroll</div></section>

<div class="marq" aria-hidden="true"><div class="track">%(marq)s</div></div>

<section><div class="wrap split">
  <div class="collage rv"><div class="a">%(i1)s</div><div class="b">%(i2)s</div><div class="stamp"><div><b>%(rating)s★</b>guest<br>rating</div></div></div>
  <div class="rv d1"><span class="eyebrow">Welcome to %(short)s</span>
    <h2 class="h2">A slow, soulful escape in the <em class="g">Western Ghats</em></h2>
    <p class="lead">%(name)s is a family-run forest homestay tucked into the hills near Dandeli. Four hand-built stays, a river at the foot of the property, and hosts who greet you with chai and stay for the stories.</p>
    <p class="lead" style="margin-top:14px">Made for couples, families and friends who want real quiet — good food, clean rooms, and nature that doesn't need a filter.</p>
    <div class="chips"><span class="chip">Couples</span><span class="chip">Families</span><span class="chip">Friend groups</span><span class="chip">Remote workers</span><span class="chip">Nature lovers</span></div>
    <div class="stats"><div class="stat"><b data-count="4" data-suffix="">4</b><small>Unique stays</small></div><div class="stat"><b data-count="150" data-suffix="+">150+</b><small>Bird species</small></div><div class="stat"><b data-count="%(rating)s">%(rating)s</b><small>Average rating</small></div></div>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="center rv"><span class="eyebrow">Stay</span><h2 class="h2">Pick your <em class="g">hideaway</em></h2><p class="lead">Four ways to sleep in the forest — from a treetop suite to a social loft. Rates from %(pf)s.</p></div>
  <div class="rooms">%(rooms)s</div>
  <p class="center" style="margin-top:44px;position:relative"><a class="btn btn-ghost" href="/stay/">See all stays</a></p>
</div></section>

<section><div class="wrap">
  <div class="center rv"><span class="eyebrow">Experiences</span><h2 class="h2">Days that feel like <em class="g">stories</em></h2><p class="lead">Every stay comes with a little adventure. Join one, join all, or do absolutely nothing in a hammock.</p></div>
  <div class="xp">%(xps)s</div>
  <p class="center" style="margin-top:40px"><a class="btn btn-line" href="/experiences/">All experiences</a></p>
</div></section>

<section style="background:#fff"><div class="wrap">
  <div class="center rv"><span class="eyebrow">Amenities</span><h2 class="h2">Comforts, <em class="g">thoughtfully</em> done</h2></div>
  %(ams)s
</div></section>

<section><div class="wrap">
  <div class="center rv"><span class="eyebrow">Gallery</span><h2 class="h2">A peek into <em class="g">paradise</em></h2></div>
  <div class="masonry" style="margin-top:44px">%(gal)s</div>
  <p class="center" style="margin-top:30px"><a class="btn btn-dark" href="/gallery/">Open full gallery</a></p>
</div></section>

<section class="dark"><div class="wrap food">
  <div class="foodimgs rv">%(f1)s%(f2)s%(f3)s%(f4)s</div>
  <div class="rv d1"><span class="eyebrow">Dining</span><h2 class="h2">Malnad flavours, <em class="g">cooked with love</em></h2>
  <p class="lead">Our kitchen team cooks fresh, local and seasonal — from crisp neer dosa at sunrise to a grilled dinner by the fire.</p>%(meals)s
  <p style="margin-top:28px"><a class="btn btn-gold" href="/dining/">See dining details</a></p></div>
</div></section>

<section><div class="wrap">
  <div class="center rv"><span class="eyebrow">Guest love</span><h2 class="h2">Loved by <em class="g">%(rc)s+ guests</em></h2>
  <div class="rating-big"><b>%(rating)s</b><div><div class="stars">★★★★★</div><small>Average rating</small></div></div></div>
  <div class="rv-wrap">%(revs)s</div>
  <p class="center"><a class="btn btn-line" href="/reviews/">Read more reviews</a></p>
</div></section>

<section style="background:#fff"><div class="wrap">
  <div class="center rv"><span class="eyebrow">Location</span><h2 class="h2">Easy to reach, <em class="g">hard to leave</em></h2><p class="lead">%(addr)s</p></div>
  <div class="loc"><div class="map rv">%(map)s</div><div class="rv d1">%(dist)s
  <p style="margin-top:22px"><a class="btn btn-dark" href="https://www.google.com/maps/search/?api=1&query=%(lat)s,%(lng)s" target="_blank" rel="noopener" data-track="directions">Get directions</a></p></div></div>
</div></section>

%(cta)s
""" % dict(hero=img("hero", "Sunrise over misty forested hills at %s" % S["name"], "bg", lazy=False, fetch=True), rating=S["rating"], rc=S["reviews_count"], sub=esc(S["sub"]),
           wa=wa("Hi! I'd like to check availability."), wasvg=WA_SVG, opts="".join("<option>%s</option>" % esc(r["name"]) for r in ROOMS), marq=marq,
           i1=img("intro-1", "Cottage garden at golden hour", w=800, h=800), i2=img("intro-2", "Lawn and valley view", w=800, h=800), short=esc(S["short"]), name=esc(S["name"]),
           pf=S["price_from"], rooms=rooms, xps=xps, ams=am_grid(AMENITIES), gal=gal,
           f1=img("food-1", "Neer dosa breakfast", w=600, h=600), f2=img("food-2", "North Karnataka thali", w=600, h=600), f3=img("food-3", "Evening snacks", w=600, h=600), f4=img("food-4", "Dinner thali", w=600, h=600),
           meals=meals_html(), revs=revs, addr=esc(S["address"]), map=map_html(), dist=dist_html(), lat=S["lat"], lng=S["lng"], cta=cta_block())
    write("", layout("", "%s — Forest Homestay in Dandeli, Karnataka" % S["name"], "Private cottages, bonfire nights and home-cooked Malnad food at %s, a family-run forest homestay in Dandeli. Check availability on WhatsApp." % S["name"], body))

def page_about():
    body = phero("Our story", "A family, a forest and a simple idea: hospitality should feel like coming home.", "About", "about") + """
<section><div class="wrap split">
 <div class="rv"><span class="eyebrow">Who we are</span><h2 class="h2">Rooted in the hills, <em class="g">raised on hospitality</em></h2>
 <p class="lead">%(name)s began as a family farmhouse. Guests kept asking to stay, so we built one cottage, then another — always using local wood, stone and the hands of village craftspeople.</p>
 <p class="lead" style="margin-top:14px">Today we remain small on purpose. You'll meet the people who built the place, eat what we grow and cook, and leave with stories rather than souvenirs.</p></div>
 <div class="collage rv d1"><div class="a">%(i1)s</div><div class="b">%(i2)s</div></div>
</div></section>
<section class="dark"><div class="wrap"><div class="center rv"><span class="eyebrow">Philosophy</span><h2 class="h2">Three promises</h2></div>
<div class="revgrid" style="position:relative">
<div class="rev rv" style="color:var(--ink)"><h3>Slow by design</h3><p>No schedules, no crowds. Rooms are few so the forest stays loud and the world stays quiet.</p></div>
<div class="rev rv d1" style="color:var(--ink)"><h3>Local first</h3><p>Local builders, local produce, local guides — your stay supports the village around us.</p></div>
<div class="rev rv d2" style="color:var(--ink)"><h3>Gently on nature</h3><p>Solar water heating, rainwater harvesting and zero single-use plastic in the rooms.</p></div>
</div></div></section>
%(cta)s""" % dict(name=esc(S["name"]), i1=img("about", "The retreat among hills", w=800, h=800), i2=img("intro-1", "Evening light on the farm", w=800, h=800), cta=cta_block())
    write("about", layout("about/", "About %s — Our Story & Hospitality Philosophy" % S["short"], "Meet the family behind %s: a small, local-first forest homestay in Dandeli built on warm hospitality and sustainable living." % S["name"], body, og="about"))

def page_stay():
    body = phero("Stay with us", "Four distinctive ways to sleep in the forest. Rates from %s." % S["price_from"], "Stay", "canopy-3") + """
<section><div class="wrap"><div class="rooms" style="margin-top:0">%s</div></div></section>
<section class="dark"><div class="wrap center rv"><span class="eyebrow">Included with every stay</span><h2 class="h2">Little extras, <em class="g">no extra cost</em></h2>
<p class="lead">Welcome drink, daily breakfast, bonfire access, free parking and a guided morning walk are part of the stay.</p></div></section>
%s""" % ("".join(room_card(r) for r in ROOMS), cta_block())
    write("stay", layout("stay/", "Rooms & Cottages — Stay at %s, Dandeli" % S["short"], "Browse the Canopy Suite, Riverside Cottage, Garden Family Room and Hilltop Loft at %s. Rates from %s per night." % (S["name"], S["price_from"]), body, og="canopy-3"))

def page_room(r):
    th = "".join('<button class="%s" aria-label="Photo %d"><img src="/assets/img/%s.%s" alt="%s photo %d" width="400" height="250" loading="lazy"></button>' % ("on" if i == 0 else "", i + 1, k, IMG_EXT, esc(r["name"]), i + 1) for i, k in enumerate(r["imgs"]))
    am = "".join('<div class="am rv"><div class="ic">%s</div><b>%s</b></div>' % (ico(a[0], ""), esc(a[1])) for a in r["amen"])
    inc = "".join("<li>%s</li>" % esc(i) for i in r["incl"])
    others = "".join(room_card(o) for o in ROOMS if o["slug"] != r["slug"])[:]
    body = phero(esc(r["name"]), r["short"], '<a href="/stay/">Stay</a> / %s' % esc(r["name"]), next(k for k in r["imgs"] if k in ("canopy-3","river-2","garden-2","loft-2"))) + """
<section><div class="wrap rm">
<div><div class="rg-main">%(main)s</div><div class="rg-th">%(th)s</div>
<h2 class="h3 h2" style="font-size:2rem">About this stay</h2><p class="lead">%(desc)s</p>
<h2 class="h3 h2" style="font-size:2rem;margin-top:40px">Room amenities</h2><div class="amgrid" style="margin-top:20px">%(am)s</div>
<h2 class="h3 h2" style="font-size:2rem;margin-top:40px">What's included</h2><ul class="ticks">%(inc)s</ul></div>
<aside class="booking"><div class="amt">%(price)s <small>/ %(unit)s</small></div><small style="opacity:.7">Taxes extra · 30%% advance confirms</small>
<div class="spec"><div>%(i1)s<b>%(cap)s</b>Capacity</div><div>%(i2)s<b>%(bed)s</b>Bed</div><div>%(i3)s<b>%(size)s</b>Size</div><div>%(i4)s<b>%(ci)s</b>Check-in</div></div>
<a class="btn btn-gold" href="%(wa)s" target="_blank" rel="noopener" data-track="room_book_%(slug)s">Book / Enquire on WhatsApp</a>
<a class="btn btn-ghost" href="/contact/" data-track="room_form_%(slug)s">Send enquiry form</a>
<a class="btn btn-ghost" href="tel:%(praw)s">Call %(phone)s</a></aside>
</div></section>
<section class="dark"><div class="wrap"><div class="center rv"><span class="eyebrow">More stays</span><h2 class="h2">Explore other rooms</h2></div><div class="rooms">%(others)s</div></div></section>
%(cta)s""" % dict(main=img(r["imgs"][0], "%s at %s" % (r["name"], S["name"]), lazy=False, w=1200, h=750), th=th, desc=esc(r["desc"]), am=am, inc=inc, price=money(r["price"]), unit=r["unit"],
                  i1=ico("users"), i2=ico("bed"), i3=ico("size"), i4=ico("clock"), cap=esc(r["cap"]), bed=esc(r["bed"]), size=esc(r["size"]), ci=S["checkin"],
                  wa=wa("Hi! I'd like to book the %s. Is it available?" % r["name"]), slug=r["slug"], praw=S["phone_raw"], phone=esc(S["phone"]), others=others, cta=cta_block())
    sch = [{"@context": "https://schema.org", "@type": "HotelRoom", "name": r["name"], "description": r["desc"], "bed": {"@type": "BedDetails", "typeOfBed": r["bed"]},
            "occupancy": {"@type": "QuantitativeValue", "description": r["cap"]}, "image": "%s/assets/img/%s.%s" % (S["domain"], r["imgs"][0], IMG_EXT),
            "offers": {"@type": "Offer", "price": r["price"], "priceCurrency": "INR"}}]
    write("stay/" + r["slug"], layout("stay/%s/" % r["slug"], "%s — %s" % (r["name"], S["name"]), "%s %s From %s per %s." % (r["name"], r["short"], money(r["price"]), r["unit"]), body, og=r["imgs"][0], schema=sch))

def page_exp():
    body = phero("Experiences", "Forest walks, river days, fireside nights — pick your adventure.", "Experiences", "exp-sunrise") + """
<section><div class="wrap"><div class="xp" style="margin-top:0">%s</div></div></section>%s""" % ("".join(exp_card(i, e) for i, e in enumerate(EXPERIENCES)), cta_block("Ready to plan your adventure?"))
    write("experiences", layout("experiences/", "Experiences & Activities — %s" % S["short"], "Sunrise forest walks, river kayaking, bonfire nights, birdwatching and village tours at %s, Dandeli." % S["name"], body, og="exp-sunrise"))

def page_gallery():
    body = phero("Gallery", "Browse the property, rooms, food and the wilderness around us.", "Gallery", "nat-1") + '<section><div class="wrap">%s</div></section>%s' % (gallery_html(GALLERY + [("nat-1", "Nature", "Valley fog"), ("loft-2", "Rooms", "Loft balcony at dusk"), ("food-4", "Food", "Dinner spread")]), cta_block())
    write("gallery", layout("gallery/", "Photo Gallery — %s" % S["short"], "See photos of the rooms, food, experiences and surroundings at %s in Dandeli, Karnataka." % S["name"], body, og="nat-1"))

def page_dining():
    body = phero("Dining", "Fresh, local, home-style — cooked to order and best enjoyed slowly.", "Dining", "food-2") + """
<section class="light"><div class="wrap food">
<div class="foodimgs rv">%s%s%s%s</div>
<div class="rv d1"><span class="eyebrow">Our kitchen</span><h2 class="h2">From farm to <em class="g">your plate</em></h2><p class="lead">Breakfast is included with every room. Lunch and dinner are made fresh on request — please tell us your preferences when you book.</p>%s
<p class="lead" style="margin-top:20px"><b>Veg &amp; non-veg</b> available · Jain, vegan and kids' options on request · Packed meals for treks.</p></div>
</div></section>%s""" % (img("food-1", "Neer dosa", w=600, h=600), img("food-2", "Thali", w=600, h=600), img("food-3", "Snacks", w=600, h=600), img("food-4", "Dinner", w=600, h=600), meals_html(True), cta_block("Hungry yet?", "Tell us your food preferences and we'll plan the menu around you."))
    write("dining", layout("dining/", "Dining & Food — %s" % S["short"], "Home-style Malnad and North-Karnataka meals at %s: neer dosa breakfasts, thalis, bonfire snacks and grilled dinners." % S["name"], body, og="food-2"))

def page_location():
    body = phero("Find us", S["address"], "Location", "loc") + """
<section><div class="wrap"><div class="loc" style="margin-top:0"><div class="map">%s</div><div>%s
<p style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-dark" href="https://www.google.com/maps/search/?api=1&query=%s,%s" target="_blank" rel="noopener" data-track="directions">Open in Google Maps</a>
<a class="btn btn-wa" href="%s" target="_blank" rel="noopener" data-track="loc_wa">%s Ask for pickup</a></p></div></div>
<div class="pcard" style="margin-top:36px"><h3>How to reach us</h3><ul><li><b>By road:</b> From Dandeli town, take Kulgi Road for ~14 km. Look for our signboard after Ambikanagar.</li><li><b>By train:</b> Alnavar Junction (~30 km). We can arrange a pickup.</li><li><b>By air:</b> Hubballi airport (~85 km), Goa Dabolim (~170 km).</li><li><b>Parking:</b> Free, secure parking on the property.</li></ul></div></div></section>%s""" % (
        map_html(), dist_html(), S["lat"], S["lng"], wa("Hi! I'd like to arrange a pickup."), WA_SVG, cta_block())
    write("location", layout("location/", "Location & Directions — %s" % S["short"], "Address, map and directions to %s near Dandeli, Karnataka. Distances from Dandeli, Alnavar, Hubballi and Goa." % S["name"], body, og="loc"))

def page_reviews():
    body = phero("Guest reviews", "Honest words from people who've stayed with us.", "Reviews", "nat-2") + """
<section><div class="wrap"><div class="center rv"><div class="rating-big"><b>%s</b><div><div class="stars">★★★★★</div><small>%s+ reviews</small></div></div></div>
<div class="revgrid">%s</div></div></section>%s""" % (S["rating"], S["reviews_count"], "".join(rev_card(r, i) for i, r in enumerate(REVIEWS)), cta_block("Be our next happy guest."))
    write("reviews", layout("reviews/", "Guest Reviews — %s" % S["short"], "Read what guests say about %s: rated %s from %s+ reviews." % (S["name"], S["rating"], S["reviews_count"]), body, og="nat-2"))

def page_faq():
    qs = "".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in FAQS)
    body = phero("FAQ", "Quick answers to common questions.", "FAQ", "nat-3") + '<section><div class="wrap"><div class="faq">%s</div></div></section>%s' % (qs, cta_block("Still have a question?", "Message us on WhatsApp — we reply fast."))
    sch = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}]
    write("faq", layout("faq/", "FAQ — Booking, Check-in, Food & More | %s" % S["short"], "Answers about booking, check-in times, meals, pets, pickups and cancellations at %s." % S["name"], body, og="nat-3", schema=sch))

def page_contact():
    body = phero("Let's plan your stay", "Tell us your dates — we'll reply within a few hours.", "Contact", "intro-2") + """
<section><div class="wrap"><div class="contact"><div class="cinfo">
<a class="ci" href="%s" target="_blank" rel="noopener"><div class="ic">%s</div><div><small>WhatsApp</small><b>Chat now · %s</b></div></a>
<a class="ci" href="tel:%s"><div class="ic">%s</div><div><small>Call</small><b>%s</b></div></a>
<a class="ci" href="mailto:%s"><div class="ic">%s</div><div><small>Email</small><b>%s</b></div></a>
<div class="ci"><div class="ic">%s</div><div><small>Address</small><b>%s</b></div></div>
<div class="map" style="min-height:260px">%s</div></div>%s</div></div></section>""" % (
        wa("Hi! I'd like to check availability."), ico("phone", ""), esc(S["phone"]), S["phone_raw"], ico("phone", ""), esc(S["phone"]), S["email"], ico("mail", ""), esc(S["email"]),
        ico("pin", ""), esc(S["address"]), map_html(), enquiry_form("contact_form"))
    write("contact", layout("contact/", "Contact & Enquiry — %s" % S["short"], "Call, WhatsApp, email or send an enquiry to %s. Check availability for your dates." % S["name"], body, og="intro-2"))

def page_policies():
    cards = "".join('<div class="pcard rv"><h3>%s</h3><ul>%s</ul></div>' % (esc(t), "".join("<li>%s</li>" % esc(i) for i in items)) for t, items in POLICIES)
    body = phero("Policies", "Check-in, cancellation, payment and house rules.", "Policies", "about") + '<section><div class="wrap"><div class="pol" style="margin-top:0">%s</div></div></section>%s' % (cards, cta_block("Questions about a policy?", "Just ask — we're flexible where we can be."))
    write("policies", layout("policies/", "Policies — Check-in, Cancellation & House Rules | %s" % S["short"], "Check-in/out times, cancellation and refund policy, payment terms and house rules at %s." % S["name"], body, og="about"))

def page_404():
    body = phero("Lost in the woods?", "That page wandered off. Let's get you back to the trail.", "404", "nat-1") + '<section><div class="wrap center"><a class="btn btn-gold" href="/">Back to home</a></div></section>'
    html_ = layout("404.html", "Page not found — %s" % S["name"], "Page not found.", body)
    URLS.pop()
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f: f.write(html_)

def seo_files():
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("  <url><loc>%s</loc></url>\n" % u for u in URLS) + "</urlset>\n"
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f: f.write(sm)
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f: f.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % S["domain"])
    fav = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e6ab3c"/><stop offset="1" stop-color="#c8523a"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#a)"/><path d="M8 48l16-24 10 14 8-10 14 20z" fill="#0b2a24"/></svg>'
    with open(os.path.join(OUT, "assets", "img", "favicon.svg"), "w") as f: f.write(fav)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    shutil.copytree(os.path.join(HERE, "assets", "css"), os.path.join(OUT, "assets", "css"))
    shutil.copytree(os.path.join(HERE, "assets", "js"), os.path.join(OUT, "assets", "js"))
    make_images()
    page_home(); page_about(); page_stay()
    for r in ROOMS: page_room(r)
    page_exp(); page_gallery(); page_dining(); page_location(); page_reviews(); page_faq(); page_contact(); page_policies(); page_404()
    seo_files()
    print("Built %d pages -> %s" % (len(URLS), OUT))

if __name__ == "__main__":
    main()
