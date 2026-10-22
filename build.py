#!/usr/bin/env python3
"""
jrresales.com site builder.

Everything that changes lives in one place: SITE (brand, contact, links)
and CONTENT (page text, listings, reviews). Run `python3 build.py` and the
finished site lands in /docs, ready for GitHub Pages.

To switch from NorthGroup to HomeSmart later: edit the BRAND block below
and rebuild. Nothing else changes.
"""
import json, os, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

# ---------------------------------------------------------------- SITE SETUP
BRAND = {
    "brokerage": "NorthGroup Real Estate",
    "brokerage_note": "NorthGroup Real Estate is now part of HomeSmart.",
    "brokerage_note_es": "NorthGroup Real Estate ahora es parte de HomeSmart.",
    "office": "148 Milestone Way, Suite D, Greenville, SC 29615",
    "broker_in_charge": "Rick Markowski, Broker-in-Charge",
    "brokerage_site": "https://jrgrimaldo.northgroupre.com",
}

SITE = {
    "domain": "jrresales.com",
    "agent": "J.R. Grimaldo",
    "title_tag": "J.R. Grimaldo, REALTOR® – Upstate SC",
    "license": "SC License #95641",
    "phone": "864-381-2326",
    "phone_tel": "+18643812326",
    "email": "jr@jrresales.com",
    "home_town": "Landrum, SC",
    "areas": ["Landrum", "Campobello", "Inman", "Greer", "Taylors",
              "Greenville", "Spartanburg", "Simpsonville", "Fountain Inn",
              "Travelers Rest"],
    # Leave empty to send the valuation form by the visitor's own email app.
    # Paste a Formspree form ID (e.g. "xabcdefg") to send through Formspree.
    "formspree_id": "mdeenynr",
    "review_page": "https://jaygrimaldo.github.io/reviews",
    "valuation_domain": "jrrevalues.com",
    "facebook": "",
}

# ------------------------------------------------------------------ CONTENT
LISTINGS = [
    {
        "address": "300 Colony Rd, Travelers Rest, SC 29690",
        "price": "$309,999",
        "line": "Full brick ranch on a corner lot in Points North, built in 1978. Three bedrooms, two full baths, all on one level. USDA area: qualified buyers may put $0 down.",
        "mls": "Greenville MLS 1605021",
        "link": "https://jrgrimaldo.northgroupre.com/property/63-1605021-300-colony-road-travelers-rest-SC-29690",
        "photo": "300-colony-rd.jpg",
    },
    {
        "address": "207 Penrith Ct, Simpsonville, SC 29681",
        "price": "$352,999",
        "line": "Investor opportunity: leased through May 31, 2027, so it earns rent from day one. Four bedrooms, two and a half baths, about 1,980 sq ft on a cul-de-sac in Villages at Windsor. New roof in late 2024.",
        "mls": "Greenville MLS 1567172",
        "link": "https://jrgrimaldo.northgroupre.com/property/63-1567172-207-penrith-court-simpsonville-SC-29681",
        "photo": "207-penrith-ct.jpg",
    },
]

# Newest or strongest first. No closing dates shown. "role" says which side
# J.R. represented. Only use photos from J.R.'s own listings; a home he sold
# for a buyer gets no photo unless J.R. took it himself.
SOLD = [
    {"address": "248 Page Creek Blvd, Landrum, SC 29356", "price": "Sold for $392,500",
     "role": "Sold for the seller",
     "line": "Three bedrooms, two baths in Landrum.",
     "photo": "248-page-creek-blvd.jpg"},
    {"address": "420 Cloverdale Ln, Simpsonville, SC 29681", "price": "Sold for $175,000",
     "role": "Sold for the seller",
     "line": "Three bedrooms, one and a half baths in Simpsonville.",
     "photo": "420-cloverdale-ln.jpg"},
    {"address": "304 Talbert Trail, Landrum, SC 29356", "price": "Sold for $290,000",
     "role": "Represented the buyer",
     "line": "Three bedrooms, two baths in Landrum.",
     "photo": "304-talbert-trail.jpg"},  # owner's own photo, sent to J.R. 10/22/2026
]

# Google reviews (Kerri H., "Knight Vision", Jeff D.) copied word for word from
# J.R.'s Google Business Profile 10/22/2026. Others copied from the NorthGroup testimonials page (same four as the HomeSmart
# "What My Clients Say" page). Slava's uses the HomeSmart wording, which
# fixes a typo in the NorthGroup copy.
# More closed sales from J.R.'s dotloop (read 10/22/2026), newest first.
# The three with photos above are not repeated here. Closing dates kept in the
# comment only; the site shows no dates. side: "S" = sold for the seller,
# "B" = represented the buyer.
SOLD_MORE = [
    ("1220 Cyndis Ln", "Greer", "B", "$304,990"),            # 04/2025
    ("241 Pebble Springs Dr", "Taylors", "S", "$193,000"),   # 03/2025
    ("305 Pebble Springs Dr", "Taylors", "S", "$162,000"),   # 12/2024
    ("302 E. Faris Rd", "Greenville", "B", "$722,500"),      # 12/2024
    ("140 Belshire Dr", "Greer", "S", "$395,000"),           # 11/2024 (bought for the same clients 06/2022)
    ("248 Pebble Springs Dr", "Taylors", "S", "$185,000"),   # 09/2024
    ("102 Ridge Rd", "Greenville", "S", "$275,000"),         # 08/2024 (bought for the same clients 04/2023)
    ("648 Cotton Branch Dr", "Boiling Springs", "B", "$219,000"),  # 03/2024
    ("102 Ridge Rd", "Greenville", "B", "$298,755"),         # 04/2023
    ("15 Heron Dr", "Fountain Inn", "S", "$268,000"),        # 04/2023
    ("406 Aniken Cir", "Boiling Springs", "B", "$255,100"),  # 09/2022
    ("361 Pewter Cir", "Simpsonville", "B", "$421,980"),     # 08/2022
    ("437 Buchanan Ridge Rd", "Taylors", "B", "$323,967"),   # 07/2022 (zip 29687)
    ("140 Belshire Dr", "Greer", "B", "$380,000"),           # 06/2022
    ("14 Garfield Ln", "Simpsonville", "S", "$299,999"),     # 06/2022
    ("410 Meadors Ave", "Greenville", "B", "$196,000"),      # 07/2021
    ("100 McCauley Rd Ext", "Travelers Rest", "S", "$245,000"),  # 07/2021
    ("501 Thorington Ct", "Greer", "S", "$370,000"),         # 06/2021
    ("121 Bagwell Farm Rd", "Spartanburg", "S", "$334,900"), # 06/2021
    ("205 Noble St", "Greer", "B", "$273,000"),              # 12/2020
    ("207 Pebble Springs Dr", "Taylors", "S", "$64,900"),    # 11/2020
]

