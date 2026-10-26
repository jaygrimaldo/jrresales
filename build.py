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
    "areas": ["Landrum", "Campobello", "Inman", "Lyman", "Greer", "Taylors",
              "Greenville", "Spartanburg", "Simpsonville", "Fountain Inn",
              "Travelers Rest"],
    # Leave empty to send the valuation form by the visitor's own email app.
    # Paste a Formspree form ID (e.g. "xabcdefg") to send through Formspree.
    "formspree_id": "mdeenynr",
    "review_page": "https://jaygrimaldo.github.io/reviews",
    "valuation_domain": "jrrevalues.com",
    "facebook": "",
    # Profiles that point back to this site (checked 10/22/2026). Used in the
    # hidden "who is this agent" label Google reads (schema.org RealEstateAgent).
    "profiles": ["https://www.facebook.com/jrresales",
                 "https://www.zillow.com/profile/Jose%20Grimaldo3",
                 "https://www.instagram.com/jrgrimaldorealtor/"],
}

# ------------------------------------------------------------------ CONTENT
LISTINGS = [
    {
        "address": "300 Colony Rd, Travelers Rest, SC 29690",
        "price": "$309,999",
        "line": "Full brick ranch on a corner lot in Points North, built in 1978. Three bedrooms, two full baths, all on one level. USDA area: qualified buyers may put $0 down.",
        "line_es": "Casa de ladrillo de un solo nivel en lote de esquina en Points North, construida en 1978. Tres recámaras y dos baños completos. Zona USDA: los compradores que califiquen pueden comprar con $0 de enganche.",
        "mls": "Greenville MLS 1605021",
        "link": "https://jrgrimaldo.northgroupre.com/property/63-1605021-300-colony-road-travelers-rest-SC-29690",
        "photo": "300-colony-rd.jpg",
    },
    {
        "address": "207 Penrith Ct, Simpsonville, SC 29681",
        "price": "$352,999",
        "role": "Repeat client",  # Berhane bought 1220 Cyndis Ln with J.R. in 2025, then listed Penrith
        "role_es": "Cliente previo",
        "line": "Investor opportunity: leased through May 31, 2027, so it earns rent from day one. Four bedrooms, two and a half baths, about 1,980 sq ft on a cul-de-sac in Villages at Windsor. New roof in late 2024.",
        "line_es": "Oportunidad para inversionistas: rentada hasta el 31 de mayo de 2027, así que genera renta desde el primer día. Cuatro recámaras, dos baños y medio, unos 1,980 pies cuadrados en una calle cerrada en Villages at Windsor. Techo nuevo a finales de 2024.",
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
     "role": "Sold for the seller \u00b7 Repeat client",
     "role_es": "Representé al vendedor \u00b7 Cliente previo",
     "line": "Three bedrooms, two baths in Landrum. I helped these same clients buy it seven years earlier.",
     "line_es": "Tres recámaras y dos baños en Landrum. Siete años antes, ayudé a estos mismos clientes a comprarla.",
     "photo": "248-page-creek-blvd.jpg"},
    {"address": "420 Cloverdale Ln, Simpsonville, SC 29681", "price": "Sold for $175,000",
     "role": "Sold for the seller \u00b7 Referred by a past client",  # Willimon, referred by her son Russell Beaver
     "role_es": "Representé al vendedor \u00b7 Recomendado por un cliente previo",
     "line": "Three bedrooms, one and a half baths in Simpsonville.",
     "line_es": "Tres recámaras y un baño y medio en Simpsonville.",
     "photo": "420-cloverdale-ln.jpg"},
    {"address": "140 Belshire Dr, Greer, SC 29650", "price": "Sold for $395,000",
     "role": "Sold for the seller \u00b7 Repeat client",
     "role_es": "Representé al vendedor \u00b7 Cliente previo",
     "line": "Three bedrooms, two and a half baths in Greer. I helped these same clients buy it two years earlier.",
     "line_es": "Tres recámaras y dos baños y medio en Greer. Dos años antes, ayudé a estos mismos clientes a comprarla.",
     "photo": "140-belshire-dr.jpg"},  # J.R.'s own listing photo 1 (Greenville MLS 1535838), closed 11/2024
    {"address": "304 Talbert Trail, Landrum, SC 29356", "price": "Sold for $290,000",
     "role": "Represented the buyer \u00b7 Repeat client",  # Bests, first bought Page Creek with J.R. in 2018
     "role_es": "Representé al comprador \u00b7 Cliente previo",
     "line": "Three bedrooms, two baths in Landrum.",
     "line_es": "Tres recámaras y dos baños en Landrum.",
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
    # Every closed sale from dotloop and OneDrive (checked with J.R. 10/23/2026),
    # newest first. The four photo cards above are not repeated here.
    # side: "S" sold for the seller, "B" represented the buyer, "SB" both sides.
    # tag: "repeat" = a later deal for a family that already closed one with J.R.
    # (J.R.'s rule: selling and buying in the same move is one hiring, not a
    # repeat). "referral" = referred by a past client. Dates in comments only.
    # Left off on purpose: 150 Buck Branch Rd, Mill Spring NC (J.R. no longer
    # holds an NC license), "2019 Grimaldo" (his own), 724 Ridge Dr (Cassar).
    ("1220 Cyndis Ln", "Greer", "B", "$304,990"),                  # 04/2025
    ("241 Pebble Springs Dr", "Taylors", "S", "$193,000"),         # 03/2025
    ("305 Pebble Springs Dr", "Taylors", "S", "$162,000"),         # 12/2024
    ("302 E. Faris Rd", "Greenville", "B", "$722,500", "repeat"),  # 12/2024
    ("248 Pebble Springs Dr", "Taylors", "S", "$185,000", "repeat"),  # 09/2024
    ("102 Ridge Rd", "Greenville", "S", "$275,000", "repeat"),     # 08/2024
    ("161 Dogwood Ave", "Spartanburg", "B", "$150,000"),           # 04/2024
    ("648 Cotton Branch Dr", "Boiling Springs", "B", "$219,000"),  # 03/2024
    ("1 Octavia Rd", "Taylors", "B", "$412,500", "repeat"),        # 11/2023
    ("102 Ridge Rd", "Greenville", "B", "$298,755", "repeat"),     # 04/2023
    ("15 Heron Dr", "Fountain Inn", "S", "$268,000", "repeat"),    # 04/2023
    ("406 Aniken Cir", "Boiling Springs", "B", "$255,100"),        # 09/2022
    ("361 Pewter Cir", "Simpsonville", "B", "$421,980", "repeat"), # 08/2022
    ("437 Buchanan Ridge Rd", "Taylors", "B", "$323,967", "referral"),  # 07/2022 Robinson, referred by Jeff DiStefano
    ("140 Belshire Dr", "Greer", "B", "$380,000", "referral"),     # 06/2022 Hawkins first deal, referred by Jeff DiStefano
    ("14 Garfield Ln", "Simpsonville", "S", "$299,999", "repeat"), # 06/2022
    ("410 Meadors Ave", "Greenville", "B", "$196,000"),            # 07/2021
    ("100 McCauley Rd Ext", "Travelers Rest", "S", "$245,000"),    # 07/2021
    ("501 Thorington Ct", "Greer", "S", "$370,000", "repeat"),     # 06/2021
    ("121 Bagwell Farm Rd", "Spartanburg", "S", "$334,900", "repeat"),  # 06/2021
    ("205 Noble St", "Greer", "B", "$273,000"),                    # 12/2020
    ("207 Pebble Springs Dr", "Taylors", "S", "$64,900"),          # 11/2020 seller Rosemary Covella Slate (manufactured home)
    ("2 Horseback Way", "Travelers Rest", "S", "$99,000", "repeat"),  # 11/2020
    ("307 Winding Willow Trl", "Taylors", "B", "$198,000"),        # 10/16/2020 buyer Rosemary Covella Slate (same move as her 207 Pebble Springs sale)
    ("214 Pebble Springs Dr", "Taylors", "S", "$93,000"),          # fall 2020 Peter Hildebrandt and Victoriano Mendez; two offers ($93,000 Posey, $93,500 Hartzig), no closing paper; lower one shown
    ("285 Pebble Springs Dr", "Taylors", "S", "$80,000"),          # 09/2020 manufactured home
    ("330 N Buncombe Rd", "Greer", "SB", "$108,000"),              # 06/2020 J.R. represented one side and handled the other as a transaction broker (customer, not client)
    ("334 N Buncombe Rd", "Greer", "S", "$110,000"),               # 06/2020
    ("4 Bullard Ct", "Greer", "B", "$287,500"),                    # 06/2020
    ("3704 Ballenger Rd", "Greer", "S", "$224,000"),               # 06/2020
    ("3702 Ballenger Rd", "Greer", "S", "$210,000"),               # 06/2020
    ("292 Pebble Springs Dr", "Taylors", "S", "$110,000", "repeat"),  # spring 2020 mobile home, listed 03/2020 at $110,500; J.R.: "sold for 110,000 something"
    ("304 Clemson Ave", "Greenville", "B", "$87,145"),             # 11/2019
    ("208 Buchanan Ridge Rd", "Taylors", "B", "$316,523"),         # 11/2019 new build, Lincoln Park lot 123 (DiStefano first deal)
    ("4 Twin Falls Dr", "Simpsonville", "B", "$162,000"),          # 10/2019
    ("14 Garfield Ln", "Simpsonville", "B", "$196,000"),           # 08/2019
    ("12 Uneeda Dr", "Greenville", "S", "$105,000", "repeat"),     # 05/2019
    ("15 Heron Dr", "Fountain Inn", "B", "$169,500", "repeat"),    # 2019
    ("101 S. Valley Ln", "Greenville", "B", "$37,000"),            # 05/2019 lot
    ("213 Brannon Ave", "Greer", "S", "$109,000"),                 # 04/2019
    ("930 Harmony Rd", "Ware Shoals", "B", "$142,000"),            # 04/2019
    ("325 Rock Quarry Rd", "Travelers Rest", "B", "$95,000"),      # 2019
    ("117 New Castle Pl", "Simpsonville", "S", "$98,000"),         # 09/2018
    ("1671 Hampton Rd", "Inman", "B", "$112,000"),                 # 2018
    ("102 Old Grove Rd", "Piedmont", "B", "$133,500"),             # 08/24/2018 buyer Dineene D. Hicks (J.R. confirmed 10/23)
    ("308 Covington Dr", "Inman", "S", "$192,900"),                # 08/2018 contract price
    ("309 Holly Oaks Ln", "Inman", "B", "$296,600"),               # 07/2018
    ("316 Covington Dr", "Inman", "S", "$200,000"),                # 07/2018
    ("128 Bonnie Woods Dr", "Greenville", "B", "$153,000"),        # 05/2018
    ("110 Birdie Ln", "Fountain Inn", "S", "$69,900"),             # 05/2018
    ("12 Uneeda Dr", "Greenville", "B", "$104,000"),               # 05/2018
    ("702 Watermarke Ln", "Anderson", "B", "$300,000"),            # 03/2018
    ("210 Legacy Dr", "Inman", "S", "$183,800"),                   # 03/2018
    ("248 Page Creek Blvd", "Landrum", "B", "$234,000"),           # 2018 contract price
    ("115 James Rd", "Campobello", "B", "$178,400"),               # 12/2017
    ("215 Ashley Danielle Dr", "Duncan", "B", "$128,000"),         # 12/2017
    ("501 Thorington Ct", "Greer", "B", "$308,000", "repeat"),     # 09/2017
    ("407 Jewelwood Dr", "Lyman", "S", "$200,000", "repeat"),      # 2017
    ("318 Tearose Ln", "Simpsonville", "B", "$188,000", "referral"),  # 03/2017
    ("705 Cannon Ford Rd", "Inman", "B", "$45,700"),               # 2017
    ("516 Carey Dr", "Greer", "B", "$198,900"),                    # late 2016 contract price
    ("407 Jewelwood Dr", "Lyman", "B", "$198,500"),                # 08/2016
    ("2 Horseback Way", "Travelers Rest", "B", "$66,000"),         # 06/2016
    ("926 Winterhawk Cir", "Inman", "S", "$95,000"),               # 2016
]
REPEAT_FAMILIES = 10

REVIEWS = [
    {"quote": "Had a great first home buyers experience with this agent. He worked on my time frame and went over and above to get things going. I just closed on my first house and I couldn't have picked a better realtor! Thanks JR for all of your help! UPDATE: 4 years later I've chosen JR to help me sell my home. It's been an excellent experience. He uses a really neat drone for professional pictures for the listing. He is very prompt with every detail of the process. I'm very pleased and couldn't ask for a better realtor.",
     "quote_es": 'Tuve una gran experiencia como compradora de primera vivienda con este agente. Trabajó según mis tiempos y fue más allá para que todo avanzara. Acabo de cerrar la compra de mi primera casa y no pude haber elegido un mejor agente. ¡Gracias JR por toda tu ayuda! ACTUALIZACIÓN: 4 años después, elegí a JR para ayudarme a vender mi casa. Ha sido una experiencia excelente. Usa un dron muy bueno para tomar fotos profesionales de la propiedad. Es muy puntual con cada detalle del proceso. Estoy muy satisfecha y no podría pedir un mejor agente.',
     "name": "Brooke H.", "where": "bought, then sold"},
    {"quote": "JR did so much for me and my husband. JR was very punctual, able to be reached, willing to go the extra mile and was cheerful all the way through. We bought and sold and bought again from JR and the timing was like none other. It happened on same day where he told us bf closing of our new home that our old sold. So on the same day.. it was an awesome experience. He\u2019s very hard working and will go the extra mile (s)!!! I will not use another realtor as long as JR is around",
     "quote_es": 'JR hizo muchísimo por mí y por mi esposo. JR fue muy puntual, fácil de localizar, dispuesto a hacer un esfuerzo extra y de buen ánimo de principio a fin. Compramos, vendimos y volvimos a comprar con JR, y la coordinación fue como ninguna otra. Pasó el mismo día: antes del cierre de nuestra casa nueva nos avisó que la anterior ya se había vendido. Así que el mismo día... fue una experiencia increíble. Es muy trabajador y hace el esfuerzo extra (¡y más!). No usaré a otro agente mientras JR esté disponible.',
     "name": "Kerri H.", "where": "Google review"},
    {"quote": "J.R. Grimaldo helped my family more than I ever imagined and could ever repay. He not only got us into our dream home, he sold our home and my mother's home. He took care of all the details to make the selling process a breeze. J.R. was always there whenever we had questions or concerns. We will continue our relationship with J.R. for many years to come. We recommend J.R. to ANYONE looking to buy or sell.",
     "quote_es": 'J.R. Grimaldo ayudó a mi familia más de lo que jamás imaginé y más de lo que podría devolverle. No solo nos consiguió la casa de nuestros sueños, también vendió nuestra casa y la casa de mi madre. Se encargó de todos los detalles para que el proceso de venta fuera muy sencillo. J.R. siempre estuvo ahí cuando tuvimos preguntas o dudas. Seguiremos nuestra relación con J.R. por muchos años. Recomendamos a J.R. a CUALQUIERA que quiera comprar o vender.',
     "name": "Google reviewer", "where": "bought and sold"},
    {"quote": "A really great agent, if that is what you are searching for :) JR is a fantastic agent. He is very helpful and positive, as well as fair to everyone involved in the process. I always felt like we were in good hands with JR. As an agent he is always available, getting back to you if you have any questions or concerns in a prompt manner. I highly recommend JR as an agent. In our case he did take on a situation, manufactured homes in a place where residents don't actually own the land -- but do own their home -- despite not being that familiar with the arrangement. He caught on fast, was willing to tackle our situation and we had success. I guess in a nutshell JR takes a lot of the stress of selling or buying a home out of the process.",
     "quote_es": 'Un agente realmente excelente, si es eso lo que busca :) JR es un agente fantástico. Es muy servicial y positivo, y además justo con todos los involucrados en el proceso. Siempre sentí que estábamos en buenas manos con JR. Como agente siempre está disponible y responde pronto a cualquier pregunta o inquietud. Recomiendo mucho a JR como agente. En nuestro caso tomó una situación poco común: casas prefabricadas en un lugar donde los residentes no son dueños del terreno, pero sí de su casa, aunque no conocía bien ese tipo de arreglo. Aprendió rápido, estuvo dispuesto a tomar nuestro caso y tuvimos éxito. En resumen, JR le quita mucho del estrés a vender o comprar una casa.',
     "name": "Peter H.", "where": ""},
    {"quote": "I just wanted to thank you again for helping us so much! I was so against trying to sell our house until Rusty and Sarah sold and then \"poof!!\", they were moving. I truly appreciate you and what you did for us. God makes things happen at the right time and we couldn't be happier that we got everything completed in time for Mom to enjoy it.",
     "quote_es": 'Solo quería agradecerle otra vez por ayudarnos tanto. Yo estaba muy en contra de intentar vender nuestra casa, hasta que Rusty y Sarah vendieron la suya y, de pronto, ya se mudaban. De verdad le agradezco lo que hizo por nosotros. Dios hace que las cosas pasen en el momento correcto, y no podríamos estar más contentos de haber terminado todo a tiempo para que mamá lo disfrutara.',
     "name": "Darrell K.", "where": "seller"},
    {"quote": "JR was an excellent realtor to work with. Always on time, informative, professional and easy to communicate with. We had a great experience and would definitely recommend to our family and friends.",
     "quote_es": 'JR fue un agente excelente con quien trabajar. Siempre puntual, informativo, profesional y fácil de comunicarse. Tuvimos una gran experiencia y sin duda lo recomendaríamos a nuestra familia y amigos.',
     "name": "Slava S.", "where": ""},
    {"quote": "My wife and I were very pleased with J.R. Grimaldo's professionalism. He certainly is a credit to himself and his company!",
     "quote_es": 'Mi esposa y yo quedamos muy satisfechos con el profesionalismo de J.R. Grimaldo. Sin duda es un orgullo para él mismo y para su empresa.',
     "name": "Jeff D.", "where": "Google review"},
]

EN = {
    "lang": "en", "dir_prefix": "", "other_lang": "es", "other_label": "Español",
    "nav": [("index.html", "Home"), ("home-value.html", "What's My Home Worth"),
            ("listings.html", "My Listings"), ("sold.html", "Sold Homes"),
            ("about.html", "About J.R."), ("reviews.html", "Reviews"),
            ("free-books.html", "Free Books"), ("contact.html", "Contact Me")],
    "search_label": "Search Homes",
    "hero_h1": "Thinking about selling your Upstate home? Start with a real number.",
    "hero_p": "Tell me the address. Within one business day, I'll prepare your valuation myself. I look at your home and the recent sales around it. Not a computer guess.",
    "hero_btn": "Get my home's value",
    "hero_addr": "Your home address",
    "truths": [
        ("Prepared by me", "I look at your home and the recent sales nearby myself. Automatic estimates skip that step."),
        ("One business day", "You get a written valuation by email. Fast enough to plan with, careful enough to trust."),
        ("Free, no strings", "No fee and no obligation. Use it to plan, to refinance, or just to know."),
    ],
    "why_h2": "Quality over quantity.",
    "why_p": "I'd rather do a great job for each client than juggle as many as I can. Most of my clients are sellers. When you list with me, you're not one file in a stack.",
    "why_bullets": [
        "I answer most calls live, and texts right away or very soon after.",
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
    "hv_note": "I prepare every valuation myself. No computer, no assistant. I'm a licensed South Carolina REALTOR®. That's why it takes a day instead of a second.",
    # listings
    "li_h1": "My listings",
    "li_empty": "Nothing on the market under my name right now. New listings show up here first, before the postcards go out.",
    "li_mls": "MLS",
    "li_btn": "Details and photos",
    "so_h1": "Sold homes",
    "so_empty": "Recent sales will be listed here with their final prices. Ask me about any of them.",
    "so_intro": "Most of my business comes from past clients and the people they send my way. Here are recent sales, and which side I represented.",
    "so_story_h2": "Four homes, one agent.",
    "so_story": "C. and K. first bought a home with me in 2018. Since then they've come back three more times, in 2019, 2023, and 2024. Each time I sold the home they had and helped them buy the next one. Twice, we closed on the sale and the purchase on the same day.",
    "so_more_h2": "Every home I've helped sell and buy",
    "so_stats1": "homes sold and bought since 2016.",
    "so_stats2": "families have come back to work with me again.",
    "so_see_all": "See all {n} sales",
    "so_fine": "Newest first. The four homes above are included in the count.",
    "so_sides": {"S": "Sold for the seller", "B": "Represented the buyer", "SB": "Helped both buyer and seller"},
    "so_tags": {"repeat": "Repeat client", "referral": "Referred by a past client"},
    # about
    "ab_h1": "Principles Before Profits",
    "ab_p1": "Honesty and integrity are what you can expect when you hire me. I help people sell and buy homes across the Upstate, and I'm based in Landrum.",
    "ab_p2": "As your trusted advisor I offer a clear read on your situation, guide you through the process, and clear the landmines before they become problems. You'll have a skillful negotiator working for you every step of the way.",
    "ab_p3": "What separates me from other agents is my approach. I'm genuinely concerned with my client's best interest, and I'm relentless about solving whatever comes up between the signed contract and closing day. My clients tend to stay friends long after the keys change hands. Ten families have come back to buy or sell with me again, and others have sent their friends and family my way.",
    "ab_p4": "If you plan to sell your home and buy another one in the area, ask me how I can save you real money.",
    "ab_p5": "I am fluent in English and Spanish.",
    "ab_why_h2": "Here's why my clients keep coming back",
    "ab_why": [
        "I believe in quality over quantity. Every client gets my full attention, from the first call to the closing table. Most of them are sellers.",
        "Most of the buyers I work with are past clients, or friends and family they send my way.",
        "I'm the only one who answers my phone. I answer most calls when they come in. Texts get a reply right away, or very soon after.",
    ],
    "ab_facts_h2": "The details",
    "ab_facts": [
        ("Licensed", "South Carolina REALTOR® since 2016, SC License #95641"),  # licensed Feb 2016 (J.R.)
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
    "rv_ask": "Worked with me?",
    "rv_note": "",
    # contact
    "ct_h1": "Get in touch",
    "ct_p": "Call or text me directly. I answer most calls live. Texts get a reply right away, or very soon after. You won't be passed to an assistant or a call center.",
    "ct_call": "Call or text",
    "ct_email": "Email",
    "ct_office": "Office",
    "ct_form_h2": "Or send a note",
    "ct_fields": {"name": "Your name", "email": "Email", "phone": "Phone (optional)",
                  "message": "How can I help?", "submit": "Send"},
    # free books
    "bk_h1": "Free books on selling and buying a home",
    "bk_p": "These are my books. Pick the ones you want and I'll mail them to you. Free. No cost, no obligation, and no sales call.",
    "bk_pick": "Which books would you like? Check one or more.",
    "bk_more": "About this book",
    "bk_h1_one": "Free book: {title}",
    "bk_req_h2": "Get your free copy",
    "bk_req_p": "I'll mail it to you. Want the others too? Check them as well.",
    "bk_back": "All three books",
    "bk_p_over": "These are my books. Pick the one you want to know more about. Each page tells you what's in the book and lets you ask for a copy. I'll mail it to you. Free. No cost, no obligation, and no sales call.",
    "bk_fields": {"name": "Your name", "email": "Email", "phone": "Phone (optional)",
                  "street": "Street address", "city": "City", "state": "State", "zip": "ZIP",
                  "submit": "Mail me my books",
                  "fine": "Your information goes only to J.R. It is never sold or shared.",
                  "ok": "Thank you. Your books are on the way. Watch your mailbox over the next week or two.",
                  "need": "Please check at least one book."},
    "bk_after_h2": "What happens next",
    "bk_after": [
        "Your request lands in my inbox.",
        "I put your books in the mail, usually within a few days.",
        "That's it. If you ever want to talk about your home, call or text me. If not, enjoy the books.",
    ],
    "footer_rights": "All rights reserved.",
    "footer_eho": "Equal Housing Opportunity.",
}

ES = {
    "lang": "es", "dir_prefix": "es/", "other_lang": "en", "other_label": "English",
    "nav": [("index.html", "Inicio"), ("home-value.html", "¿Cuánto vale mi casa?"),
            ("listings.html", "Mis propiedades"), ("sold.html", "Casas vendidas"),
            ("about.html", "Sobre J.R."), ("reviews.html", "Opiniones"),
            ("free-books.html", "Libros gratis"), ("contact.html", "Contácteme")],
    "search_label": "Buscar casas",
    "hero_h1": "¿Piensa vender su casa en el Upstate? Empiece con un número real.",
    "hero_p": "Déme la dirección. En un día hábil, yo mismo le preparo su valuación. Reviso su casa y las ventas recientes a su alrededor. No es un cálculo de computadora.",
    "hero_btn": "Quiero saber el valor de mi casa",
    "hero_addr": "Dirección de su casa",
    "truths": [
        ("Preparada por mí", "Yo mismo reviso su casa y las ventas recientes cercanas. Los estimados automáticos se saltan ese paso."),
        ("Un día hábil", "Recibe una valuación por escrito en su correo. Rápida para planear, cuidadosa para confiar."),
        ("Gratis, sin compromiso", "Sin costo y sin obligación. Úsela para planear, para refinanciar, o solo para saber."),
    ],
    "why_h2": "Calidad antes que cantidad.",
    "why_p": "Prefiero hacer un gran trabajo para cada cliente que atender a todos los que pueda. La mayoría de mis clientes son vendedores. Cuando me contrata para vender, usted no es un expediente más en la pila.",
    "why_bullets": [
        "Contesto la mayoría de las llamadas en el momento, y los textos de inmediato o muy poco después.",
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
    "hv_note": "Yo mismo preparo cada valuación. Sin computadora, sin asistente. Soy REALTOR® con licencia en Carolina del Sur. Por eso toma un día y no un segundo.",
    "li_h1": "Mis propiedades",
    "li_empty": "Por ahora no tengo propiedades en venta a mi nombre. Las nuevas aparecen aquí primero, antes de que salgan las postales.",
    "li_mls": "MLS", "li_btn": "Detalles y fotos",
    "so_h1": "Casas vendidas",
    "so_empty": "Las ventas recientes aparecerán aquí con su precio final. Pregúnteme por cualquiera de ellas.",
    "so_intro": "La mayor parte de mi trabajo viene de clientes anteriores y de las personas que ellos me recomiendan. Aquí hay ventas recientes, y a qué lado representé.",
    "so_story_h2": "Cuatro casas, un solo agente.",
    "so_story": "C. y K. compraron su primera casa conmigo en 2018. Desde entonces han vuelto tres veces más, en 2019, 2023 y 2024. Cada vez vendí la casa que tenían y los ayudé a comprar la siguiente. Dos veces cerramos la venta y la compra el mismo día.",
    "so_more_h2": "Todas las casas que he ayudado a vender y comprar",
    "so_stats1": "casas vendidas y compradas desde 2016.",
    "so_stats2": "familias han vuelto a trabajar conmigo.",
    "so_see_all": "Ver las {n} ventas",
    "so_fine": "Las más recientes primero. Las cuatro casas de arriba están incluidas en el total.",
    "so_sides": {"S": "Representé al vendedor", "B": "Representé al comprador", "SB": "Ayudé al comprador y al vendedor"},
    "so_tags": {"repeat": "Cliente previo", "referral": "Recomendado por un cliente previo"},
    "ab_h1": "Principios Antes De Ganancias",
    "ab_p1": "Honestidad e integridad es lo que puede esperar cuando me contrata. Ayudo a vender y comprar casas en todo el Upstate, y vivo en Landrum.",
    "ab_p2": "Como su asesor de confianza, le doy una lectura clara de su situación, lo guío en el proceso, y quito los obstáculos antes de que sean problemas. Tendrá un negociador hábil trabajando para usted en cada paso.",
    "ab_p3": "Lo que me separa de otros agentes es mi forma de trabajar. Me importa de verdad el interés de mi cliente, y no descanso hasta resolver lo que surja entre la firma del contrato y el día del cierre. Mis clientes suelen seguir siendo amigos mucho después de recibir las llaves. Diez familias han vuelto a comprar o vender conmigo, y otros me han recomendado a sus amigos y familiares.",
    "ab_p4": "Si piensa vender su casa y comprar otra en la zona, pregúnteme cómo puedo ahorrarle dinero de verdad.",
    "ab_p5": "Hablo inglés y español con fluidez.",
    "ab_why_h2": "Por qué mis clientes regresan",
    "ab_why": [
        "Creo en la calidad antes que la cantidad. Cada cliente recibe toda mi atención, desde la primera llamada hasta el cierre. La mayoría son vendedores.",
        "La mayoría de los compradores con quienes trabajo son clientes anteriores, o amigos y familiares que ellos me recomiendan.",
        "Soy el único que contesta mi teléfono. Contesto la mayoría de las llamadas en el momento. Los textos reciben respuesta de inmediato, o muy poco después.",
    ],
    "ab_facts_h2": "Los datos",
    "ab_facts": [
        ("Licencia", "REALTOR® de Carolina del Sur desde 2016, SC License #95641"),
        ("Corredora", BRAND["brokerage"]),
        ("Vivo en", "Landrum, SC"),
        ("Zona de servicio", ", ".join(SITE["areas"])),
        ("Miembro", "Greater Greenville Association of REALTORS®, South Carolina Association of REALTORS®, National Association of REALTORS®"),
        ("Idiomas", "Inglés y español"),
    ],
    "rv_h1": "Opiniones",
    "rv_note": "Traducidas del inglés. Las opiniones originales están en la versión en inglés de esta página.",
    "rv_empty": "Estoy reuniendo opiniones de clientes. Si ha trabajado conmigo, le agradecería unas palabras.",
    "rv_btn": "Dejar una opinión",
    "rv_ask": "¿Trabajó conmigo?",
    "ct_h1": "Contacto",
    "ct_p": "Llámeme o envíeme un texto directamente. Contesto la mayoría de las llamadas en el momento. Los textos reciben respuesta de inmediato, o muy poco después. No lo pasarán a un asistente ni a un centro de llamadas.",
    "ct_call": "Llamar o texto", "ct_email": "Correo", "ct_office": "Oficina",
    "ct_form_h2": "O envíe un mensaje",
    "ct_fields": {"name": "Su nombre", "email": "Correo electrónico", "phone": "Teléfono (opcional)",
                  "message": "¿En qué puedo ayudarle?", "submit": "Enviar"},
    "bk_h1": "Libros gratis sobre vender y comprar una casa",
    "bk_p": "Estos son mis libros. Elija los que quiera y se los envío por correo. Gratis. Sin costo, sin compromiso y sin llamada de ventas. Los libros están escritos en inglés.",
    "bk_pick": "¿Qué libros quiere? Marque uno o más.",
    "bk_more": "Sobre este libro",
    "bk_h1_one": "Libro gratis: {title}",
    "bk_req_h2": "Pida su copia gratis",
    "bk_req_p": "Se la envío por correo. ¿Quiere los otros también? Márquelos.",
    "bk_back": "Los tres libros",
    "bk_p_over": "Estos son mis libros. Elija el que quiera conocer. Cada página explica qué trae el libro y le permite pedir una copia. Se la envío por correo. Gratis. Sin costo, sin compromiso y sin llamada de ventas. Los libros están escritos en inglés.",
    "bk_fields": {"name": "Su nombre", "email": "Correo electrónico", "phone": "Teléfono (opcional)",
                  "street": "Dirección", "city": "Ciudad", "state": "Estado", "zip": "Código postal",
                  "submit": "Envíenme mis libros",
                  "fine": "Su información llega solo a J.R. Nunca se vende ni se comparte.",
                  "ok": "Gracias. Sus libros van en camino. Revise su buzón en la próxima semana o dos.",
                  "need": "Por favor marque al menos un libro."},
    "bk_after_h2": "Qué pasa después",
    "bk_after": [
        "Su solicitud llega a mi correo.",
        "Pongo sus libros en el correo, normalmente en unos días.",
        "Eso es todo. Si algún día quiere hablar de su casa, llámeme o envíeme un texto. Si no, disfrute los libros.",
    ],
    "footer_rights": "Todos los derechos reservados.",
    "footer_eho": "Igualdad de oportunidades de vivienda.",
}

# The printed books J.R. has on hand (photographed 10/26/2026). All three are
# in English. Remove a book here when he runs out of copies.
BOOKS = [
    {"key": "How to Sell Homes Fast for Top Dollar", "slug": "free-book-sell-fast", "photo": "book-sellers.png",
     "title": "How to Sell Homes Fast for Top Dollar",
     "line": "For homeowners thinking about selling. How to price, prepare, and market a home so it sells quickly and for the most money.",
     "line_es": "Para dueños que piensan vender. Cómo poner el precio, preparar y promover una casa para que se venda rápido y por el mejor precio.",
     # CHECK AGAINST THE BOOK: general description, written before J.R. sent the table of contents.
     "about": [
         "Most homes that sell fast and for a strong price have three things in common. They were priced right from the first day. They were ready to show. And buyers heard about them.",
         "This book walks through each of those, in plain language. How to set a price buyers will act on. What to fix, clean, and clear out before the photos are taken, and what not to bother with. How a home gets in front of buyers today. And what to expect once the offers start, from the first negotiation to closing day.",
         "It's written for a homeowner who hasn't sold in a while, or has never sold at all. No jargon. Read it in an evening.",
     ],
     "about_es": [
         "La mayoría de las casas que se venden rápido y a buen precio tienen tres cosas en común. Tuvieron el precio correcto desde el primer día. Estaban listas para mostrarse. Y los compradores se enteraron de ellas.",
         "Este libro explica cada una de esas cosas, en lenguaje sencillo. Cómo poner un precio que haga actuar a los compradores. Qué arreglar, limpiar y sacar antes de las fotos, y en qué no vale la pena gastar. Cómo llega una casa a los compradores hoy. Y qué esperar cuando empiezan las ofertas, desde la primera negociación hasta el día del cierre.",
         "Está escrito para un dueño que no ha vendido en mucho tiempo, o que nunca ha vendido. Sin términos técnicos. Se lee en una tarde. El libro está en inglés.",
     ]},
    {"key": "Complete Guide to Buying a Home", "slug": "free-book-buying", "photo": "book-buyers.png",
     "title": "Complete Guide to Buying a Home",
     "line": "For anyone buying a home, first or next. What happens at each step, from getting pre-approved to closing day.",
     "line_es": "Para quien va a comprar una casa, la primera o la siguiente. Qué pasa en cada paso, desde la preaprobación hasta el día del cierre.",
     "about": [
         "Buying a home is a long list of steps, and most people only do it a few times in their life. This book puts the steps in order.",
         "It starts before the house hunt: what lenders look at, what a pre-approval is, and how much home you can really afford. Then the search itself, how to look at a house with a clear head, and what to do when you find the one. Then the part most people find confusing: the offer, the inspection, the appraisal, and all the paperwork between a signed contract and the keys.",
         "If you're buying your first home, this is the guide I wish every first-time buyer had read before we started. If you've bought before, it's a good refresher, because the process has changed.",
     ],
     "about_es": [
         "Comprar una casa es una lista larga de pasos, y la mayoría de la gente lo hace solo unas pocas veces en la vida. Este libro pone los pasos en orden.",
         "Empieza antes de buscar casa: qué revisan los prestamistas, qué es una preaprobación, y cuánta casa puede pagar en realidad. Luego la búsqueda, cómo ver una casa con la cabeza fría, y qué hacer cuando encuentra la suya. Después la parte que más confunde: la oferta, la inspección, el avalúo, y todo el papeleo entre el contrato firmado y las llaves.",
         "Si va a comprar su primera casa, esta es la guía que me gustaría que todo comprador leyera antes de empezar. Si ya ha comprado antes, es un buen repaso, porque el proceso ha cambiado. El libro está en inglés.",
     ]},
    {"key": "Expired!? A Guide for Selling Homes Others Couldn't Sell", "slug": "free-book-expired", "photo": "book-expired.png",
     "title": "Expired!? A Guide for Selling Homes Others Couldn't Sell",
     "line": "For owners whose home was listed and didn't sell. Why homes don't sell, and what to change the second time.",
     "line_es": "Para dueños cuya casa estuvo en venta y no se vendió. Por qué las casas no se venden, y qué cambiar la segunda vez.",
     "about": [
         "Your home was on the market. Buyers came through, or maybe they didn't. The listing ran out, and the home didn't sell. That's frustrating, and it's more common than people think.",
         "This book is about what went wrong, and what to do differently. It covers the usual reasons a home doesn't sell: the price, the condition, the photos, the marketing, and sometimes just timing. Then it walks through how to relist the right way, so the second try isn't a repeat of the first.",
         "It's a short, honest read. If your home didn't sell, read this before you sign with anyone again, including me.",
     ],
     "about_es": [
         "Su casa estuvo en venta. Vinieron compradores, o tal vez no. El contrato de venta terminó y la casa no se vendió. Es frustrante, y pasa más seguido de lo que la gente cree.",
         "Este libro trata de qué salió mal y qué hacer diferente. Cubre las razones comunes por las que una casa no se vende: el precio, la condición, las fotos, la promoción, y a veces simplemente el momento. Luego explica cómo volver a ponerla en venta de la forma correcta, para que el segundo intento no repita el primero.",
         "Es una lectura corta y honesta. Si su casa no se vendió, léalo antes de firmar con alguien otra vez, incluso conmigo. El libro está en inglés.",
     ]},
]

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
.brand{color:#fff;text-decoration:none;font-weight:600;font-size:1.2rem;letter-spacing:.01em;white-space:nowrap}
.brand small{display:block;font-weight:400;font-size:.8rem;opacity:.8}
nav.menu{display:none}
nav.menu a{color:#fff;text-decoration:none;margin-left:12px;font-size:.86rem;white-space:nowrap;border-bottom:2px solid transparent;padding:4px 0}
nav.menu a[aria-current]{border-color:var(--gold)}
nav.menu a.lang{border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:3px 10px;margin-left:16px}
.burger{background:none;border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:6px;padding:8px 10px;font:inherit;font-size:.95rem;cursor:pointer}
.topright{display:flex;align-items:center;gap:8px}
.lang-m{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:6px 12px;font-size:.92rem;white-space:nowrap}
.drawer{display:none;background:var(--ridge);padding:8px 0 14px}
.drawer.open{display:block}
.drawer a{display:block;color:#fff;text-decoration:none;padding:12px var(--gutter);border-top:1px solid rgba(255,255,255,.12);font-size:1.05rem}
.drawer a[aria-current]{color:#f3d58a}
@media(min-width:1240px){nav.menu{display:flex;align-items:center}.burger,.drawer,.topright{display:none!important}}
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
.sold-list .rep{display:inline-block;margin-left:6px;font-size:.78rem;font-weight:600;color:#fff;background:var(--ridge);border-radius:999px;padding:1px 8px}
.more-sold h2{margin-bottom:.3em}
.more-sold .stats{font-size:1.1rem;line-height:1.6}
.more-sold .stats b{font-size:1.35rem;color:var(--ridge-deep)}
.all-sales summary{cursor:pointer;display:inline-block;font-weight:600;color:var(--ridge);border:1px solid var(--ridge);border-radius:8px;padding:10px 18px;list-style:none}
.all-sales summary::-webkit-details-marker{display:none}
.all-sales[open] summary{margin-bottom:8px}
.sold-list{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:0;max-width:820px}
.sold-list li{display:grid;grid-template-columns:1fr auto;grid-template-areas:"a pr" "sd sd";gap:2px 16px;padding:12px 0;border-top:1px solid var(--line)}
.sold-list .a{grid-area:a}.sold-list .pr{grid-area:pr}.sold-list .sd{grid-area:sd}
.sold-list li:last-child{border-bottom:1px solid var(--line)}
.sold-list .a{font-weight:600}
.sold-list .c{color:var(--ink-2);font-weight:400}
.sold-list .pr{font-weight:600;color:var(--ridge-deep);text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.sold-list .sd{font-size:.9rem;color:var(--gold-ink)}
@media(min-width:640px){.sold-list li{grid-template-columns:1fr 300px 110px;grid-template-areas:"a sd pr";align-items:baseline}}
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
.books{display:grid;gap:18px;margin:0 0 6px}
@media(min-width:720px){.books{grid-template-columns:repeat(3,1fr)}}
.book{position:relative;display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:start;padding:14px;border:1.5px solid var(--line);border-radius:12px;background:#fff;cursor:pointer}
@media(min-width:720px){.book{grid-template-columns:1fr;text-align:center}.book img{margin:0 auto}}
.book img{width:96px;height:auto}
@media(min-width:720px){.book img{width:150px}}
.book:has(input:checked){border-color:var(--gold);background:#fbf6ea;box-shadow:0 0 0 2px var(--gold)}
form.sheet .book input[type=checkbox]{position:absolute;top:12px;right:12px;width:24px;height:24px;padding:0;accent-color:var(--gold-ink);margin:0}
@media(min-width:720px){form.sheet .book input[type=checkbox]{left:12px;right:auto}}
.book b{display:block;font-size:1.02rem;margin-bottom:4px}
.book span{display:block;font-size:.95rem;color:var(--ink-2)}
form.sheet .books label{display:grid}
.shelf{display:grid;gap:18px}
@media(min-width:720px){.shelf{grid-template-columns:repeat(3,1fr)}}
.shelf a{display:grid;gap:10px;padding:18px;border:1.5px solid var(--line);border-radius:12px;text-decoration:none;color:var(--ink);text-align:center;background:#fff}
.shelf a:hover{border-color:var(--gold);background:#fbf6ea}
.shelf img{width:170px;height:auto;margin:0 auto}
.shelf b{font-size:1.05rem}
.shelf span{font-size:.95rem;color:var(--ink-2)}
.shelf .go{color:var(--ridge);font-weight:600;text-decoration:underline;text-underline-offset:3px}
.bookhero{display:grid;gap:24px;align-items:start}
@media(min-width:800px){.bookhero{grid-template-columns:300px 1fr;gap:48px}}
.bookhero img{width:100%;max-width:320px;margin:0 auto}
.form-msg{padding:16px 18px;border-radius:8px;font-size:1.05rem;max-width:62ch;margin:0}
.form-msg.ok{background:#e6f1ea;color:#1d4a2e;border-left:4px solid #2f7a4a}
.form-msg.bad{background:#fbeaea;color:#6b1f1f;border-left:4px solid #b03a3a}
[hidden]{display:none!important}
.note{border-left:4px solid var(--gold);padding:12px 18px;background:var(--stone);max-width:62ch;margin:24px 0}
.note.story h2{font-size:1.3rem;margin:0 0 .3em}.note.story p{margin:0}
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
      if(form.dataset.need&&!form.querySelector('input[name=books]:checked')){
        msg.className='form-msg bad';msg.textContent=form.dataset.need;msg.hidden=false;
        form.querySelector('.books').scrollIntoView({block:'center'});return;
      }
      btn.disabled=true;btn.textContent=form.dataset.sending;
      var src=new FormData(form),fd=new FormData();
      try{
        var g=function(k){return (src.get(k)||'').toString().trim();};
        var r={t:form.id==='hv-form'?'v':(form.id==='bk-form'?'b':'c'),l:document.documentElement.lang==='es'?'es':'en',
               n:g('name'),p:g('phone'),e:g('email'),a:[g('address')||g('street'),g('city')].filter(Boolean).join(', ')};
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

def mail_form(T, lang, subject, fields_html, submit_label, form_id="", ok=None):
    """Formspree if an ID is set, otherwise a mailto that opens the visitor's mail app."""
    if SITE["formspree_id"]:
        ok_custom = ok
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
        if ok_custom:
            ok = ok_custom
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

import json as _json
AGENT_LD = _json.dumps({
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "name": "J.R. Grimaldo, REALTOR\u00ae",
    "url": "https://" + SITE["domain"] + "/",
    "image": "https://" + SITE["domain"] + "/assets/jr-headshot.jpg",
    "telephone": SITE["phone_tel"],
    "email": SITE["email"],
    "address": {"@type": "PostalAddress", "streetAddress": "148 Milestone Way, Suite D",
                "addressLocality": "Greenville", "addressRegion": "SC", "postalCode": "29615", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": a + ", SC"} for a in SITE["areas"]],
    "knowsLanguage": ["en", "es"],
    "slogan": "Principles Before Profits",
    "parentOrganization": {"@type": "RealEstateAgent", "name": BRAND["brokerage"]},
    "sameAs": SITE["profiles"],
}, ensure_ascii=False).replace("</", "<\\/")

def layout(T, page, title, body, lang_switch, desc=None, alt=None):
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
    root = "https://" + SITE["domain"] + "/"
    canon = root + p + ("" if page == "index.html" else page)
    hreflang = ""
    if alt is not None:
        en_url = canon if T["lang"] == "en" else root + ("" if alt == "index.html" else alt)
        es_url = canon if T["lang"] == "es" else root + "es/" + ("" if alt == "index.html" else alt)
        hreflang = (f'\n<link rel="alternate" hreflang="en" href="{en_url}">'
                    f'\n<link rel="alternate" hreflang="es" href="{es_url}">'
                    f'\n<link rel="alternate" hreflang="x-default" href="{en_url}">')
    towns_links = " · ".join(f'<a href="{up}{k}.html">{esc(TOWNS[k]["name"])}</a>' for k in TOWN_ORDER)
    towns_label = "Selling your home in" if T["lang"] == "en" else "Vender su casa en"
    return f"""<!doctype html>
<html lang="{T['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc or T['hero_p'])}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="J.R. Grimaldo, REALTOR®">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc or T['hero_p'])}">
<meta property="og:image" content="https://{SITE['domain']}/assets/share.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{canon}">
<link rel="canonical" href="{canon}">{hreflang}
<script type="application/ld+json">{AGENT_LD}</script>
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
      <p>{esc(towns_label)}: {towns_links}</p>
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
    es = T["lang"] == "es"
    role_t = it.get("role_es") if es and it.get("role_es") else it.get("role")
    line_t = it.get("line_es") if es and it.get("line_es") else it.get("line", "")
    price_t = it["price"]
    if es and price_t.startswith("Sold for "):
        price_t = "Vendida en " + price_t[len("Sold for "):]
    role = f'<p class="role">{esc(role_t)}</p>' if role_t else ""
    return f"""<article class="card">{phdiv}<div class="body">{role}
<p class="price">{esc(price_t)}</p><p class="addr-l">{esc(it['address'])}</p>
<p>{esc(line_t)}</p>{('<p class="mls">'+esc(it['mls'])+'</p>') if it.get('mls') else ''}
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

def _book_form(T, checked_key=None):
    F = T["bk_fields"]
    up = "../" if T["dir_prefix"] else ""
    es = T["lang"] == "es"
    picks = "".join(
        f'<label class="book"><img src="{up}assets/{b["photo"]}" alt="{esc(b["title"])}" width="396" height="601">'
        f'<div><b><input type="checkbox" name="books" value="{esc(b["key"])}"{" checked" if b["key"] == checked_key else ""}>{esc(b["title"])}</b>'
        f'<span>{esc(b["line_es"] if es else b["line"])}</span></div></label>' for b in BOOKS)
    fields = (
        f'<p class="fine" style="font-size:1.02rem;color:var(--ink)">{esc(T["bk_pick"])}</p>'
        f'<div class="books">{picks}</div>'
        + '<div class="two">' + field("name", F["name"], req=True) + field("email", F["email"], "email", req=True) + '</div>'
        + field("phone", F["phone"], "tel")
        + field("street", F["street"], req=True)
        + '<div class="three">' + field("city", F["city"], req=True)
        + f'<label>{esc(F["state"])}<input type="text" name="state" value="SC" required></label>'
        + field("zip", F["zip"], req=True) + '</div>'
        + f'<p class="fine">{esc(F["fine"])}</p>'
    )
    subj = "Free book request from " + SITE["domain"] if not es else "Solicitud de libro gratis desde " + SITE["domain"]
    form = mail_form(T, T["lang"], subj, fields, F["submit"], "bk-form", ok=F["ok"])
    return form.replace('<form ', f'<form data-need="{esc(F["need"])}" ', 1)

def page_books(T):
    """Overview: the three books, each linking to its own page."""
    up = "../" if T["dir_prefix"] else ""
    es = T["lang"] == "es"
    shelf = "".join(
        f'<a href="{b["slug"]}.html"><img src="{up}assets/{b["photo"]}" alt="" width="396" height="601">'
        f'<b>{esc(b["title"])}</b><span>{esc(b["line_es"] if es else b["line"])}</span>'
        f'<span class="go">{esc(T["bk_more"])}</span></a>' for b in BOOKS)
    return f"""
<section><div class="wrap"><h1>{esc(T['bk_h1'])}</h1><p>{esc(T['bk_p_over'])}</p>
<div class="shelf">{shelf}</div></div></section>"""

def page_book(T, b):
    """One book: what's in it, then the request form with this book pre-checked."""
    up = "../" if T["dir_prefix"] else ""
    es = T["lang"] == "es"
    about = "".join(f"<p>{esc(x)}</p>" for x in (b["about_es"] if es else b["about"]))
    steps = "".join(f'<li>{esc(x)}</li>' for x in T["bk_after"])
    return f"""
<section><div class="wrap"><p class="fine"><a href="free-books.html">&larr; {esc(T['bk_back'])}</a></p>
<div class="bookhero"><img src="{up}assets/{b["photo"]}" alt="{esc(b["title"])}" width="396" height="601">
<div><h1>{esc(T['bk_h1_one'].format(title=b['title']))}</h1>{about}
<p><a class="btn" href="#request">{esc(T['bk_req_h2'])}</a></p></div></div></div></section>
<section class="alt" id="request"><div class="wrap"><h2>{esc(T['bk_req_h2'])}</h2><p>{esc(T['bk_req_p'])}</p>{_book_form(T, b["key"])}</div></section>
<section><div class="wrap"><h2>{esc(T['bk_after_h2'])}</h2><ol class="steps">{steps}</ol></div></section>"""

def page_list(T, h1, items, empty, intro=""):
    cards = "".join(card(x, T) for x in items)
    body = f'<div class="cards">{cards}</div>' if items else f'<div class="empty"><p style="margin:0">{esc(empty)}</p></div>'
    lead = f'<p>{esc(intro)}</p>' if (intro and items) else ""
    return f'<section><div class="wrap"><h1>{esc(h1)}</h1>{lead}{body}</div></section>'

def page_sold(T=EN):
    base = page_list(T, T["so_h1"], SOLD, T["so_empty"], T["so_intro"])
    story = (f'<div class="note story"><h2>{esc(T["so_story_h2"])}</h2>'
             f'<p>{esc(T["so_story"])}</p></div>')
    # Chris Roberts and Kerri Hogan. J.R., 10/23/2026: husband's initial first; the
    # 2019 and 2023 moves closed the same day, the 2024 move did not.
    base = base.replace('<div class="cards">', story + '<div class="cards">', 1)
    if not SOLD_MORE:
        return base
    sides = T["so_sides"]
    tags = T["so_tags"]
    def row(r):
        a, c, sd, pr = r[:4]
        t = tags.get(r[4]) if len(r) > 4 else None
        tag = f' <span class="rep">{esc(t)}</span>' if t else ""
        return (f'<li><span class="a">{esc(a)}, <span class="c">{esc(c)}</span></span>'
                f'<span class="sd">{esc(sides[sd])}{tag}</span><span class="pr">{esc(pr)}</span></li>')
    rows = "".join(row(r) for r in SOLD_MORE)
    n = len(SOLD) + len(SOLD_MORE)
    more = (f'<div class="more-sold"><h2>{esc(T["so_more_h2"])}</h2>'
            f'<p class="stats"><b>{n}</b> {esc(T["so_stats1"])}<br>'
            f'<b>{REPEAT_FAMILIES}</b> {esc(T["so_stats2"])}</p>'
            f'<details class="all-sales"><summary>{esc(T["so_see_all"].format(n=n))}</summary>'
            f'<p class="fine">{esc(T["so_fine"])}</p>'
            f'<ul class="sold-list">{rows}</ul></details></div>')
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
<section class="alt"><div class="wrap"><h2>{esc(T['ab_why_h2'])}</h2>{"".join(f"<p>{esc(x)}</p>" for x in T["ab_why"])}</div></section>
<section><div class="wrap"><h2>{esc(T['ab_facts_h2'])}</h2><div class="facts">{facts}</div></div></section>"""

_WHERE_ES = {"bought, then sold": "compró, luego vendió", "Google review": "opinión en Google",
             "bought and sold": "compró y vendió", "seller": "vendedor"}
def _where(w, T):
    return _WHERE_ES.get(w, w) if T["lang"] == "es" else w

def page_reviews(T):
    if REVIEWS:
        note = f'<p class="fine">{esc(T["rv_note"])}</p>' if T.get("rv_note") else ""
        body = note + "".join(f'<blockquote><p>{esc(r["quote_es"] if T["lang"] == "es" and r.get("quote_es") else r["quote"])}</p><footer>{esc(r["name"])}{(", "+esc(_where(r["where"], T))) if r.get("where") else ""}</footer></blockquote>' for r in REVIEWS)
        body += f'<p>{esc(T["rv_ask"])} <a class="btn quiet" href="{SITE["review_page"]}">{esc(T["rv_btn"])}</a></p>'
    else:
        body = f'<div class="empty"><p>{esc(T["rv_empty"])}</p><a class="btn quiet" href="{SITE["review_page"]}">{esc(T["rv_btn"])}</a></div>'
    return f'<section><div class="wrap"><h1>{esc(T["rv_h1"])}</h1>{body}</div></section>'

# Town pages for local search ("sell my house in Greer"). Sales are pulled
# automatically from SOLD and SOLD_MORE, so a new sale shows up on its town page.
# Only J.R.'s real sales; no dates; no claims about other agents.
# J.R., 10/23/2026: "Go ahead and do anything ... to promote this."
TOWN_ORDER = ["landrum", "greer", "taylors", "greenville", "simpsonville", "inman", "travelers-rest", "fountain-inn"]
TOWNS = {
    "landrum": {"name": "Landrum",
        "intro": ["I live in Landrum, and I've been helping my neighbors here buy and sell homes since 2016.",
                  "When you sell with me, you get an agent who knows the streets, the neighborhoods, and what buyers here are looking for. I also work in the towns around us, including Campobello, Inman, and Lyman."],
        "note": "The same family on all three. They bought Page Creek with me, then came back years later to sell it and buy Talbert Trail."},
    "greer": {"name": "Greer"},
    "taylors": {"name": "Taylors"},
    "greenville": {"name": "Greenville"},
    "simpsonville": {"name": "Simpsonville"},
    "inman": {"name": "Inman"},
    "travelers-rest": {"name": "Travelers Rest"},
    "fountain-inn": {"name": "Fountain Inn"},
}
TOWN_HOW = [
    "A written valuation within one business day, prepared by me, not a computer.",
    "Drone photos and a mailing to your neighbors on every listing.",
    "Honest pricing, even when it isn't what you hoped to hear.",
    "I answer most calls live, and texts right away or very soon after.",
]
_SIDES = {"S": "Sold for the seller", "B": "Represented the buyer", "SB": "Helped both buyer and seller"}
_TAGS = {"repeat": "Repeat client", "referral": "Referred by a past client"}

def town_sales(name):
    rows = []
    for it in SOLD:
        parts = [x.strip() for x in it["address"].split(",")]
        if parts[1] == name:
            role = it["role"].split(" · ")
            rows.append((parts[0], role[0], it["price"].replace("Sold for ", ""), role[1] if len(role) > 1 else None))
    for r in SOLD_MORE:
        if r[1] == name:
            rows.append((r[0], _SIDES[r[2]], r[3], _TAGS.get(r[4]) if len(r) > 4 else None))
    return rows

def town_listings(name):
    return [x for x in LISTINGS if [p.strip() for p in x["address"].split(",")][1] == name]

def town_meta(key):
    t = TOWNS[key]; n = len(town_sales(t["name"]))
    title = f"Selling Your Home in {t['name']}, SC – J.R. Grimaldo, REALTOR®"
    if key == "landrum":
        desc = "J.R. Grimaldo lives in Landrum and has helped neighbors here buy and sell homes since 2016. Get a free home valuation, prepared by J.R. himself, within one business day."
    else:
        desc = (f"J.R. Grimaldo has helped clients buy and sell {n} homes in {t['name']}, SC. "
                "Get a free written home valuation, prepared by J.R. himself, within one business day.")
    return title, desc

def page_town(key):
    t = TOWNS[key]; name = t["name"]; sales = town_sales(name)
    if "intro" in t:
        intro_l = t["intro"]
    else:
        first = (f"I've been selling homes across the Upstate since 2016, and {name} is one of the places I've worked the most. I've helped clients buy and sell {len(sales)} homes here."
                 if len(sales) >= 5 else
                 f"I've been selling homes across the Upstate since 2016, and I've helped clients buy and sell {len(sales)} homes in {name}.")
        intro_l = [first,
                   "I believe in quality over quantity. Every client gets my full attention, and I'm the only one who answers my phone."]
    intro = "".join(f"<p>{esc(x)}</p>" for x in intro_l)
    def row(r):
        a, side, pr, tag = r
        tg = f' <span class="rep">{esc(tag)}</span>' if tag else ""
        return (f'<li><span class="a">{esc(a)}, <span class="c">{esc(name)}</span></span>'
                f'<span class="sd">{esc(side)}{tg}</span><span class="pr">{esc(pr)}</span></li>')
    rows = "".join(row(r) for r in sales)
    note = f'<p class="fine" style="margin-top:12px">{esc(t["note"])}</p>' if t.get("note") else ""
    lst = town_listings(name)
    lst_html = (f'<section><div class="wrap"><h2>For sale now in {esc(name)}</h2><div class="cards">'
                + "".join(card(x, EN) for x in lst) + '</div></div></section>') if lst else ""
    how = "".join(f"<li>{esc(x)}</li>" for x in TOWN_HOW)
    others = " · ".join(f'<a href="{k}.html">{esc(TOWNS[k]["name"])}</a>' for k in TOWN_ORDER if k != key)
    return f"""
<section><div class="wrap"><h1>Selling your home in {esc(name)}</h1>{intro}
<p><a class="btn" href="home-value.html">Get my free valuation</a></p></div></section>
{lst_html}
<section class="alt"><div class="wrap"><h2>My {esc(name)} sales</h2>
<ul class="sold-list">{rows}</ul>{note}
<p><a class="btn quiet" href="sold.html">See all my sales</a></p></div></section>
<section><div class="wrap"><h2>What you get when you sell with me</h2><ul class="plain">{how}</ul></div></section>
<section class="alt"><div class="wrap"><h2>What's your {esc(name)} home worth?</h2>
<p>Tell me the address. I'll look at your home and the recent sales around it, and send you a written valuation within one business day.</p>
<a class="btn" href="home-value.html">Get my free valuation</a>
<p class="fine" style="margin-top:22px">Other towns I work in: {others}</p></div></section>"""

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
  b:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your book request from my website. Your books go in the mail in the next few days. If you ever want to talk about your home, just text me here.",
     subj:"Your free books are on the way",
     mail:"Hi {first},\n\nThank you for asking for my books. I got your request, and they'll go in the mail to {addr} in the next few days.\n\nNo strings attached. If you ever want to talk about selling or buying a home, call or text me at 864-381-2326.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrinciples Before Profits"},
  c:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your message from my website. What's a good time to talk? You can also reach me right here by text.",
     subj:"Thanks for reaching out",
     mail:"Hi {first},\n\nThank you for your message. I got it and wanted you to know right away.\n\nWhat's a good time to talk? You can call or text me at 864-381-2326, or simply reply to this email.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrinciples Before Profits"}},
 es:{
  v:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su solicitud de valuación para {addr}. Ya estoy revisando las ventas recientes cerca de usted, y tendrá su valuación por correo en un día hábil. Si tiene alguna pregunta, escríbame aquí.",
     subj:"Su solicitud de valuación para {addr}",
     mail:"Hola {first}:\n\nGracias por pedirme la valuación de su casa en {addr}. Recibí su solicitud y ya estoy trabajando en ella.\n\nSoy agente con licencia en Carolina del Sur y preparo cada valuación personalmente. Voy a revisar las ventas recientes cerca de usted y los detalles de su casa, y le enviaré una valuación por escrito en un día hábil, con las ventas que usé para que vea el razonamiento.\n\nSi prefiere hablar antes, llámeme o escríbame al 864-381-2326.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrincipios Antes De Ganancias"},
  b:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su solicitud de libros desde mi página web. Sus libros salen por correo en los próximos días. Si algún día quiere hablar de su casa, escríbame aquí.",
     subj:"Sus libros gratis van en camino",
     mail:"Hola {first}:\n\nGracias por pedir mis libros. Recibí su solicitud, y salen por correo a {addr} en los próximos días.\n\nSin compromiso. Si algún día quiere hablar de vender o comprar una casa, llámeme o escríbame al 864-381-2326.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrincipios Antes De Ganancias"},
  c:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su mensaje desde mi página web. ¿A qué hora le queda bien que hablemos? También puede escribirme aquí.",
     subj:"Gracias por comunicarse",
     mail:"Hola {first}:\n\nGracias por su mensaje. Lo recibí y quería avisarle de inmediato.\n\n¿A qué hora le queda bien que hablemos? Puede llamarme o escribirme al 864-381-2326, o simplemente responder a este correo.\n\nJ.R. Grimaldo, REALTOR®\nNorthGroup Real Estate\n864-381-2326 | jr@jrresales.com\nPrincipios Antes De Ganancias"}}
};
var q=new URLSearchParams(location.hash.slice(1));
var d={t:q.get('t')==='c'?'c':(q.get('t')==='b'?'b':'v'),l:q.get('l')==='es'?'es':'en',n:q.get('n')||'',p:(q.get('p')||'').replace(/[^0-9+]/g,''),e:q.get('e')||'',a:q.get('a')||''};
var first=(d.n.split(/\s+/)[0]||'').replace(/^./,function(c){return c.toUpperCase();});
function fill(s){return s.replace(/\{first\}/g,first||(d.l==='es'?'':'there')).replace(/\{addr\}/g,d.a||(d.l==='es'?'su casa':'your home')).replace(/^Hola :/,'Hola:').replace(/^Hola ,/,'Hola,');}
function show(){
  var N=NOTES[d.l][d.t],tx=fill(N.text),sj=fill(N.subj),bd=fill(N.mail);
  document.documentElement.lang=d.l;
  document.getElementById('h').textContent=(d.l==='es'?'Responder a ':'Reply to ')+(d.n||'?');
  document.getElementById('who').textContent=[d.t==='v'?(d.l==='es'?'Solicitud de valuación':'Home value request'):d.t==='b'?(d.l==='es'?'Solicitud de libros':'Book request'):(d.l==='es'?'Mensaje':'Message'),d.a,d.p,d.e].filter(Boolean).join(' · ');
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
    (OUT / "defaultsite" / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/index.html"><link rel="canonical" href="https://jrresales.com/"><title>J.R. Grimaldo</title><a href="/index.html">Go to jrresales.com</a><script>location.replace("/index.html")</script>')
    (OUT / "CNAME").write_text(SITE["domain"] + "\n")
    # Search engines: list of public pages, and where to find it.
    base = "https://" + SITE["domain"] + "/"
    urls = ["", "home-value.html", "listings.html", "sold.html", "about.html", "reviews.html", "free-books.html", "contact.html",
            "es/", "es/home-value.html", "es/listings.html", "es/sold.html", "es/about.html", "es/reviews.html", "es/free-books.html", "es/contact.html"]
    urls += [b["slug"] + ".html" for b in BOOKS] + ["es/" + b["slug"] + ".html" for b in BOOKS] + [k + ".html" for k in TOWN_ORDER]
    import datetime as _dt
    today = _dt.date.today().isoformat()
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{base}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /reply.html\nDisallow: /defaultsite/\nSitemap: " + base + "sitemap.xml\n")
    (OUT / ".nojekyll").write_text("")

    t = "J.R. Grimaldo, REALTOR® – Sell Your Home in Landrum & the Upstate SC"
    n_sales = len(SOLD) + len(SOLD_MORE)
    D = {
        "index.html": "Thinking of selling in the Upstate? J.R. Grimaldo, a Landrum REALTOR® since 2016, prepares a free written home valuation himself within one business day.",
        "home-value.html": "Find out what your Upstate SC home is worth. J.R. Grimaldo prepares a free written valuation himself, from the recent sales near you, within one business day.",
        "listings.html": "Homes for sale now with J.R. Grimaldo, REALTOR®, in the Upstate SC.",
        "sold.html": f"{n_sales} homes sold and bought since 2016 in Greer, Taylors, Greenville, Simpsonville, Inman, Landrum, and across the Upstate SC. {REPEAT_FAMILIES} families have come back to work with J.R. again.",
        "about.html": "Meet J.R. Grimaldo, a Landrum-based South Carolina REALTOR® since 2016. Quality over quantity, quick replies, and clients who come back. Hablo español.",
        "reviews.html": "What clients say about buying and selling with J.R. Grimaldo, REALTOR®, in the Upstate SC.",
        "free-books.html": "Free books on selling and buying a home, mailed to you by J.R. Grimaldo, REALTOR® in Landrum, SC. No cost, no obligation, no sales call.",
        "contact.html": "Call or text J.R. Grimaldo at 864-381-2326. He answers most calls live and replies to texts right away. Landrum and Upstate SC Real Estate.",
    }
    DE = {
        "index.html": "¿Piensa vender en el Upstate? J.R. Grimaldo, REALTOR® desde 2016, le prepara una valuación gratis por escrito en un día hábil. Hablo español.",
        "home-value.html": "¿Cuánto vale su casa en el Upstate de Carolina del Sur? J.R. Grimaldo le prepara una valuación gratis por escrito, con las ventas recientes cerca de usted, en un día hábil.",
        "listings.html": "Casas en venta ahora con J.R. Grimaldo, REALTOR®, en el Upstate de Carolina del Sur. Hablo español.",
        "sold.html": f"{n_sales} casas vendidas y compradas desde 2016 en Greer, Taylors, Greenville, Simpsonville, Inman, Landrum y todo el Upstate de Carolina del Sur. {REPEAT_FAMILIES} familias han vuelto a trabajar con J.R.",
        "about.html": "Conozca a J.R. Grimaldo, REALTOR® de Carolina del Sur desde 2016, con base en Landrum. Calidad antes que cantidad y respuestas rápidas. Hablo español.",
        "reviews.html": "Lo que dicen los clientes de comprar y vender con J.R. Grimaldo, REALTOR®, en el Upstate de Carolina del Sur.",
        "free-books.html": "Libros gratis sobre vender y comprar una casa, enviados por correo por J.R. Grimaldo, REALTOR® en Landrum, SC. Sin costo ni compromiso.",
        "contact.html": "Llame o envíe un texto a J.R. Grimaldo al 864-381-2326. Contesta la mayoría de las llamadas en el momento. Bienes raíces en Landrum y el Upstate.",
    }
    # English: (title, body, language switch, Spanish twin or None)
    pages = {
        "index.html": (t, page_home(EN), "es/index.html", "index.html"),
        "home-value.html": ("What's My Home Worth? Free Home Valuation – " + SITE["agent"], page_home_value(EN), "es/home-value.html", "home-value.html"),
        "listings.html": ("My Listings – " + SITE["agent"] + ", REALTOR®", page_list(EN, EN["li_h1"], LISTINGS, EN["li_empty"]), "es/listings.html", "listings.html"),
        "sold.html": ("Sold Homes – " + SITE["agent"] + ", REALTOR®", page_sold(EN), "es/sold.html", "sold.html"),
        "about.html": ("About J.R. Grimaldo, REALTOR® – Landrum, SC", page_about(EN), "es/about.html", "about.html"),
        "reviews.html": ("Client Reviews – " + SITE["agent"] + ", REALTOR®", page_reviews(EN), "es/reviews.html", "reviews.html"),
        "free-books.html": ("Free Books on Selling and Buying a Home – " + SITE["agent"], page_books(EN), "es/free-books.html", "free-books.html"),
        "contact.html": ("Contact J.R. Grimaldo, REALTOR®", page_contact(EN), "es/contact.html", "contact.html"),
    }
    for b in BOOKS:
        n = b["slug"] + ".html"
        pages[n] = ("Free Book: " + b["title"] + " – " + SITE["agent"], page_book(EN, b), "es/" + n, n)
        D[n] = b["line"] + " Free, mailed to you by J.R. Grimaldo, REALTOR® in Landrum, SC."
    for name, (title, body, sw, alt) in pages.items():
        (OUT / name).write_text(layout(EN, name, title, body, sw, D[name], alt))
    for k in TOWN_ORDER:
        title, desc = town_meta(k)
        (OUT / (k + ".html")).write_text(layout(EN, k + ".html", title, page_town(k), "es/index.html", desc))
    # Spanish
    es_pages = {
        "index.html": ("J.R. Grimaldo, REALTOR® – Venda su casa en el Upstate de Carolina del Sur", page_home(ES), "../index.html"),
        "home-value.html": ("¿Cuánto vale mi casa? Valuación gratis – " + SITE["agent"], page_home_value(ES), "../home-value.html"),
        "listings.html": ("Mis propiedades – " + SITE["agent"] + ", REALTOR®", page_list(ES, ES["li_h1"], LISTINGS, ES["li_empty"]), "../listings.html"),
        "sold.html": ("Casas vendidas – " + SITE["agent"] + ", REALTOR®", page_sold(ES), "../sold.html"),
        "about.html": ("Sobre J.R. Grimaldo, REALTOR® – Landrum, SC", page_about(ES), "../about.html"),
        "reviews.html": ("Opiniones de clientes – " + SITE["agent"] + ", REALTOR®", page_reviews(ES), "../reviews.html"),
        "free-books.html": ("Libros gratis sobre vender y comprar una casa – " + SITE["agent"], page_books(ES), "../free-books.html"),
        "contact.html": ("Contácteme – " + SITE["agent"] + ", REALTOR®", page_contact(ES), "../contact.html"),
    }
    for b in BOOKS:
        n = b["slug"] + ".html"
        es_pages[n] = ("Libro gratis: " + b["title"] + " – " + SITE["agent"], page_book(ES, b), "../" + n)
        DE[n] = b["line_es"] + " Gratis, enviado por correo por J.R. Grimaldo, REALTOR® en Landrum, SC."
    for name, (title, body, sw) in es_pages.items():
        (OUT / "es" / name).write_text(layout(ES, name, title, body, sw, DE[name], name))
    print("built", len(pages) + len(es_pages) + len(TOWN_ORDER), "pages into", OUT)

if __name__ == "__main__":
    build()