REVIEWS = [
    {"quote": "Had a great first home buyers experience with this agent. He worked on my time frame and went over and above to get things going. I just closed on my first house and I couldn't have picked a better realtor! Thanks JR for all of your help! UPDATE: 4 years later I've chosen JR to help me sell my home. It's been an excellent experience. He uses a really neat drone for professional pictures for the listing. He is very prompt with every detail of the process. I'm very pleased and couldn't ask for a better realtor.",
     "name": "Brooke H.", "where": "bought, then sold"},
    {"quote": "JR did so much for me and my husband. JR was very punctual, able to be reached, willing to go the extra mile and was cheerful all the way through. We bought and sold and bought again from JR and the timing was like none other. It happened on same day where he told us bf closing of our new home that our old sold. So on the same day.. it was an awesome experience. He\u2019s very hard working and will go the extra mile (s)!!! I will not use another realtor as long as JR is around",
     "name": "Kerri H.", "where": "Google review"},
    {"quote": "J.R. Grimaldo helped my family more than I ever imagined and could ever repay. He not only got us into our dream home, he sold our home and my mother's home. He took care of all the details to make the selling process a breeze. J.R. was always there whenever we had questions or concerns. We will continue our relationship with J.R. for many years to come. We recommend J.R. to ANYONE looking to buy or sell.",
     "name": "Google reviewer", "where": "bought and sold"},
    {"quote": "A really great agent, if that is what you are searching for :) JR is a fantastic agent. He is very helpful and positive, as well as fair to everyone involved in the process. I always felt like we were in good hands with JR. As an agent he is always available, getting back to you if you have any questions or concerns in a prompt manner. I highly recommend JR as an agent. In our case he did take on a situation, manufactured homes in a place where residents don't actually own the land -- but do own their home -- despite not being that familiar with the arrangement. He caught on fast, was willing to tackle our situation and we had success. I guess in a nutshell JR takes a lot of the stress of selling or buying a home out of the process.",
     "name": "Peter H.", "where": ""},
    {"quote": "I just wanted to thank you again for helping us so much! I was so against trying to sell our house until Rusty and Sarah sold and then \"poof!!\", they were moving. I truly appreciate you and what you did for us. God makes things happen at the right time and we couldn't be happier that we got everything completed in time for Mom to enjoy it.",
     "name": "Darrell K.", "where": "seller"},
    {"quote": "JR was an excellent realtor to work with. Always on time, informative, professional and easy to communicate with. We had a great experience and would definitely recommend to our family and friends.",
     "name": "Slava S.", "where": ""},
    {"quote": "My wife and I were very pleased with J.R. Grimaldo's professionalism. He certainly is a credit to himself and his company!",
     "name": "Jeff D.", "where": "Google review"},
]

EN = {
    "lang": "en", "dir_prefix": "", "other_lang": "es", "other_label": "Español",
    "nav": [("index.html", "Home"), ("home-value.html", "What's My Home Worth"),
            ("listings.html", "My Listings"), ("sold.html", "Sold Homes"),
            ("about.html", "About J.R."), ("reviews.html", "Reviews"),
            ("contact.html", "Contact")],
    "search_label": "Search Homes",
    "hero_h1": "Thinking about selling your Upstate home? Start with a real number.",
    "hero_p": "Tell me the address. Within one business day you'll have a valuation prepared by a licensed South Carolina agent who looked at your home and the sales around it. Not a computer guess.",
    "hero_btn": "Get my home's value",
    "hero_addr": "Your home address",
    "truths": [
        ("Prepared by a person", "A licensed agent reviews your home and the recent sales nearby. Automated estimates skip that step."),
        ("One business day", "You get a written valuation by email. Fast enough to plan with, careful enough to trust."),
        ("Free, no strings", "No fee and no obligation. Use it to plan, to refinance, or just to know."),
    ],
    "why_h2": "Why sellers work with me",
    "why_p": "I've lived in Landrum for years and I work the whole Upstate, from the foothills down through Greenville and Spartanburg. I prefer working with sellers. That focus means I know what makes a listing move here, what buyers are paying, and where the landmines are between contract and closing.",
    "why_bullets": [
        "Honest pricing, even when it isn't what you hoped to hear.",
        "A negotiator on your side from the first offer to the closing table.",
        "Drone photos and a neighbor mailing on every listing.",
        "Fluent in English and Spanish.",
    ],
    "why_btn": "More about J.R.",
    "listings_h2": "On the market now",
    "listings_btn": "See all my listings",
    "cta_h2": "Ready to talk it through?",
    "cta_p": "Call, text, or send a note. No pressure, no script.",
    "cta_btn": "Contact J.R.",
    # home value page
    "hv_h1": "What's my home worth?",
    "hv_p": "Fill in what you can. I'll pull the recent sales around you, look at your home's details, and send you a written valuation within one business day.",
    "hv_fields": {
        "name": "Your name", "email": "Email", "phone": "Phone (optional)",
        "address": "Home address", "city": "City", "zip": "ZIP",
        "beds": "Bedrooms", "baths": "Bathrooms", "sqft": "Square feet (if known)",
        "year": "Year built (if known)", "updates": "Recent updates, condition, anything I should know",
        "timing": "When are you thinking of selling?",
        "timing_opts": ["Just curious", "In the next 3 months", "3 to 12 months", "More than a year"],
        "submit": "Send my request",
        "fine": "Your information goes only to J.R. It is never sold or shared.",
    },
    "hv_after_h2": "What happens next",
    "hv_after": [
        "Your request lands in my inbox.",
        "I pull the comparable sales and look at your home's details.",
        "You get a written valuation by email within one business day, with the sales I used so you can see the reasoning.",
    ],
    "hv_note": "Unlike an automatic estimate, this valuation is prepared by a licensed South Carolina agent. That's why it takes a day instead of a second.",
    # listings
    "li_h1": "My listings",
    "li_empty": "Nothing on the market under my name right now. New listings show up here first, before the postcards go out.",
    "li_mls": "MLS",
    "li_btn": "Details and photos",
    "so_h1": "Sold homes",
    "so_empty": "Recent sales will be listed here with their final prices. Ask me about any of them.",
    # about
    "ab_h1": "Principles Before Profits",
    "ab_p1": "Honesty and integrity are what you can expect when you hire me. I help people sell and buy homes across the Upstate, and I'm based in Landrum.",
    "ab_p2": "As your trusted advisor I offer a clear read on your situation, guide you through the process, and clear the landmines before they become problems. You'll have a skillful negotiator working for you every step of the way.",
    "ab_p3": "What separates me from other agents is my approach. I'm genuinely concerned with my client's best interest, and I'm relentless about solving whatever comes up between the signed contract and closing day. My clients tend to stay friends long after the keys change hands.",
    "ab_p4": "If you plan to sell and stay in the area, ask me how I can save you real money on your selling costs.",
    "ab_p5": "I am fluent in English and Spanish.",
    "ab_facts_h2": "The details",
    "ab_facts": [
        ("Licensed", "South Carolina REALTOR®, " + "SC License #95641"),
        ("Brokerage", BRAND["brokerage"]),
        ("Based in", "Landrum, SC"),
        ("Serving", ", ".join(SITE["areas"])),
        ("Member", "Greater Greenville Association of REALTORS®, South Carolina Association of REALTORS®, National Association of REALTORS®"),
        ("Languages", "English and Spanish"),
    ],
    # reviews
    "rv_h1": "What clients say",
    "rv_empty": "Client reviews are being gathered now. If you've worked with me, I'd be grateful for a few words.",
    "rv_btn": "Leave a review",
    # contact
    "ct_h1": "Get in touch",
    "ct_p": "Call or text is fastest. Email works too. If I'm driving, I'll get back to you the same day.",
    "ct_call": "Call or text",
    "ct_email": "Email",
    "ct_office": "Office",
    "ct_form_h2": "Or send a note",
    "ct_fields": {"name": "Your name", "email": "Email", "phone": "Phone (optional)",
                  "message": "How can I help?", "submit": "Send"},
    "footer_rights": "All rights reserved.",
    "footer_eho": "Equal Housing Opportunity.",
}

ES = {
    "lang": "es", "dir_prefix": "es/", "other_lang": "en", "other_label": "English",
    "nav": [("index.html", "Inicio"), ("home-value.html", "¿Cuánto vale mi casa?"),
            ("../listings.html", "Mis propiedades"), ("../sold.html", "Casas vendidas"),
            ("about.html", "Sobre J.R."), ("../reviews.html", "Opiniones"),
            ("contact.html", "Contacto")],
    "search_label": "Buscar casas",
    "hero_h1": "¿Piensa vender su casa en el Upstate? Empiece con un número real.",
    "hero_p": "Déme la dirección. En un día hábil tendrá una valuación preparada por un agente con licencia en Carolina del Sur, que revisó su casa y las ventas a su alrededor. No es un cálculo de computadora.",
    "hero_btn": "Quiero saber el valor de mi casa",
    "hero_addr": "Dirección de su casa",
    "truths": [
        ("Preparada por una persona", "Un agente con licencia revisa su casa y las ventas recientes cercanas. Los estimados automáticos se saltan ese paso."),
        ("Un día hábil", "Recibe una valuación por escrito en su correo. Rápida para planear, cuidadosa para confiar."),
        ("Gratis, sin compromiso", "Sin costo y sin obligación. Úsela para planear, para refinanciar, o solo para saber."),
    ],
    "why_h2": "Por qué los vendedores trabajan conmigo",
    "why_p": "Vivo en Landrum desde hace años y trabajo todo el Upstate, desde las montañas hasta Greenville y Spartanburg. Prefiero trabajar con vendedores. Por eso sé qué hace que una casa se venda aquí, cuánto están pagando los compradores, y dónde están los problemas entre el contrato y el cierre.",
    "why_bullets": [
        "Precios honestos, aunque no sea lo que esperaba oír.",
        "Un negociador de su lado desde la primera oferta hasta el cierre.",
        "Fotos con dron y envío postal a los vecinos en cada propiedad.",
        "Hablo inglés y español.",
    ],
    "why_btn": "Más sobre J.R.",
    "listings_h2": "En venta ahora",
    "listings_btn": "Ver todas mis propiedades",
    "cta_h2": "¿Listo para conversar?",
    "cta_p": "Llame, envíe un texto o un mensaje. Sin presión.",
    "cta_btn": "Contactar a J.R.",
    "hv_h1": "¿Cuánto vale mi casa?",
    "hv_p": "Llene lo que pueda. Yo busco las ventas recientes a su alrededor, reviso los detalles de su casa, y le envío una valuación por escrito en un día hábil.",
    "hv_fields": {
        "name": "Su nombre", "email": "Correo electrónico", "phone": "Teléfono (opcional)",
        "address": "Dirección de la casa", "city": "Ciudad", "zip": "Código postal",
        "beds": "Recámaras", "baths": "Baños", "sqft": "Pies cuadrados (si lo sabe)",
        "year": "Año de construcción (si lo sabe)", "updates": "Mejoras recientes, condición, cualquier cosa que deba saber",
        "timing": "¿Cuándo piensa vender?",
        "timing_opts": ["Solo por curiosidad", "En los próximos 3 meses", "De 3 a 12 meses", "En más de un año"],
        "submit": "Enviar mi solicitud",
        "fine": "Su información llega solo a J.R. Nunca se vende ni se comparte.",
    },
    "hv_after_h2": "Qué pasa después",
    "hv_after": [
        "Su solicitud llega a mi correo.",
        "Busco las ventas comparables y reviso los detalles de su casa.",
        "Recibe una valuación por escrito en un día hábil, con las ventas que usé para que vea el razonamiento.",
    ],
    "hv_note": "A diferencia de un estimado automático, esta valuación la prepara un agente con licencia en Carolina del Sur. Por eso toma un día y no un segundo.",
    "li_h1": "Mis propiedades", "li_empty": "", "li_mls": "MLS", "li_btn": "Detalles y fotos",
    "so_h1": "Casas vendidas", "so_empty": "",
    "ab_h1": "Principios Antes De Ganancias",
    "ab_p1": "Honestidad e integridad es lo que puede esperar cuando me contrata. Ayudo a vender y comprar casas en todo el Upstate, y vivo en Landrum.",
    "ab_p2": "Como su asesor de confianza, le doy una lectura clara de su situación, lo guío en el proceso, y quito los obstáculos antes de que sean problemas. Tendrá un negociador hábil trabajando para usted en cada paso.",
    "ab_p3": "Lo que me separa de otros agentes es mi forma de trabajar. Me importa de verdad el interés de mi cliente, y no descanso hasta resolver lo que surja entre la firma del contrato y el día del cierre. Mis clientes suelen seguir siendo amigos mucho después de recibir las llaves.",
    "ab_p4": "Si piensa vender y quedarse en la zona, pregúnteme cómo puedo ahorrarle dinero de verdad en los costos de venta.",
    "ab_p5": "Hablo inglés y español con fluidez.",
    "ab_facts_h2": "Los datos",
    "ab_facts": [
        ("Licencia", "REALTOR® de Carolina del Sur, SC License #95641"),
        ("Corredora", BRAND["brokerage"]),
        ("Vivo en", "Landrum, SC"),
        ("Zona de servicio", ", ".join(SITE["areas"])),
        ("Miembro", "Greater Greenville Association of REALTORS®, South Carolina Association of REALTORS®, National Association of REALTORS®"),
        ("Idiomas", "Inglés y español"),
    ],
    "rv_h1": "Opiniones", "rv_empty": "", "rv_btn": "",
    "ct_h1": "Contacto",
    "ct_p": "Llamar o enviar un texto es lo más rápido. El correo también funciona. Si estoy manejando, le respondo el mismo día.",
    "ct_call": "Llamar o texto", "ct_email": "Correo", "ct_office": "Oficina",
    "ct_form_h2": "O envíe un mensaje",
    "ct_fields": {"name": "Su nombre", "email": "Correo electrónico", "phone": "Teléfono (opcional)",
                  "message": "¿En qué puedo ayudarle?", "submit": "Enviar"},
    "footer_rights": "Todos los derechos reservados.",
    "footer_eho": "Igualdad de oportunidades de vivienda.",
}

# ------------------------------------------------------------------- HTML
CSS = r"""
:root{
  --ink:#1b2730; --ink-2:#4a5a66; --ridge:#2f4b5f; --ridge-deep:#213746;
  --haze:#e9eef1; --paper:#ffffff; --stone:#f3f2ee; --gold:#b98a2c; --gold-ink:#7a5a17;
  --line:#d8dde1; --focus:#b98a2c;
  --maxw:1080px; --gutter:20px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,"Times New Roman",serif;font-size:18px;line-height:1.55}
img{max-width:100%;display:block}
a{color:var(--ridge);text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
h1,h2,h3{font-weight:600;line-height:1.15;margin:0 0 .5em;letter-spacing:-.01em}
h1{font-size:clamp(2rem,5.5vw,3.2rem)}
h2{font-size:clamp(1.5rem,3.6vw,2.1rem)}
h3{font-size:1.15rem}
p{margin:0 0 1em;max-width:62ch}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--gutter)}
/* header */
.top{background:var(--ridge-deep);color:#fff}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px}
.brand{color:#fff;text-decoration:none;font-weight:600;font-size:1.2rem;letter-spacing:.01em}
.brand small{display:block;font-weight:400;font-size:.8rem;opacity:.8}
nav.menu{display:none}
nav.menu a{color:#fff;text-decoration:none;margin-left:16px;font-size:.92rem;white-space:nowrap;border-bottom:2px solid transparent;padding:4px 0}
nav.menu a[aria-current]{border-color:var(--gold)}
nav.menu a.lang{border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:3px 10px;margin-left:22px}
.burger{background:none;border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:6px;padding:8px 10px;font:inherit;font-size:.95rem;cursor:pointer}
.topright{display:flex;align-items:center;gap:8px}
.lang-m{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:6px 12px;font-size:.92rem;white-space:nowrap}
.drawer{display:none;background:var(--ridge);padding:8px 0 14px}
.drawer.open{display:block}
.drawer a{display:block;color:#fff;text-decoration:none;padding:12px var(--gutter);border-top:1px solid rgba(255,255,255,.12);font-size:1.05rem}
.drawer a[aria-current]{color:#f3d58a}
@media(min-width:1040px){nav.menu{display:flex;align-items:center}.burger,.drawer,.topright{display:none!important}}
/* hero */
.hero{background:linear-gradient(180deg,var(--ridge-deep) 0,var(--ridge) 100%);color:#fff;padding:48px 0 56px}
.hero h1{max-width:18ch}
.hero p{color:#dfe7ec;max-width:52ch;font-size:1.08rem}
.addr{display:flex;flex-direction:column;gap:10px;margin-top:22px;max-width:560px}
.addr input{font:inherit;font-size:1.05rem;padding:14px 16px;border:1px solid #fff;border-radius:8px;width:100%}
@media(min-width:620px){.addr{flex-direction:row}.addr input{flex:1}}
.btn{display:inline-block;background:var(--gold);color:#1b1503;font:inherit;font-weight:600;font-size:1.02rem;padding:14px 22px;border-radius:8px;border:0;text-decoration:none;cursor:pointer;white-space:nowrap}
.btn:hover{background:#cf9b34}
.btn.quiet{background:transparent;color:var(--ridge);border:1.5px solid var(--ridge)}
.btn.quiet:hover{background:var(--haze)}
/* sections */
section{padding:48px 0}
section.alt{background:var(--stone)}
.truths{display:grid;gap:22px}
.truths h3{margin-bottom:.25em}
.truths p{margin:0;color:var(--ink-2);font-size:1rem}
@media(min-width:720px){.truths{grid-template-columns:repeat(3,1fr);gap:32px}}
.split{display:grid;gap:28px;align-items:start}
@media(min-width:800px){.split{grid-template-columns:260px 1fr;gap:48px}}
.portrait{border-radius:14px;width:100%;max-width:300px;box-shadow:0 10px 30px rgba(33,55,70,.18)}
ul.plain{padding-left:1.15em;margin:0 0 1.2em}
ul.plain li{margin-bottom:.45em}
/* listings */
.cards{display:grid;gap:20px}
@media(min-width:720px){.cards{grid-template-columns:repeat(2,1fr)}}
.card{background:var(--paper);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.card .ph{aspect-ratio:4/3;background:var(--haze) repeating-linear-gradient(45deg,transparent 0 14px,rgba(47,75,95,.06) 14px 28px);display:flex;align-items:center;justify-content:center;color:var(--ink-2);font-size:.95rem}
.card .ph img{width:100%;height:100%;object-fit:cover}
.card .body{padding:16px 18px 20px}
.more-sold{margin-top:40px}
.more-sold h2{margin-bottom:.3em}
.sold-list{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:0;max-width:820px}
.sold-list li{display:grid;grid-template-columns:1fr auto;grid-template-areas:"a pr" "sd sd";gap:2px 16px;padding:12px 0;border-top:1px solid var(--line)}
.sold-list .a{grid-area:a}.sold-list .pr{grid-area:pr}.sold-list .sd{grid-area:sd}
.sold-list li:last-child{border-bottom:1px solid var(--line)}
.sold-list .a{font-weight:600}
.sold-list .c{color:var(--ink-2);font-weight:400}
.sold-list .pr{font-weight:600;color:var(--ridge-deep);text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.sold-list .sd{font-size:.9rem;color:var(--gold-ink)}
@media(min-width:640px){.sold-list li{grid-template-columns:1fr 190px 110px;grid-template-areas:"a sd pr";align-items:baseline}}
.card .role{display:inline-block;font-size:.85rem;font-weight:600;color:var(--gold-ink);background:#f6edd9;border-radius:999px;padding:3px 10px;margin:0 0 10px}
.card{align-self:start}
.card .price{font-size:1.4rem;font-weight:600;color:var(--ridge-deep);margin:0 0 .15em}
.card .addr-l{margin:0 0 .5em;font-weight:600}
.card p{font-size:1rem;color:var(--ink-2)}
.card .mls{font-size:.85rem;color:var(--ink-2);margin-bottom:.9em}
.empty{background:var(--stone);border-radius:12px;padding:28px 24px;max-width:62ch}
/* forms */
form.sheet{display:grid;gap:14px;max-width:640px}
form.sheet label{display:grid;gap:6px;font-size:.98rem}
form.sheet input,form.sheet select,form.sheet textarea{font:inherit;font-size:1.02rem;padding:12px 14px;border:1px solid #9aa7b0;border-radius:8px;width:100%;background:#fff}
form.sheet textarea{min-height:120px}
.two{display:grid;gap:14px}
@media(min-width:560px){.two{grid-template-columns:1fr 1fr}.three{grid-template-columns:1fr 1fr 1fr}}
.three{display:grid;gap:14px}
.fine{font-size:.9rem;color:var(--ink-2)}
.form-msg{padding:16px 18px;border-radius:8px;font-size:1.05rem;max-width:62ch;margin:0}
.form-msg.ok{background:#e6f1ea;color:#1d4a2e;border-left:4px solid #2f7a4a}
.form-msg.bad{background:#fbeaea;color:#6b1f1f;border-left:4px solid #b03a3a}
[hidden]{display:none!important}
.note{border-left:4px solid var(--gold);padding:12px 18px;background:var(--stone);max-width:62ch;margin:24px 0}
ol.steps{padding-left:1.2em;max-width:62ch}
ol.steps li{margin-bottom:.6em}
.facts{display:grid;gap:12px;max-width:720px}
.facts div{display:grid;grid-template-columns:120px 1fr;gap:12px;padding:12px 0;border-top:1px solid var(--line)}
.facts div:last-child{border-bottom:1px solid var(--line)}
.facts b{font-weight:600;color:var(--ridge-deep)}
.contact-grid{display:grid;gap:18px;max-width:720px}
@media(min-width:720px){.contact-grid{grid-template-columns:repeat(3,1fr)}}
.contact-grid a{font-size:1.1rem;font-weight:600;text-decoration:none}
.contact-grid small{display:block;color:var(--ink-2);font-size:.9rem;margin-bottom:4px}
blockquote{margin:0 0 24px;padding:20px 22px;background:var(--stone);border-radius:12px;max-width:62ch}
blockquote p{font-size:1.05rem}
blockquote footer{color:var(--ink-2);font-size:.95rem}
/* footer */
footer.site{background:var(--ridge-deep);color:#cfd9e0;padding:36px 0 40px;font-size:.92rem}
footer.site .wrap{display:grid;gap:18px}
footer.site a{color:#fff}
footer.site .merge{color:#f3d58a;font-weight:600;font-size:1rem}
footer.site p{margin:0;max-width:none}
@media(min-width:800px){footer.site .wrap{grid-template-columns:1fr 1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = r"""
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),d=document.querySelector('.drawer');
  if(b&&d){b.addEventListener('click',function(){var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  var h=document.getElementById('hero-addr');
  if(h){h.addEventListener('submit',function(e){e.preventDefault();var a=encodeURIComponent(h.querySelector('input').value||'');location.href=h.getAttribute('data-to')+(a?'?address='+a:'');});}
  var f=document.getElementById('addr-field');
  if(f){var q=new URLSearchParams(location.search).get('address');if(q)f.value=q;}
  document.querySelectorAll('form.js-fs').forEach(function(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var btn=form.querySelector('button[type=submit]'),msg=form.querySelector('.form-msg'),label=btn.textContent;
      btn.disabled=true;btn.textContent=form.dataset.sending;
      var src=new FormData(form),fd=new FormData();
      try{
        var g=function(k){return (src.get(k)||'').toString().trim();};
        var r={t:form.id==='hv-form'?'v':'c',l:document.documentElement.lang==='es'?'es':'en',
               n:g('name'),p:g('phone'),e:g('email'),a:[g('address'),g('city')].filter(Boolean).join(', ')};
        fd.append('tap_to_reply',location.origin+'/reply.html#'+new URLSearchParams(r).toString());
      }catch(err){}
      src.forEach(function(v,k){fd.append(k,v);});
      fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'}})
        .then(function(r){
          if(!r.ok)throw new Error('send failed');
          form.querySelectorAll('label,.two,.three,.fine,button').forEach(function(el){el.hidden=true;});
          msg.className='form-msg ok';msg.textContent=form.dataset.ok;msg.hidden=false;
          msg.scrollIntoView({block:'center'});
        })
        .catch(function(){
          btn.disabled=false;btn.textContent=label;
          msg.className='form-msg bad';msg.textContent=form.dataset.bad;msg.hidden=false;
        });
    });
  });
});
"""

def esc(s): return html.escape(s, quote=True)

def mail_form(T, lang, subject, fields_html, submit_label, form_id=""):
    """Formspree if an ID is set, otherwise a mailto that opens the visitor's mail app."""
    if SITE["formspree_id"]:
        action = f'https://formspree.io/f/{SITE["formspree_id"]}'
        hidden = (f'<input type="hidden" name="_subject" value="{esc(subject)}">'
                  f'<input type="hidden" name="language" value="{"Spanish" if lang == "es" else "English"}">'
                  '<input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">')
        if lang == "es":
            ok = "Gracias. Su solicitud llegó a J.R. Recibirá respuesta en un día hábil."
            bad = "No se pudo enviar. Por favor llame o envíe un texto a J.R. al " + SITE["phone"] + "."
            sending = "Enviando…"
        else:
            ok = "Thank you. Your request reached J.R. You'll hear back within one business day."
            bad = "That didn't go through. Please call or text J.R. at " + SITE["phone"] + "."
            sending = "Sending…"
        return (f'<form class="sheet js-fs" id="{form_id}" action="{action}" method="POST" '
                f'data-ok="{esc(ok)}" data-bad="{esc(bad)}" data-sending="{esc(sending)}">{hidden}{fields_html}'
                f'<button class="btn" type="submit">{esc(submit_label)}</button>'
                f'<p class="form-msg" role="status" aria-live="polite" hidden></p></form>')
    action = f'mailto:{SITE["email"]}?subject={esc(subject)}'
    return f'<form class="sheet" id="{form_id}" action="{action}" method="POST" enctype="text/plain">{fields_html}<button class="btn" type="submit">{esc(submit_label)}</button></form>'

def field(name, label, typ="text", req=False, opts=None, textarea=False, fid=None):
    r = " required" if req else ""
    i = f' id="{fid}"' if fid else ""
    if textarea:
        return f'<label>{esc(label)}<textarea name="{name}"{r}></textarea></label>'
    if opts:
        o = "".join(f'<option>{esc(x)}</option>' for x in opts)
        return f'<label>{esc(label)}<select name="{name}">{o}</select></label>'
    return f'<label>{esc(label)}<input type="{typ}" name="{name}"{i}{r}></label>'

def layout(T, page, title, body, lang_switch):
    p = T["dir_prefix"]
    up = "../" if p else ""
    nav_links = ""
    drawer = ""
    for href, label in T["nav"]:
        cur = ' aria-current="page"' if href.endswith(page) and not href.startswith("..") else ""
        nav_links += f'<a href="{href}"{cur}>{esc(label)}</a>'
        drawer += f'<a href="{href}"{cur}>{esc(label)}</a>'
    search = f'<a href="{BRAND["brokerage_site"]}" rel="noopener">{esc(T["search_label"])}</a>'
    lang = f'<a class="lang" href="{lang_switch}" lang="{T["other_lang"]}">{T["other_label"]}</a>'
    note = BRAND["brokerage_note"] if T["lang"] == "en" else BRAND["brokerage_note_es"]
    return f"""<!doctype html>
<html lang="{T['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(T['hero_p'])}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="J.R. Grimaldo, REALTOR®">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(T['hero_p'])}">
<meta property="og:image" content="https://{SITE['domain']}/assets/share.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="https://{SITE['domain']}/{p}{page}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{up if p else ''}{'index.html' if not p else 'index.html'}">{esc(SITE['agent'])}<small>{esc(BRAND['brokerage'])}</small></a>
    <nav class="menu" aria-label="Main">{nav_links}{search}{lang}</nav>
    <div class="topright"><a class="lang-m" href="{lang_switch}" lang="{T["other_lang"]}">{T["other_label"]}</a><button class="burger" aria-expanded="false" aria-controls="drawer">Menu</button></div>
  </div>
  <div class="drawer" id="drawer">{drawer}{search}</div>
</header>
<main>
{body}
</main>
<footer class="site">
  <div class="wrap">
    <div>
      <p class="merge">{esc(note)}</p>
      <p>{esc(SITE['agent'])}, REALTOR® · {esc(SITE['license'])}</p>
      <p>{esc(BRAND['brokerage'])} · {esc(BRAND['broker_in_charge'])}</p>
      <p>{esc(BRAND['office'])}</p>
    </div>
    <div>
      <p><a href="tel:{SITE['phone_tel']}">{SITE['phone']}</a> · <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      <p>{esc(T['footer_eho'])} © 2026 {esc(SITE['agent'])}. {esc(T['footer_rights'])}</p>
    </div>
  </div>
</footer>
<script src="{up}assets/site.js"></script>
</body>
</html>"""

def card(it, T):
    if "photo" in it and it["photo"] is None:
        phdiv = ""
    else:
        ph = f'<img src="{"../" if T["dir_prefix"] else ""}assets/{it["photo"]}" alt="{esc(it["address"])}">' if it.get("photo") else "Photo coming"
        phdiv = f'<div class="ph">{ph}</div>'
    role = f'<p class="role">{esc(it["role"])}</p>' if it.get("role") else ""
    return f"""<article class="card">{phdiv}<div class="body">{role}
<p class="price">{esc(it['price'])}</p><p class="addr-l">{esc(it['address'])}</p>
<p>{esc(it.get('line',''))}</p>{('<p class="mls">'+esc(it['mls'])+'</p>') if it.get('mls') else ''}
{('<a class="btn quiet" href="'+it['link']+'">'+esc(T['li_btn'])+'</a>') if it.get('link') else ''}</div></article>"""

def page_home(T):
    up = "../" if T["dir_prefix"] else ""
    truths = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in T["truths"])
    bullets = "".join(f'<li>{esc(x)}</li>' for x in T["why_bullets"])
    cards = "".join(card(x, T) for x in LISTINGS[:2]) if LISTINGS else f'<div class="empty"><p>{esc(EN["li_empty"] if T["lang"]=="en" else "Por ahora no tengo propiedades en venta. Las nuevas aparecen aquí primero.")}</p></div>'
    listings_href = "listings.html" if not T["dir_prefix"] else "../listings.html"
    return f"""
<section class="hero"><div class="wrap">
  <h1>{esc(T['hero_h1'])}</h1>
  <p>{esc(T['hero_p'])}</p>
  <form class="addr" id="hero-addr" data-to="home-value.html">
    <label class="visually-hidden" style="position:absolute;left:-9999px" for="hero-input">{esc(T['hero_addr'])}</label>
    <input id="hero-input" type="text" placeholder="{esc(T['hero_addr'])}" autocomplete="street-address">
    <button class="btn" type="submit">{esc(T['hero_btn'])}</button>
  </form>
</div></section>
<section><div class="wrap"><div class="truths">{truths}</div></div></section>
<section class="alt"><div class="wrap split">
  <img class="portrait" src="{up}assets/jr-headshot.jpg" alt="{esc(SITE['agent'])}">
  <div><h2>{esc(T['why_h2'])}</h2><p>{esc(T['why_p'])}</p><ul class="plain">{bullets}</ul>
  <a class="btn quiet" href="about.html">{esc(T['why_btn'])}</a></div>
</div></section>
<section><div class="wrap"><h2>{esc(T['listings_h2'])}</h2><div class="cards">{cards}</div>
<p style="margin-top:22px"><a class="btn quiet" href="{listings_href}">{esc(T['listings_btn'])}</a></p></div></section>
<section class="alt"><div class="wrap"><h2>{esc(T['cta_h2'])}</h2><p>{esc(T['cta_p'])}</p>
<a class="btn" href="contact.html">{esc(T['cta_btn'])}</a></div></section>"""

def page_home_value(T):
    F = T["hv_fields"]
    fields = (
        '<div class="two">' + field("name", F["name"], req=True) + field("email", F["email"], "email", req=True) + '</div>'
        + field("phone", F["phone"], "tel")
        + field("address", F["address"], req=True, fid="addr-field")
        + '<div class="two">' + field("city", F["city"], req=True) + field("zip", F["zip"]) + '</div>'
        + '<div class="three">' + field("bedrooms", F["beds"]) + field("bathrooms", F["baths"]) + field("square_feet", F["sqft"]) + '</div>'
        + field("year_built", F["year"])
        + field("updates", F["updates"], textarea=True)
        + field("timing", F["timing"], opts=F["timing_opts"])
        + f'<p class="fine">{esc(F["fine"])}</p>'
    )
    subj = "Home valuation request from " + SITE["domain"] if T["lang"] == "en" else "Solicitud de valuación desde " + SITE["domain"]
    form = mail_form(T, T["lang"], subj, fields, F["submit"], "hv-form")
    steps = "".join(f'<li>{esc(x)}</li>' for x in T["hv_after"])
    return f"""
<section><div class="wrap"><h1>{esc(T['hv_h1'])}</h1><p>{esc(T['hv_p'])}</p>{form}</div></section>
<section class="alt"><div class="wrap"><h2>{esc(T['hv_after_h2'])}</h2><ol class="steps">{steps}</ol>
<div class="note"><p style="margin:0">{esc(T['hv_note'])}</p></div></div></section>"""

def page_list(T, h1, items, empty, intro=""):
    cards = "".join(card(x, T) for x in items)
    body = f'<div class="cards">{cards}</div>' if items else f'<div class="empty"><p style="margin:0">{esc(empty)}</p></div>'
    lead = f'<p>{esc(intro)}</p>' if (intro and items) else ""
    return f'<section><div class="wrap"><h1>{esc(h1)}</h1>{lead}{body}</div></section>'

def page_sold():
    base = page_list(EN, EN["so_h1"], SOLD, EN["so_empty"], "Recently sold, and which side I represented. Ask me about any of them.")
    if not SOLD_MORE:
        return base
    rows = "".join(
        f'<li><span class="a">{esc(a)}, <span class="c">{esc(c)}</span></span>'
        f'<span class="sd">{"Sold for the seller" if sd == "S" else "Represented the buyer"}</span>'
        f'<span class="pr">{esc(pr)}</span></li>' for a, c, sd, pr in SOLD_MORE)
    n = len(SOLD) + len(SOLD_MORE)
    more = (f'<div class="more-sold"><h2>More homes I\'ve helped sell and buy</h2>'
            f'<p>{n} closed sales across the Upstate, from Taylors and Greer to Simpsonville, Fountain Inn, and Boiling Springs.</p>'
            f'<ul class="sold-list">{rows}</ul></div>')
    i = base.rfind("</div></section>")
    return base[:i] + more + base[i:]

def page_about(T):
    up = "../" if T["dir_prefix"] else ""
    facts = "".join(f'<div><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in T["ab_facts"])
    return f"""
<section><div class="wrap split">
  <img class="portrait" src="{up}assets/jr-headshot.jpg" alt="{esc(SITE['agent'])}">
  <div><h1>{esc(T['ab_h1'])}</h1>
  <p>{esc(T['ab_p1'])}</p><p>{esc(T['ab_p2'])}</p><p>{esc(T['ab_p3'])}</p><p>{esc(T['ab_p4'])}</p><p>{esc(T['ab_p5'])}</p>
  <a class="btn" href="home-value.html">{esc(T['hero_btn'])}</a></div>
</div></section>
<section class="alt"><div class="wrap"><h2>{esc(T['ab_facts_h2'])}</h2><div class="facts">{facts}</div></div></section>"""

def page_reviews(T):
    if REVIEWS:
        body = "".join(f'<blockquote><p>{esc(r["quote"])}</p><footer>{esc(r["name"])}{(", "+esc(r["where"])) if r.get("where") else ""}</footer></blockquote>' for r in REVIEWS)
        body += f'<p>Worked with me? <a class="btn quiet" href="{SITE["review_page"]}">Leave a review</a></p>'
    else:
        body = f'<div class="empty"><p>{esc(T["rv_empty"])}</p><a class="btn quiet" href="{SITE["review_page"]}">{esc(T["rv_btn"])}</a></div>'
    return f'<section><div class="wrap"><h1>{esc(T["rv_h1"])}</h1>{body}</div></section>'

def page_contact(T):
    F = T["ct_fields"]
    fields = ('<div class="two">' + field("name", F["name"], req=True) + field("email", F["email"], "email", req=True) + '</div>'
              + field("phone", F["phone"], "tel") + field("message", F["message"], textarea=True, req=True))
    subj = "Message from " + SITE["domain"] if T["lang"] == "en" else "Mensaje desde " + SITE["domain"]
    form = mail_form(T, T["lang"], subj, fields, F["submit"], "ct-form")
    return f"""
<section><div class="wrap"><h1>{esc(T['ct_h1'])}</h1><p>{esc(T['ct_p'])}</p>
<div class="contact-grid">
  <div><small>{esc(T['ct_call'])}</small><a href="tel:{SITE['phone_tel']}">{SITE['phone']}</a></div>
  <div><small>{esc(T['ct_email'])}</small><a href="mailto:{SITE['email']}">{SITE['email']}</a></div>
  <div><small>{esc(T['ct_office'])}</small><span>{esc(BRAND['office'])}</span></div>
</div></div></section>
<section class="alt"><div class="wrap"><h2>{esc(T['ct_form_h2'])}</h2>{form}</div></section>"""

# ------------------------------------------------------------- REPLY PAGE
# Opened from the "tap_to_reply" link in each Formspree email. Everything
# about the visitor rides after the # in the link, so it never reaches a
# server. Not linked from the site and hidden from search engines.
# Edit the notes in NOTES below.
REPLY_HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Reply – J.R. Grimaldo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<link rel="stylesheet" href="assets/site.css">
<style>
.rp{padding-block:28px 48px}
.rp h1{font-size:1.6rem;margin-bottom:.2em}
.rp .who{color:var(--ink-2);margin-bottom:22px}
.rp .acts{display:grid;gap:12px;max-width:520px;margin-bottom:26px}
.rp .acts .btn{text-align:center;font-size:1.15rem;padding:18px 20px}
.rp .acts .btn[aria-disabled=true]{opacity:.45;pointer-events:none}
.rp h2{font-size:1.05rem;margin:22px 0 8px}
.rp pre{white-space:pre-wrap;font:inherit;font-size:1rem;background:var(--stone);border-radius:10px;padding:14px 16px;max-width:620px;margin:0}
.rp .tog{display:flex;gap:8px;margin-bottom:18px}
.rp .tog button{font:inherit;padding:8px 14px;border-radius:999px;border:1.5px solid var(--ridge);background:#fff;color:var(--ridge);cursor:pointer}
.rp .tog button[aria-pressed=true]{background:var(--ridge);color:#fff}
</style></head>
<body>
<main class="wrap rp">
  <h1 id="h">Reply</h1>
  <p class="who" id="who"></p>
  <div class="tog" role="group" aria-label="Language">
    <button type="button" data-l="en">English</button>
    <button type="button" data-l="es">Español</button>
  </div>
  <div class="acts">
    <a class="btn" id="sms" href="#">Text</a>
    <a class="btn quiet" id="mail" href="#">Email</a>
  </div>
  <h2>Text message</h2><pre id="tx"></pre>
  <h2>Email</h2><pre id="em"></pre>
</main>
<script>
var NOTES={
 en:{
  v:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your home value request for {addr}. I'm pulling the recent sales near you now, and you'll have your valuation by email within one business day. Any questions in the meantime, just text me here.",
     subj:"Your home value request for {addr}",
     mail:"Hi {first},\n\nThank you for asking me to value your home at {addr}. I got your request, and I'm on it.\n\nI'm a licensed South Carolina agent, and I prepare every valuation myself. I'll look at the recent sales near you and at your home's details, then send you a written valuation within one business day, with the sales I used so you can see the reasoning.\n\nIf you'd like to talk sooner, call or text me at 864-381-2326.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrinciples Before Profits"},
  c:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your message from my website. What's a good time to talk? You can also reach me right here by text.",
     subj:"Thanks for reaching out",
     mail:"Hi {first},\n\nThank you for your message. I got it and wanted you to know right away.\n\nWhat's a good time to talk? You can call or text me at 864-381-2326, or simply reply to this email.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrinciples Before Profits"}},
 es:{
  v:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su solicitud de valuación para {addr}. Ya estoy revisando las ventas recientes cerca de usted, y tendrá su valuación por correo en un día hábil. Si tiene alguna pregunta, escríbame aquí.",
     subj:"Su solicitud de valuación para {addr}",
     mail:"Hola {first}:\n\nGracias por pedirme la valuación de su casa en {addr}. Recibí su solicitud y ya estoy trabajando en ella.\n\nSoy agente con licencia en Carolina del Sur y preparo cada valuación personalmente. Voy a revisar las ventas recientes cerca de usted y los detalles de su casa, y le enviaré una valuación por escrito en un día hábil, con las ventas que usé para que vea el razonamiento.\n\nSi prefiere hablar antes, llámeme o escríbame al 864-381-2326.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrincipios Antes De Ganancias"},
  c:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su mensaje desde mi página web. ¿A qué hora le queda bien que hablemos? También puede escribirme aquí.",
     subj:"Gracias por comunicarse",
     mail:"Hola {first}:\n\nGracias por su mensaje. Lo recibí y quería avisarle de inmediato.\n\n¿A qué hora le queda bien que hablemos? Puede llamarme o escribirme al 864-381-2326, o simplemente responder a este correo.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrincipios Antes De Ganancias"}}
};
var q=new URLSearchParams(location.hash.slice(1));
var d={t:q.get('t')==='c'?'c':'v',l:q.get('l')==='es'?'es':'en',n:q.get('n')||'',p:(q.get('p')||'').replace(/[^0-9+]/g,''),e:q.get('e')||'',a:q.get('a')||''};
var first=(d.n.split(/\s+/)[0]||'').replace(/^./,function(c){return c.toUpperCase();});
function fill(s){return s.replace(/\{first\}/g,first||(d.l==='es'?'':'there')).replace(/\{addr\}/g,d.a||(d.l==='es'?'su casa':'your home')).replace(/^Hola :/,'Hola:').replace(/^Hola ,/,'Hola,');}
function show(){
  var N=NOTES[d.l][d.t],tx=fill(N.text),sj=fill(N.subj),bd=fill(N.mail);
  document.documentElement.lang=d.l;
  document.getElementById('h').textContent=(d.l==='es'?'Responder a ':'Reply to ')+(d.n||'?');
  document.getElementById('who').textContent=[d.t==='v'?(d.l==='es'?'Solicitud de valuación':'Home value request'):(d.l==='es'?'Mensaje':'Message'),d.a,d.p,d.e].filter(Boolean).join(' · ');
  document.getElementById('tx').textContent=tx;
  document.getElementById('em').textContent='Subject: '+sj+'\n\n'+bd;
  var s=document.getElementById('sms'),m=document.getElementById('mail');
  s.textContent=(d.l==='es'?'Enviar texto a ':'Text ')+(first||'');
  m.textContent=(d.l==='es'?'Enviar correo a ':'Email ')+(first||'');
  if(d.p){var num=d.p.length===10?'+1'+d.p:d.p;s.href='sms:'+num+'?&body='+encodeURIComponent(tx);s.removeAttribute('aria-disabled');}
  else{s.href='#';s.setAttribute('aria-disabled','true');s.textContent=d.l==='es'?'Sin teléfono':'No phone number given';}
  if(d.e){m.href='mailto:'+d.e.replace(/[^A-Za-z0-9@._+-]/g,'')+'?subject='+encodeURIComponent(sj)+'&body='+encodeURIComponent(bd);m.removeAttribute('aria-disabled');}
  else{m.href='#';m.setAttribute('aria-disabled','true');}
  document.querySelectorAll('.tog button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===d.l?'true':'false');});
}
document.querySelectorAll('.tog button').forEach(function(b){b.addEventListener('click',function(){d.l=b.dataset.l;show();});});
show();
</script>
</body></html>"""

FAVICON ='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#213746"/><path d="M12 40 L24 24 L32 32 L42 18 L52 40 Z" fill="#b98a2c"/><rect x="12" y="42" width="40" height="6" fill="#e9eef1"/></svg>'

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / "es").mkdir()
    for f in (SRC / "assets").iterdir(): shutil.copy(f, OUT / "assets" / f.name)
    (OUT / "assets" / "site.css").write_text(CSS)
    (OUT / "assets" / "site.js").write_text(JS)
    (OUT / "assets" / "favicon.svg").write_text(FAVICON)
    (OUT / "reply.html").write_text(REPLY_HTML)
    # IONOS used to forward jrresales.com to /defaultsite. Browsers that saved
    # that forwarding land here; send them to /index.html (not /, which those
    # browsers would bounce back here).
    (OUT / "defaultsite").mkdir(exist_ok=True)
    (OUT / "defaultsite" / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/index.html"><link rel="canonical" href="/index.html"><title>J.R. Grimaldo</title><a href="/index.html">Go to jrresales.com</a><script>location.replace("/index.html")</script>')
    (OUT / "CNAME").write_text(SITE["domain"] + "\n")
    # Search engines: list of public pages, and where to find it.
    base = "https://" + SITE["domain"] + "/"
    urls = ["", "home-value.html", "listings.html", "sold.html", "about.html", "reviews.html", "contact.html",
            "es/index.html", "es/home-value.html", "es/about.html", "es/contact.html"]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{base}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /reply.html\nDisallow: /defaultsite/\nSitemap: " + base + "sitemap.xml\n")
    (OUT / ".nojekyll").write_text("")

    t = SITE["title_tag"]
    # English
    pages = {
        "index.html": (t, page_home(EN), "es/index.html"),
        "home-value.html": ("What's My Home Worth? – " + SITE["agent"], page_home_value(EN), "es/home-value.html"),
        "listings.html": ("My Listings – " + SITE["agent"], page_list(EN, EN["li_h1"], LISTINGS, EN["li_empty"]), "es/index.html"),
        "sold.html": ("Sold Homes – " + SITE["agent"], page_sold(), "es/index.html"),
        "about.html": ("About J.R. Grimaldo", page_about(EN), "es/about.html"),
        "reviews.html": ("Reviews – " + SITE["agent"], page_reviews(EN), "es/index.html"),
        "contact.html": ("Contact – " + SITE["agent"], page_contact(EN), "es/contact.html"),
    }
    for name, (title, body, sw) in pages.items():
        (OUT / name).write_text(layout(EN, name, title, body, sw))
    # Spanish
    es_pages = {
        "index.html": ("J.R. Grimaldo, REALTOR® – Upstate SC", page_home(ES), "../index.html"),
        "home-value.html": ("¿Cuánto vale mi casa? – " + SITE["agent"], page_home_value(ES), "../home-value.html"),
        "about.html": ("Sobre J.R. Grimaldo", page_about(ES), "../about.html"),
        "contact.html": ("Contacto – " + SITE["agent"], page_contact(ES), "../contact.html"),
    }
    for name, (title, body, sw) in es_pages.items():
        (OUT / "es" / name).write_text(layout(ES, name, title, body, sw))
    print("built", len(pages) + len(es_pages), "pages into", OUT)

if __name__ == "__main__":
    build()
