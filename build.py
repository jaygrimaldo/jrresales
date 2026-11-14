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
    "office": "P.O. Box 106, Landrum, SC 29356",
    "broker_in_charge": "Rick Markowski, Broker-in-Charge",
    "brokerage_site": "https://jrgrimaldo.northgroupre.com",
}

SITE = {
    "domain": "jrresales.com",
    "agent": "J.R. Grimaldo",
    "title_tag": "J.R. Grimaldo, Real Estate Professional – Upstate SC",
    "license": "SC License #95641",
    "phone": "864-381-2326",
    "phone_tel": "+18643812326",
    "email": "jr@jrREsales.com",
    "home_town": "Landrum, SC",
    # J.R.'s focus area (10/27/2026). He still takes listings elsewhere.
    "areas": ["Landrum", "Campobello", "Inman", "Boiling Springs", "Greer", "Lyman",
              "Duncan", "Wellford", "Travelers Rest", "Taylors"],
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
        # Temporarily off the market (J.R., 10/27/2026) until the tenants leave
        # 11/30/2026. He may not advertise it while it is off the market, so it
        # was hidden 10/27; J.R. then chose to show it with a banner instead.
        # Delete this line when it is back on the market.
        "off_market": True,
    },
    {
        "address": "207 Penrith Ct, Simpsonville, SC 29681",
        "price": "$352,999",
        "role": "Repeat client",  # Berhane bought 1220 Cyndis Ln with J.R. in 2025, then listed Penrith
        "role_es": "Cliente previo",
        "line": "Investor opportunity: leased through May 31, 2027. The buyer takes over the lease. Four bedrooms, two and a half baths, about 1,980 sq ft on a cul-de-sac in Villages at Windsor. New roof in late 2024.",
        "line_es": "Oportunidad para inversionistas: rentada hasta el 31 de mayo de 2027. El comprador asume el contrato de alquiler. Cuatro recámaras, dos baños y medio, unos 1,980 pies cuadrados en una calle cerrada en Villages at Windsor. Techo nuevo a finales de 2024.",
        "mls": "Greenville MLS 1567172",
        "link": "https://jrgrimaldo.northgroupre.com/property/63-1567172-207-penrith-court-simpsonville-SC-29681",
        "photo": "207-penrith-ct.jpg",
    },
]

# Listings marked off_market still show (J.R.'s decision, 10/27/2026) but
# carry a "Temporarily off the market" banner across the photo, and come
# after the on-market listings.
ALL_LISTINGS = LISTINGS
LISTINGS = sorted(ALL_LISTINGS, key=lambda x: bool(x.get("off_market")))

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
            ("free-books.html", "Free Guides & Books"), ("sold.html", "Sold Homes"),
            ("reviews.html", "Reviews"), ("about.html", "About J.R."),
            ("contact.html", "Contact Me"), ("newsletter.html", "Newsletter"),
            ("listings.html", "My Listings")],
    "search_label": "Search Homes",
    "hero_h1": "Thinking about selling your Upstate home? Start with a real number.",
    "hero_p": "Tell me the address. Within one business day, I'll prepare your valuation myself. I look at your home and the recent sales around it. Not a computer guess.",
    "hero_btn": "Get my home's value",
    "hero_addr": "Your home address",
    "truths": [
        ("Prepared by me", "I look at your home and the recent sales nearby myself. Automatic estimates skip that step."),
        ("One business day", "You get a written valuation by email. Fast enough to plan with, careful enough to trust."),
        ("Free, no strings", "No fee and no obligation. Use it to plan, or just to know."),
    ],
    "why_h2": "Quality over quantity.",
    "why_p": "I'd rather do a great job for each client than juggle as many as I can. Most of my clients are sellers. When you list with me, you're not one file in a stack.",
    "why_bullets": [
        "Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message.",
        "Honest pricing, even when it isn't what you hoped to hear.",
        "A negotiator on your side from the first offer to the closing table.",
        "Drone photos and a neighbor mailing on every listing.",
        "Fluent in English and Spanish.",
    ],
    "why_btn": "More about J.R.",
    "listings_h2": "On the market now",
    "listings_btn": "See all my listings",
    "cta_h2": "Ready to talk it through?",
    "cta_p": "Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message. No pressure, no script.",
    "cta_btn": "Text J.R.",
    "hero_who": "J.R. Grimaldo, Real Estate Professional",
    "hero_where": "Landrum, SC · Hablo español",
    "hero_call": "Text 864-381-2326. Fastest way to reach me.",
    "text_btn": "Text J.R. at 864-381-2326",
    "text_fast": "Fastest way to reach me.",
    "val_btn": "Get my home's value",
    "hm_sold_h2": "Recently sold",
    "hm_sold_p": "A few of the homes I've sold for my clients.",
    "hm_sold_btn": "See all my sales",
    "hm_books_h2": "Free Guides & Books",
    "hm_books_p": "My Seller's Guide walks you through a home sale, step by step. I'll email it to you. I also have two short printed books, one on selling and one for homes that didn't sell the first time. I'll mail those. No cost, no obligation.",
    "hm_books_btn": "See the guides and books",
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
        "fine": "You'll also get my monthly newsletter. I never sell your information. I use it only to answer you and to send what you asked for.",
    },
    "hv_after_h2": "What happens next",
    # Required by SC Code 40-60-30(1) (checked on scstatehouse.gov 11/13/2026).
    "hv_law": "This is a Real Estate agent's opinion of value, not an appraisal. This valuation service may not be used for the purposes of obtaining financing in a federally related transaction.",
    "hv_after": [
        "Your request lands in my inbox.",
        "I pull the comparable sales and look at your home's details.",
        "You get a written valuation by email within one business day, with the sales I used so you can see the reasoning.",
    ],
    "hv_note": "I prepare every valuation myself. It is not an automatic estimate. I'm a licensed South Carolina Real Estate Professional. That's why it takes a day instead of a second.",
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
    "so_see_all": "See the rest of my sales",
    "so_fine": "Newest first.",
    "so_sides": {"S": "Sold for the seller", "B": "Represented the buyer", "SB": "Helped both buyer and seller"},
    "so_tags": {"repeat": "Repeat client", "referral": "Referred by a past client"},
    # about
    "ab_h1": "Principles Before Profits",
    "ab_p1": "Honesty and integrity are what you can expect when you hire me. I help people sell and buy homes across the Upstate, and I'm based in Landrum.",
    "ab_p2": "I give you a clear read on your situation, guide you through each step, and deal with problems before they grow. I negotiate for you from the first offer to closing.",
    "ab_p3": "Here's how I work. I'm genuinely concerned with my clients' best interest, and I don't let up on whatever comes up between the signed contract and closing day. My clients tend to stay friends long after the keys change hands. Ten families have come back to buy or sell with me again, and others have sent their friends and family my way.",
    "ab_p4": "If you plan to sell your home and buy another one in the area, ask me how I can save you real money.",
    "ab_p5": "I am fluent in English and Spanish.",
    "ab_why_h2": "Here's why my clients keep coming back",
    "ab_why": [
        "I believe in quality over quantity. Every client gets my full attention, from the first call to the closing table. Most of them are sellers.",
        "Most of the buyers I work with are past clients, or friends and family they send my way.",
        "Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message.",
    ],
    "ab_facts_h2": "The details",
    "ab_facts": [
        ("Licensed", "Licensed South Carolina Real Estate Professional since 2016, SC License #95641"),  # licensed Feb 2016 (J.R.)
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
    "ct_p": "Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message. You won't be passed to an assistant or a call center.",
    "ct_call": "Text me (fastest)",
    "ct_email": "Email",
    "ct_office": "Mailing address",
    "ct_fine": "You'll also get my monthly newsletter. I never sell your information. I use it only to answer you and to send what you asked for.",
    "ct_form_h2": "Or send a note",
    "ct_fields": {"name": "Your name", "email": "Email", "phone": "Phone (optional)",
                  "message": "How can I help?", "submit": "Send"},
    # free books
    "bk_h1": "Free Guides & Books",
    "bk_p": "These are my books. Pick the ones you want and I'll mail them to you. Free. No cost, no obligation, and no sales call.",
    "bk_pick": "Which books would you like? Check one or more.",
    "bk_more": "About this book",
    "bk_h1_one": "Free book: {title}",
    "bk_req_h2": "Get your free copy",
    "bk_req_p": "I'll mail it to you. Want the others too? Check them as well.",
    "bk_back": "All guides and books",
    "bk_p_over": "Pick the one you want to know more about. Each page tells you what's inside and lets you ask for a copy. My two guides come by email. The two books are printed and mailed to you. All free, with no cost and no obligation.",
    "bk_fields": {"name": "Your name", "email": "Email", "phone": "Phone (optional)",
                  "street": "Street address", "city": "City", "state": "State", "zip": "ZIP",
                  "submit": "Mail me my books",
                  "fine": "You'll also get my monthly newsletter. I never sell your information. I use it only to answer you and to send what you asked for.",
                  "ok": "Thank you. I got your request. I'll mail it to you myself in the next few days.",
                  "need": "Please check at least one book."},
    # newsletter
    "nl_h1": "My monthly newsletter",
    "nl_p": "The first Wednesday of each month, I send a short email about homes in our part of the Upstate: what homes are selling for in our towns, whether sales are up or down, where mortgage rates stand, and a tip or two for homeowners. It's free, and you can stop it anytime.",
    "nl_sign_h2": "Get it by email",
    "nl_fields": {"name": "Your name", "email": "Email", "submit": "Sign me up",
                  "fine": "I never sell your information. I use it only to answer you and to send what you asked for.",
                  "ok": "Thank you. You're on the list. Watch for my next newsletter in your inbox."},
    "nl_past_h2": "Past issues",
    "nl_empty": "The first issue is coming soon. Sign up above and it will come straight to your inbox.",
    "nl_back": "All newsletters",
    "bk_after_h2": "What happens next",
    "bk_after": [
        "Your request lands in my inbox.",
        "I put your books in the mail, usually within a few days.",
        "That's it. If you ever want to talk about your home, text me at 864-381-2326. If not, enjoy the books.",
    ],
    "footer_rights": "All rights reserved.",
    "footer_eho": "Equal Housing Opportunity.",
}

ES = {
    "lang": "es", "dir_prefix": "es/", "other_lang": "en", "other_label": "English",
    "nav": [("index.html", "Inicio"), ("home-value.html", "¿Cuánto vale mi casa?"),
            ("free-books.html", "Guías y libros gratis"), ("sold.html", "Casas vendidas"),
            ("reviews.html", "Opiniones"), ("about.html", "Sobre J.R."),
            ("contact.html", "Contácteme"), ("newsletter.html", "Boletín"),
            ("listings.html", "Mis propiedades")],
    "search_label": "Buscar casas",
    "hero_h1": "¿Piensa vender su casa en el Upstate? Empiece con un número real.",
    "hero_p": "Deme la dirección. En un día hábil, yo mismo le preparo su valuación. Reviso su casa y las ventas recientes a su alrededor. No es un cálculo de computadora.",
    "hero_btn": "Quiero saber el valor de mi casa",
    "hero_addr": "Dirección de su casa",
    "truths": [
        ("Preparada por mí", "Yo mismo reviso su casa y las ventas recientes cercanas. Los estimados automáticos se saltan ese paso."),
        ("Un día hábil", "Recibe una valuación por escrito en su correo. Rápida para planear, cuidadosa para confiar."),
        ("Gratis, sin compromiso", "Sin costo y sin obligación. Úsela para planear, o solo para saber."),
    ],
    "why_h2": "Calidad antes que cantidad.",
    "why_p": "Prefiero hacer un gran trabajo para cada cliente que atender a todos los que pueda. La mayoría de mis clientes son vendedores. Cuando me contrata para vender, usted no es un expediente más en la pila.",
    "why_bullets": [
        "Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje.",
        "Precios honestos, aunque no sea lo que esperaba oír.",
        "Un negociador de su lado desde la primera oferta hasta el cierre.",
        "Fotos con dron y envío postal a los vecinos en cada propiedad.",
        "Hablo inglés y español.",
    ],
    "why_btn": "Más sobre J.R.",
    "listings_h2": "En venta ahora",
    "listings_btn": "Ver todas mis propiedades",
    "cta_h2": "¿Listo para conversar?",
    "cta_p": "Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje. Sin presión.",
    "cta_btn": "Enviar texto a J.R.",
    "hero_who": "J.R. Grimaldo, Profesional de Bienes Raíces",
    "hero_where": "Landrum, SC · Hablo español",
    "hero_call": "Envíe un texto al 864-381-2326. Es lo más rápido.",
    "text_btn": "Envíe un texto a J.R. al 864-381-2326",
    "text_fast": "Es lo más rápido.",
    "val_btn": "Quiero saber el valor de mi casa",
    "hm_sold_h2": "Vendidas recientemente",
    "hm_sold_p": "Algunas de las casas que he vendido para mis clientes.",
    "hm_sold_btn": "Ver todas mis ventas",
    "hm_books_h2": "Guías y libros gratis",
    "hm_books_p": "Mi guía para vendedores le explica la venta de una casa, paso a paso, y está en español. Se la envío por correo electrónico. También tengo dos libros cortos impresos, en inglés: uno sobre vender y otro para casas que no se vendieron la primera vez. Esos se los envío por correo. Sin costo ni compromiso.",
    "hm_books_btn": "Ver las guías y libros",
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
        "fine": "También recibirá mi boletín mensual. Nunca vendo su información. La uso solo para contestarle y enviarle lo que pidió.",
    },
    "hv_after_h2": "Qué pasa después",
    # Required by SC Code 40-60-30(1); the law's sentence is also given in English, word for word.
    "hv_law": "Esta es la opinión de valor de un agente de bienes raíces, no un appraisal (el informe de valor que pide el banco). Este servicio de valuación no se puede usar para obtener financiamiento en una transacción relacionada con el gobierno federal. En inglés, como lo dice la ley: <i lang=\"en\">This valuation service may not be used for the purposes of obtaining financing in a federally related transaction.</i>",
    "hv_after": [
        "Su solicitud llega a mi correo.",
        "Busco las ventas comparables y reviso los detalles de su casa.",
        "Recibe una valuación por escrito en un día hábil, con las ventas que usé para que vea el razonamiento.",
    ],
    "hv_note": "Yo mismo preparo cada valuación. No es un cálculo automático. Soy Profesional de Bienes Raíces con licencia en Carolina del Sur. Por eso toma un día y no un segundo.",
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
    "so_see_all": "Ver el resto de mis ventas",
    "so_fine": "Las más recientes primero.",
    "so_sides": {"S": "Representé al vendedor", "B": "Representé al comprador", "SB": "Ayudé al comprador y al vendedor"},
    "so_tags": {"repeat": "Cliente previo", "referral": "Recomendado por un cliente previo"},
    "ab_h1": "Principios Antes De Ganancias",
    "ab_p1": "Honestidad e integridad es lo que puede esperar cuando me contrata. Ayudo a vender y comprar casas en todo el Upstate, y vivo en Landrum.",
    "ab_p2": "Le doy una idea clara de su situación, lo guío en cada paso y me ocupo de los problemas antes de que crezcan. Negocio por usted desde la primera oferta hasta el cierre.",
    "ab_p3": "Así trabajo yo. Me importa de verdad el interés de mis clientes, y no me detengo ante nada de lo que surja entre la firma del contrato y el día del cierre. Mis clientes suelen seguir siendo amigos mucho después de recibir las llaves. Diez familias han vuelto a comprar o vender conmigo, y otros me han recomendado a sus amigos y familiares.",
    "ab_p4": "Si piensa vender su casa y comprar otra en la zona, pregúnteme cómo puedo ahorrarle dinero de verdad.",
    "ab_p5": "Hablo inglés y español con fluidez.",
    "ab_why_h2": "Por qué mis clientes regresan",
    "ab_why": [
        "Creo en la calidad antes que la cantidad. Cada cliente recibe toda mi atención, desde la primera llamada hasta el cierre. La mayoría son vendedores.",
        "La mayoría de los compradores con quienes trabajo son clientes anteriores, o amigos y familiares que ellos me recomiendan.",
        "Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje.",
    ],
    "ab_facts_h2": "Los datos",
    "ab_facts": [
        ("Licencia", "Profesional de Bienes Raíces con licencia en Carolina del Sur desde 2016, Licencia de SC #95641"),
        ("Agencia", BRAND["brokerage"]),
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
    "ct_p": "Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje. No lo pasarán a un asistente ni a un centro de llamadas.",
    "ct_fine": "También recibirá mi boletín mensual. Nunca vendo su información. La uso solo para contestarle y enviarle lo que pidió.",
    "ct_call": "Mensaje de texto (lo más rápido)", "ct_email": "Correo", "ct_office": "Dirección postal",
    "ct_form_h2": "O envíe un mensaje",
    "ct_fields": {"name": "Su nombre", "email": "Correo electrónico", "phone": "Teléfono (opcional)",
                  "message": "¿En qué puedo ayudarle?", "submit": "Enviar"},
    "bk_h1": "Guías y libros gratis",
    "bk_p": "Estos son mis libros. Elija los que quiera y se los envío por correo. Gratis. Sin costo, sin compromiso y sin llamada de ventas. Los libros están escritos en inglés.",
    "bk_pick": "¿Qué libros quiere? Marque uno o más.",
    "bk_more": "Sobre este libro",
    "bk_h1_one": "Libro gratis: {title}",
    "bk_req_h2": "Pida su copia gratis",
    "bk_req_p": "Se la envío por correo. ¿Quiere los otros también? Márquelos.",
    "bk_back": "Todas las guías y libros",
    "bk_p_over": "Elija el que quiera conocer. Cada página explica qué trae y le permite pedir una copia. Mis dos guías se las envío por correo electrónico: la guía para vendedores está en español, y la guía para dueños que venden por su cuenta está en inglés. Los dos libros están en inglés, y se los envío impresos por correo. Todo es gratis, sin costo y sin compromiso.",
    "bk_fields": {"name": "Su nombre", "email": "Correo electrónico", "phone": "Teléfono (opcional)",
                  "street": "Dirección", "city": "Ciudad", "state": "Estado", "zip": "Código postal",
                  "submit": "Envíenme mis libros",
                  "fine": "También recibirá mi boletín mensual. Nunca vendo su información. La uso solo para contestarle y enviarle lo que pidió.",
                  "ok": "Gracias. Recibí su solicitud. Yo mismo se lo envío por correo en los próximos días.",
                  "need": "Por favor marque al menos un libro."},
    "nl_h1": "Mi boletín mensual",
    "nl_p": "El primer miércoles de cada mes, envío un correo corto sobre las casas en nuestra parte del Upstate: en cuánto se venden las casas en nuestros pueblos, si las ventas suben o bajan, cómo están las tasas de hipoteca, y un consejo o dos para los dueños de casa. Es gratis, y puede cancelarlo cuando quiera. El boletín está en inglés.",
    "nl_sign_h2": "Recíbalo por correo",
    "nl_fields": {"name": "Su nombre", "email": "Correo electrónico", "submit": "Inscribirme",
                  "fine": "Nunca vendo su información. La uso solo para contestarle y enviarle lo que pidió.",
                  "ok": "Gracias. Ya está en la lista. Busque mi próximo boletín en su correo."},
    "nl_past_h2": "Boletines anteriores",
    "nl_empty": "El primer boletín sale pronto. Inscríbase arriba y le llegará directo a su correo.",
    "nl_back": "Todos los boletines",
    "bk_after_h2": "Qué pasa después",
    "bk_after": [
        "Su solicitud llega a mi correo.",
        "Pongo sus libros en el correo, normalmente en unos días.",
        "Eso es todo. Si algún día quiere hablar de su casa, envíeme un texto al 864-381-2326. Si no, disfrute los libros.",
    ],
    "footer_rights": "Todos los derechos reservados.",
    "footer_eho": "Igualdad de oportunidades de vivienda.",
}

# The printed books J.R. offers (photographed 10/26/2026). All are in English.
# Remove a book here when he runs out of copies. "Complete Guide to Buying a Home"
# was taken off 10/26/2026: J.R. wants the site to draw sellers, not buyers.
# Its cover image (book-buyers.png) is kept in assets in case he wants it back.
BOOKS = [
    # Descriptions rewritten 10/26/2026 from the books' real tables of contents
    # (J.R. sent photos) and approved by J.R. Publisher claims in chapter titles
    # ("15% more money," "20% rule," "without dropping the price") are left out
    # on purpose: on J.R.'s site they would read as his promises.
    {"key": "How to Sell Homes Fast for Top Dollar", "slug": "free-book-sell-fast", "photo": "book-sellers.png",
     "title": "How to Sell Homes Fast for Top Dollar",
     "line": "For homeowners thinking about selling. How to get your home ready, find buyers, and negotiate the best price.",
     "line_es": "Para dueños que piensan vender. Cómo preparar su casa, encontrar compradores y negociar el mejor precio.",
     "about": [
         "This book walks you through selling your home in the order it happens. It starts with the first steps. Then it covers getting the house ready, getting it in front of buyers, and getting the best deal.",
         "Getting ready: how to make the outside look inviting from the street, how to set up rooms so buyers can picture living there, and which upgrades pay back what they cost. One chapter covers the 80/20 rule: a few jobs make most of the difference, so do those first.",
         "Selling: how to market your home and find buyers, the mistakes sellers make most often, and lessons from sellers who learned the hard way. The last two chapters are about negotiating: how to stand firm, and what to do and not do when offers come in.",
     ],
     "about_es": [
         "Este libro lo guía para vender su casa en el orden en que pasan las cosas. Empieza con los primeros pasos. Luego explica cómo preparar la casa, cómo hacer que los compradores la vean, y cómo lograr el mejor trato.",
         "La preparación: cómo hacer que la casa se vea atractiva desde la calle, cómo arreglar los cuartos para que los compradores se imaginen viviendo ahí, y qué mejoras recuperan lo que cuestan. Un capítulo explica la regla del 80/20: unos pocos trabajos hacen la mayor diferencia, así que hágalos primero.",
         "La venta: cómo promover su casa y encontrar compradores, los errores más comunes de los vendedores, y lecciones de quienes aprendieron por las malas. Los dos últimos capítulos tratan de la negociación: cómo mantenerse firme, y qué hacer y qué no hacer cuando llegan las ofertas. El libro está en inglés.",
     ]},
    {"key": "Expired!? A Guide for Selling Homes Others Couldn't Sell", "slug": "free-book-expired", "photo": "book-expired.png",
     "title": "Expired!? A Guide for Selling Homes Others Couldn't Sell",
     "line": "For owners whose home was listed and didn't sell. Why it happens, and what to change before you try again.",
     "line_es": "Para dueños cuya casa estuvo en venta y no se vendió. Por qué pasa, y qué cambiar antes de intentarlo otra vez.",
     "about": [
         "Your home was on the market, and the listing ran out without a sale. That's frustrating, and it happens to good homes too. This short book explains why.",
         "It covers whether the listing price really matters, what to avoid, how easy it is to sell a home for less than it's worth, and what stops even well-kept homes from selling.",
         "Then it turns to the second try: what you can change besides the price, how to catch buyers' attention, and why staging (setting up the rooms for showings) really matters. If your home didn't sell, read this before you sign with anyone again, including me.",
     ],
     "about_es": [
         "Su casa estuvo en venta y el contrato terminó sin una venta. Es frustrante, y también les pasa a casas buenas. Este libro corto explica por qué.",
         "Trata de si el precio de venta de verdad importa, qué evitar, lo fácil que es vender una casa por menos de lo que vale, y qué impide que se vendan aun las casas bien cuidadas.",
         "Luego habla del segundo intento: qué puede cambiar además del precio, cómo captar la atención de los compradores, y por qué de verdad importa preparar la casa para las visitas. Si su casa no se vendió, léalo antes de firmar con alguien otra vez, incluso conmigo. El libro está en inglés.",
     ]},
]

# ------------------------------------------------------------------- HTML
CSS = r"""
:root{
  --ink:#1b2730; --ink-2:#4a5a66; --ridge:#2f4b5f; --ridge-deep:#213746;
  --haze:#e9eef1; --paper:#ffffff; --stone:#eef3f6; --gold:#b98a2c; --gold-ink:#7a5a17;
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
nav.menu a{color:#fff;text-decoration:none;margin-left:14px;font-size:1rem;white-space:nowrap;border-bottom:2px solid transparent;padding:4px 0}
nav.menu a[aria-current]{border-color:var(--gold)}
nav.menu a.lang{border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:3px 10px;margin-left:16px}
.burger{background:none;border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:6px;padding:8px 10px;font:inherit;font-size:.95rem;cursor:pointer}
.topright{display:flex;align-items:center;gap:8px}
.lang-m{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:6px 12px;font-size:.92rem;white-space:nowrap}
.drawer{display:none;background:var(--ridge);padding:8px 0 14px}
.drawer.open{display:block}
.drawer a{display:block;color:#fff;text-decoration:none;padding:12px var(--gutter);border-top:1px solid rgba(255,255,255,.12);font-size:1.05rem}
.drawer a[aria-current]{color:#f3d58a}
@media(min-width:1024px){.top .wrap{flex-wrap:wrap;row-gap:0;padding-top:12px}nav.menu{display:flex;align-items:center;flex-wrap:wrap;width:100%;border-top:1px solid rgba(255,255,255,.14);margin-top:10px;padding-block:8px 10px;row-gap:4px}nav.menu a{margin-left:0;margin-right:12px;font-size:.86rem}@media(max-width:1180px){nav.menu a{font-size:.8rem;margin-right:10px}}nav.menu{flex-wrap:nowrap!important}nav.menu a.srch{margin-left:auto}nav.menu a.lang{margin-left:4px;margin-right:0}.burger,.drawer,.topright{display:none!important}}
/* hero */
.hero{background:linear-gradient(180deg,var(--ridge-deep) 0,var(--ridge) 100%);color:#fff;padding:48px 0 56px}
.hero h1{max-width:18ch}
.hero p{color:#dfe7ec;max-width:52ch;font-size:1.08rem}
.addr{display:flex;flex-direction:column;gap:10px;margin-top:22px;max-width:560px}
.contact-grid a.ct-alt,.ct-alt{display:block;font-size:.9rem;font-weight:400;margin-top:6px}
/* Layout review 11/13/2026 */
.hero-call{margin:12px 0 0;display:flex;flex-direction:column;gap:6px;max-width:560px}
.hero-call span{font-size:.95rem;color:#dfe7ec}
.btn.btn-text{background:transparent;color:#fff;border:2px solid #fff;text-align:center;white-space:normal}
.btn.btn-text:hover{background:rgba(255,255,255,.12)}
.btn.btn-text.dark{color:var(--ridge-deep);border-color:var(--ridge-deep)}
.btn.btn-text.dark:hover{background:var(--haze)}
@media(min-width:620px){.hero-call{flex-direction:row;align-items:center;gap:14px}}
@media(max-width:719px){.hero-truths{grid-template-columns:repeat(3,1fr);gap:10px;padding:14px}.hero-truths p{display:none}.hero .hero-truths h3{font-size:.95rem;margin:0}.hero-truths>div{padding-top:8px}}
.sold-strip.mini{grid-template-columns:repeat(2,1fr);max-width:640px}
.sold-strip .tag.off{background:#9b1c1c}
.me-head{display:flex;align-items:center;gap:16px;margin-bottom:10px}
.me-head img{width:72px;height:72px;border-radius:50%;object-fit:cover;border:2px solid var(--gold);flex:none}
.me-head h1{margin:0}
.me-head .me-by{margin:2px 0 0;color:var(--ink-2);font-size:.98rem}
.hv-grid{display:grid;gap:28px}
.hv-side{background:var(--stone);border-radius:12px;padding:20px 22px}
@media(min-width:960px){.hv-grid{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:48px;align-items:start}.hv-side{position:sticky;top:24px}}
details.more-boxes{border:1.5px solid var(--line);border-radius:10px;padding:12px 14px}
details.more-boxes>summary{cursor:pointer;font-weight:600;color:var(--ridge)}
details.more-boxes[open]>summary{margin-bottom:12px}
details.more-boxes label{margin-top:10px}
.stats.top{margin:6px 0 18px;font-size:1.05rem}
.rv-grid{display:grid;gap:0 24px}
@media(min-width:900px){.rv-grid{grid-template-columns:1fr 1fr}.rv-grid blockquote{max-width:none}}
.ct-wrap{display:grid;gap:32px}
@media(min-width:900px){.ct-wrap{grid-template-columns:1fr 1fr;gap:56px;align-items:start}}
.ct-btns{display:grid;gap:12px;max-width:440px;margin-top:8px}
.btn.btn-big{font-size:1.15rem;padding:18px 22px;text-align:center;white-space:normal}
.ct-small{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.ct-small .btn{text-align:center}
@media(max-width:719px){.shelf{grid-template-columns:1fr 1fr;gap:12px}.shelf a{padding:12px;gap:8px}.shelf img{width:100%;max-width:120px}.shelf b{font-size:.95rem}.shelf span:not(.go){font-size:.85rem}}
.shelf .go.btn{display:block;text-decoration:none;font-size:.95rem;padding:10px 12px;white-space:normal;margin-top:4px}
.f-contact{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:10px}
.f-contact a{font-size:1rem}
.f-towns{line-height:1.9}
.hv-law{margin:16px 0 0;max-width:70ch}
.addr input{font:inherit;font-size:1.05rem;padding:14px 16px;border:1px solid #fff;border-radius:8px;width:100%}
@media(min-width:620px){.addr{flex-direction:row}.addr input{flex:1}}
.btn{display:inline-block;background:var(--gold);color:#1b1503;font:inherit;font-weight:600;font-size:1.02rem;padding:14px 22px;border-radius:8px;border:0;text-decoration:none;cursor:pointer;white-space:nowrap}
.btn:hover{background:#cf9b34}
.btn.quiet{background:transparent;color:var(--ridge);border:1.5px solid var(--ridge)}
.btn.quiet:hover{background:var(--haze)}
/* home redesign */
/* Hero photo: Blue Ridge Mountains at sunset, by Sara Parlier on Unsplash
   (unsplash.com/photos/mmVBTYA45ok). Unsplash License: free for business use, no credit required. */
.hero{position:relative;overflow:hidden;padding:64px 0 48px;
  background:linear-gradient(180deg,rgba(12,24,36,.55) 0%,rgba(12,24,36,.42) 35%,rgba(12,24,36,.30) 65%,rgba(12,24,36,.35) 100%),
             url(hero-mountains-1200.jpg) 40% 100%/auto 150% no-repeat #21384c}
@media(min-width:900px){.hero{padding:96px 0 72px;
  background:linear-gradient(90deg,rgba(12,24,36,.86) 0%,rgba(12,24,36,.62) 42%,rgba(12,24,36,.18) 78%,rgba(12,24,36,.10) 100%),
             url(hero-mountains.jpg) center 65%/cover no-repeat #21384c}}
.hero .wrap{position:relative;z-index:1}
.hero-grid{display:grid;gap:32px;align-items:center}
@media(min-width:900px){.hero-grid{grid-template-columns:1fr 330px;gap:56px}}
.hero-me{display:none;text-align:center;color:#dfe7ec}
@media(min-width:900px){.hero-me{display:block}}
.hero-me img{width:280px;height:280px;border-radius:50%;object-fit:cover;margin:0 auto 14px;border:4px solid var(--gold);box-shadow:0 18px 40px rgba(0,0,0,.35)}
.hero-me b{display:block;color:#fff;font-size:1.1rem}
.hero-me span{font-size:.95rem}
.hero-me-m{display:flex;align-items:center;gap:12px;margin-bottom:18px;color:#dfe7ec;font-size:.95rem}
.hero-me-m img{width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid var(--gold)}
.hero-me-m b{display:block;color:#fff}
@media(min-width:900px){.hero-me-m{display:none}}

.hero h1,.hero p{text-shadow:0 1px 12px rgba(10,22,32,.45)}
.truths > div{border-top:3px solid var(--gold);padding-top:14px}
.hero-truths{margin-top:44px;padding:20px 22px 22px;background:rgba(12,24,36,.58);border-radius:12px;-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
.hero .hero-truths h3{color:#fff}
.hero .hero-truths p{color:#e6edf2;text-shadow:none}
@media(min-width:900px){.hero-truths{margin-top:56px}}
.sold-strip{display:grid;gap:16px;grid-template-columns:repeat(2,1fr)}
@media(min-width:900px){.sold-strip{grid-template-columns:repeat(4,1fr)}}
.sold-strip figure{margin:0;border-radius:12px;overflow:hidden;background:#fff;border:1px solid var(--line)}
.sold-strip .im{position:relative;aspect-ratio:4/3}
.sold-strip img{width:100%;height:100%;object-fit:cover}
.sold-strip .tag{position:absolute;left:10px;top:10px;background:var(--ridge-deep);color:#fff;font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:4px 9px;border-radius:4px}
.sold-strip figcaption{padding:10px 12px 12px;font-size:.92rem;color:var(--ink-2)}
.sold-strip figcaption b{display:block;color:var(--ridge-deep);font-size:1.05rem}
.towns-band{border-bottom:1px solid #dde5ea}
.towns-band .town-btns{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px}
@media(min-width:640px){.towns-band .town-btns{grid-template-columns:repeat(3,1fr)}}
@media(min-width:1000px){.towns-band .town-btns{grid-template-columns:repeat(5,1fr)}}
.town-btns a{display:block;text-align:center;padding:13px 10px;border:1.5px solid var(--ridge);border-radius:8px;color:var(--ridge);text-decoration:none;font-weight:600;font-size:1rem;background:#fff}
.town-btns a:hover,.town-btns a:focus-visible{background:var(--ridge);color:#fff}
.towns-band .note{font-size:.92rem;color:var(--ink-2);margin-top:14px}
.gtop{padding-top:18px;padding-bottom:26px}
.ghead{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center}
.ghead img{width:74px;height:auto;border-radius:3px;box-shadow:0 3px 10px rgba(0,0,0,.2)}
.ghead .kick{font-size:.82rem;color:var(--ink-2);margin:0 0 2px}
.ghead h1{font-size:1.45rem;margin:0;line-height:1.15}
.gtop .gline{margin:12px 0 14px;font-size:1rem}
.gtop form.sheet{gap:10px}
.gtop form.sheet .fine{margin:0;font-size:.85rem}
.gtop form.sheet input{padding:10px 12px}
.glong{max-width:70ch}
.gwho{margin:12px 0 0;font-size:.95rem}
.gshort-h{margin:12px 0 2px;font-size:.82rem;font-weight:600;color:var(--ink-2);text-transform:uppercase;letter-spacing:.06em}
.gshort{margin:0;padding-left:1.1em;font-size:.95rem;line-height:1.35}
.gshort li{margin:2px 0}
.gagain{margin-top:24px}
/* Seller's Guide pages carry the short bullets; tighten so the button stays near the first phone screen */
@media(max-width:799px){.gtop.has-short{padding-top:10px}.gtop.has-short .ghead img{width:60px}.gtop.has-short .ghead h1{font-size:1.3rem}
.gtop.has-short .gshort-h{margin-top:8px}.gtop.has-short .gline{margin:8px 0 10px;font-size:.95rem}
.gtop.has-short form.sheet{gap:8px}.gtop.has-short form.sheet label{gap:3px;font-size:.92rem}.gtop.has-short form.sheet input{padding:8px 12px}}
.pair{display:grid;grid-template-columns:1.7fr 1fr;gap:10px}
@media(min-width:800px){.gtop{padding-top:40px}.ghead img{width:150px}.ghead{gap:28px}.ghead h1{font-size:2.4rem}.gtop .gline{font-size:1.1rem;margin:18px 0}}
.guidehero{display:grid;gap:26px;align-items:center}
.guidehero img{width:100%;max-width:180px;height:auto;border-radius:6px;box-shadow:0 8px 24px rgba(0,0,0,.18)}
@media(min-width:800px){.guidehero img{max-width:260px}.guidehero.has-cover{grid-template-columns:260px 1fr;gap:44px}}
.guidehero > div{max-width:720px}
.books-band{background:var(--ridge-deep);color:#fff}
.books-band .wrap{display:grid;gap:28px;align-items:center}
@media(min-width:900px){.books-band .wrap{grid-template-columns:1fr 1fr;gap:48px}}
.books-band p{color:#dfe7ec}
.books-row{display:flex;justify-content:center;align-items:flex-end;gap:6px}
.books-row a{flex:1;max-width:190px}
.books-row img{width:100%;height:auto;transition:transform .2s}
.books-row a.guide{padding:0 8px 4.5%}
.books-row a.guide img{border-radius:3px;box-shadow:0 6px 16px rgba(0,0,0,.35)}
.books-row a:hover img,.books-row img:hover{transform:translateY(-6px)}
.why-one ul.plain{max-width:820px}
.why-one ul.plain{columns:1}
@media(min-width:760px){.why-one ul.plain{columns:2;column-gap:40px}.why-one ul.plain li{break-inside:avoid}}
.quote-band blockquote{background:none;margin:0 auto;padding:0;max-width:46rem;text-align:center}
.quote-band blockquote p{font-size:clamp(1.25rem,2.6vw,1.6rem);font-style:italic;line-height:1.45;margin:0 auto .6em;max-width:none}
.quote-band .mark{font-size:4rem;line-height:.5;color:var(--gold);display:block;margin-bottom:10px}
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
.card .ph{position:relative}
.card .offmk{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);background:rgba(155,28,28,.88);color:#fff;font-weight:600;font-size:1.05rem;letter-spacing:.04em;text-transform:uppercase;text-align:center;padding:12px 10px}
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
.nl-list{list-style:none;padding:0;margin:0;max-width:720px}
.nl-list li{padding:14px 0;border-top:1px solid var(--line)}
.nl-list li:last-child{border-bottom:1px solid var(--line)}
.nl-list a{text-decoration:none}
.nl-body{max-width:65ch}
.nl-body h2{font-size:clamp(1.5rem,3.6vw,2.1rem);margin-top:0}
.nl-body h3{font-size:1.25rem;margin:0 0 .6em;color:var(--ridge-deep)}
.nl-kicker{font-size:.85rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 .4em}
.nl-head h1{margin-bottom:.35em}
section[id]{scroll-margin-top:12px}
.tbl-wrap{overflow-x:auto;margin:6px 0 18px;border:1px solid var(--line);border-radius:10px;-webkit-overflow-scrolling:touch}
.nl-table{border-collapse:collapse;width:100%;min-width:640px;font-size:.97rem;font-variant-numeric:tabular-nums}
.nl-table caption{text-align:left;font-weight:600;padding:12px 14px 6px;color:var(--ink-2);font-size:.92rem}
.nl-table th,.nl-table td{padding:10px 14px;text-align:right;border-top:1px solid var(--line);white-space:nowrap}
.nl-table thead th{font-size:.85rem;color:var(--ink-2);font-weight:600;background:var(--stone)}
.nl-table th[scope=row],.nl-table thead th:first-child{text-align:left;position:sticky;left:0;background:var(--paper)}
.nl-table thead th:first-child{background:var(--stone)}
.nl-table tr.tot th,.nl-table tr.tot td{font-weight:700;background:#f6edd9}
.nl-table tr.tot th[scope=row]{background:#f6edd9}
.nl-sign{font-size:.92rem;color:var(--ink-2);margin-top:22px}
.nl-boxes{display:none;list-style:none;padding:0;margin:6px 0 18px}
.nl-boxes li{display:grid;gap:2px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;margin-bottom:8px;font-variant-numeric:tabular-nums}
.nl-boxes li span{color:var(--ink-2);font-size:.97rem}
.nl-boxes li.tot{background:#f6edd9;border-color:#e3d3ad}
.nl-boxes li.cap{border:0;padding:0 2px 4px;color:var(--ink-2);font-size:.9rem;font-weight:600}
@media(max-width:700px){.tbl-wrap{display:none}.nl-boxes{display:block}}
.books{display:grid;gap:18px;margin:0 0 6px}
@media(min-width:720px){.books{grid-template-columns:repeat(2,1fr);max-width:640px}}
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
@media(min-width:720px){.shelf{grid-template-columns:repeat(2,1fr);max-width:760px}}
.shelf a{display:grid;gap:10px;padding:18px;border:1.5px solid var(--line);border-radius:12px;text-decoration:none;color:var(--ink);text-align:center;background:#fff}
.shelf a:hover{border-color:var(--gold);background:#fbf6ea}
.shelf img{width:170px;height:auto;margin:0 auto}
.shelf b{font-size:1.05rem}
.shelf span{font-size:.95rem;color:var(--ink-2)}
.shelf .go{color:var(--ridge);font-weight:600;text-decoration:underline;text-underline-offset:3px}
.bookhero{display:grid;gap:24px;align-items:start}
@media(min-width:800px){.bookhero{grid-template-columns:300px 1fr;gap:48px}}
.bookhero img{width:130px;height:auto;margin:0}
@media(min-width:800px){.bookhero img{width:100%;max-width:320px;margin:0 auto}}
@media(max-width:799px){.bookhero{gap:14px}.bookhero h1{font-size:1.65rem}}
.form-err{font-size:.8rem;color:var(--ink-2);margin:4px 0 0;word-break:break-word}
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
.privacy{max-width:680px}.privacy h2{font-size:1.25rem;margin:26px 0 6px}.privacy p{margin:0 0 10px}
@media(min-width:800px){footer.site .wrap{grid-template-columns:1fr 1fr}}
/* Footer newsletter sign-up: small and quiet, under the footer text (J.R., 11/10/2026). */
footer.site .nl-foot{grid-column:1/-1;border-top:1px solid rgba(255,255,255,.14);padding-top:14px;margin-top:2px;font-size:.86rem}
footer.site .nl-foot p.t{margin:0 0 8px;color:#cfd9e0}footer.site .nl-foot b{color:#fff;font-weight:600}
footer.site .nl-foot .row{display:flex;gap:8px;flex-wrap:wrap;max-width:460px}
footer.site .nl-foot label{flex:1 1 200px;display:block}
footer.site .nl-foot input[type=email]{width:100%;font:inherit;font-size:16px;padding:8px 10px;border-radius:6px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:#fff}
footer.site .nl-foot input[type=email]::placeholder{color:#9fb0bc}
footer.site .nl-foot button{font:inherit;font-size:.88rem;font-weight:600;padding:8px 14px;border-radius:6px;border:1px solid rgba(255,255,255,.4);background:transparent;color:#fff;cursor:pointer;white-space:nowrap}
footer.site .nl-foot .form-msg{font-size:.88rem;padding:8px 10px;margin-top:8px;max-width:460px}
footer.site .nl-foot .form-err{color:#cfd9e0}
.hp{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = r"""
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),d=document.querySelector('.drawer');
  if(b&&d){b.addEventListener('click',function(){var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
  var h=document.getElementById('hero-addr');
  if(h){h.addEventListener('submit',function(e){e.preventDefault();var v=(h.querySelector('input').value||'').trim(),ok=false;
    // The address goes to the next page through this visit's storage, not the page address (kept out of the Meta Pixel).
    try{sessionStorage.setItem('jr_addr',v);ok=true;}catch(err){}
    location.href=h.getAttribute('data-to')+(!ok&&v?'?address='+encodeURIComponent(v):'');});}
  var f=document.getElementById('addr-field');
  if(f){var q=new URLSearchParams(location.search).get('address');if(!q){try{q=sessionStorage.getItem('jr_addr');sessionStorage.removeItem('jr_addr');}catch(err){}}if(q)f.value=q;}
  // Source tag (J.R., 11/10/2026): a link like ?src=fbad marks where the visitor came from.
  // The tag is kept for the visit (sessionStorage), so it survives clicks to other pages,
  // and is written into each form's "source" field when it sends. No tag: the page's own source.
  var tag='';
  try{
    var qs=new URLSearchParams(location.search).get('src');
    if(qs!==null){qs=qs.trim().slice(0,60);if(qs){try{sessionStorage.setItem('jr_src',qs);}catch(e){}tag=qs;}}
    if(!tag){try{tag=sessionStorage.getItem('jr_src')||'';}catch(e){}}
  }catch(e){}
  document.querySelectorAll('form.js-fs').forEach(function(form){
    var sf=form.querySelector('input[name=source]');
    if(!sf){sf=document.createElement('input');sf.type='hidden';sf.name='source';sf.value='website';form.appendChild(sf);}
    sf.dataset.base=sf.value;
    if(tag)sf.value=tag;
    // Which form this is (same name the Pixel 'Lead' uses), sent as "form" so every entry says where it came from.
    var pg=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'');
    var fname=(form.id==='nl-foot'?'footer':(pg==='index'?'home':pg))+(document.documentElement.lang==='es'?'-es':'');
    // Robot protection (J.R., 11/10/2026), nothing a person sees or has to do:
    // 1) a second hidden "honeypot" box that people never see; robots that fill every box fill it;
    // 2) the form only sends after a real person typed, tapped or clicked in it (robots' fake events don't count);
    // 3) a send less than 2 seconds after the page opened is treated as a robot.
    var hp=document.createElement('div');hp.className='hp';hp.setAttribute('aria-hidden','true');
    hp.innerHTML='<label>Leave this empty<input type="text" name="company_website" tabindex="-1" autocomplete="off" value=""></label>';
    form.appendChild(hp);
    var touched=false,opened=Date.now();
    ['input','keydown','pointerdown','touchstart','change'].forEach(function(ev){form.addEventListener(ev,function(x){if(x.isTrusted)touched=true;},true);});
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var btn=form.querySelector('button[type=submit]'),msg=form.querySelector('.form-msg'),label=btn.textContent;
      // No send without a real email, whatever started the send (a robot can skip the browser's own check).
      var em=form.querySelector('input[name=email]'),ev=em?(em.value||'').trim():'';
      if(!em||!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(ev)||!form.checkValidity()){
        if(e.isTrusted&&form.reportValidity)form.reportValidity();
        return;
      }
      var bot=!touched||(Date.now()-opened<2000)||((form.querySelector('input[name=_gotcha]')||{}).value)||((form.querySelector('input[name=company_website]')||{}).value);
      if(bot){
        // Looks like a robot: show the normal thank-you, send nothing, count nothing.
        form.querySelectorAll('label,.two,.three,.pair,.fine,.row,details,button').forEach(function(el){el.hidden=true;});
        msg.className='form-msg ok';msg.textContent=form.dataset.ok;msg.hidden=false;return;
      }
      if(form.dataset.need&&!form.querySelector('input[name=books]:checked')){
        msg.className='form-msg bad';msg.textContent=form.dataset.need;msg.hidden=false;
        form.querySelector('.books').scrollIntoView({block:'center'});return;
      }
      if(btn.disabled)return;
      btn.disabled=true;btn.textContent=form.dataset.sending;msg.hidden=true;
      var old=form.querySelector('.form-err');if(old)old.remove();
      // One ID per request, kept across retries and taps, so any repeat is easy to spot (J.R., 11/5/2026).
      if(!form.dataset.rid)form.dataset.rid=Date.now().toString(36)+Math.random().toString(36).slice(2,8);
      var src=new FormData(form),base=[],errs=[];
      try{
        var g=function(k){return (src.get(k)||'').toString().trim();};
        var r={t:form.id==='hv-form'?'v':(form.id==='bk-form'?'b':(form.id.indexOf('nl-')===0?'n':(form.id==='sg-form'?'g':(form.id==='fg-form'?'f':(form.id==='sl-form'?'s':(form.id==='bg-form'?'y':'c')))))),l:document.documentElement.lang==='es'?'es':'en',
               n:g('name'),p:g('phone'),e:g('email'),a:[g('address')||g('street'),g('city')].filter(Boolean).join(', ')};
        base.push(['tap_to_reply',location.origin+'/reply.html#'+new URLSearchParams(r).toString()]);
      }catch(err){}
      if(!src.get('_subject'))src.set('_subject','Website form ('+fname+') from jrREsales.com');
      src.set('form',fname);
      src.delete('company_website');
      src.forEach(function(v,k){base.push([k,v]);});
      if(tag&&sf.dataset.base!==tag)base.push(['source_without_tag',sf.dataset.base]);
      base.push(['request_id',form.dataset.rid]);
      function done(){
        // Meta Pixel 'Lead' for sign-up forms (not the contact form). Only the form's name goes to Facebook.
        try{
          if(window.fbq&&form.id!=='ct-form'){
            fbq('track','Lead',{content_name:fname});
          }
        }catch(err){}
        form.querySelectorAll('label,.two,.three,.pair,.fine,button').forEach(function(el){el.hidden=true;});
        msg.className='form-msg ok';msg.textContent=form.dataset.ok;msg.hidden=false;
        msg.scrollIntoView({block:'center'});
      }
      function fail(code){
        btn.disabled=false;btn.textContent=label;
        msg.className='form-msg bad';msg.textContent=form.dataset.bad;msg.hidden=false;
        var sm=document.createElement('p');sm.className='form-err';sm.textContent='Error code: '+code;msg.insertAdjacentElement('afterend',sm);
      }
      function send(n){
        var fd=new FormData();base.forEach(function(kv){fd.append(kv[0],kv[1]);});
        fd.append('attempt',String(n));
        if(errs.length)fd.append('earlier_try_error',errs.join(' | '));
        var ctl=('AbortController' in window)?new AbortController():null,tm=ctl?setTimeout(function(){ctl.abort();},15000):null;
        fetch(form.dataset.fs,{method:'POST',body:fd,headers:{'Accept':'application/json'},signal:ctl?ctl.signal:undefined})
          .then(function(res){
            if(tm)clearTimeout(tm);
            if(res.ok){done();return;}
            return res.text().then(function(t){
              var code='HTTP '+res.status+(t?' '+t.slice(0,120):'');
              // Retry only when the problem may be passing; a 4xx answer means Formspree refused this request.
              if(res.status>=500||res.status===429)retry(n,code);else fail(code);
            });
          })
          .catch(function(err){
            if(tm)clearTimeout(tm);
            retry(n,(err&&err.name==='AbortError')?'timeout after 15 seconds':'network: '+((err&&err.message)||err));
          });
      }
      function retry(n,code){
        errs.push('try '+n+': '+code);
        if(n<3)setTimeout(function(){send(n+1);},1000*n);else fail(code);
      }
      send(1);
    });
  });
});
"""

def esc(s): return html.escape(s, quote=True)

import hashlib as _hl
# Added to the style and script links (site.css?v=...). It changes whenever the
# CSS or JS changes, so browsers never mix a new page with an old saved style file.
ASSET_V = _hl.sha1((CSS + JS).encode()).hexdigest()[:8]

def mail_form(T, lang, subject, fields_html, submit_label, form_id="", ok=None):
    """Formspree if an ID is set, otherwise a mailto that opens the visitor's mail app."""
    if SITE["formspree_id"]:
        ok_custom = ok
        action = f'https://formspree.io/f/{SITE["formspree_id"]}'
        hidden = (f'<input type="hidden" name="_subject" value="{esc(subject)}">'
                  f'<input type="hidden" name="language" value="{"Spanish" if lang == "es" else "English"}">'
                  '<div style="display:none" aria-hidden="true"><input type="text" name="_gotcha" tabindex="-1" autocomplete="off" value=""></div>')
        if lang == "es":
            ok = "Gracias. Su solicitud llegó a J.R. Recibirá respuesta en un día hábil."
            bad = "No se pudo enviar. Por favor envíe un texto a J.R. al " + SITE["phone"] + "."
            sending = "Enviando…"
        else:
            ok = "Thank you. Your request reached J.R. You'll hear back within one business day."
            bad = "That didn't go through. Please text J.R. at " + SITE["phone"] + "."
            sending = "Sending…"
        if ok_custom:
            ok = ok_custom
        return (f'<form class="sheet js-fs" id="{form_id}" data-fs="{action}" method="POST" '
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
    "name": "J.R. Grimaldo",
    "jobTitle": "Real Estate Professional",
    "url": "https://" + SITE["domain"] + "/",
    "image": "https://" + SITE["domain"] + "/assets/jr-headshot.jpg",
    "telephone": SITE["phone_tel"],
    "email": SITE["email"],
    "address": {"@type": "PostalAddress", "streetAddress": "P.O. Box 106",
                "addressLocality": "Landrum", "addressRegion": "SC", "postalCode": "29356", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": a + ", SC"} for a in SITE["areas"]],
    "knowsLanguage": ["en", "es"],
    "slogan": "Principles Before Profits",
    "parentOrganization": {"@type": "RealEstateAgent", "name": BRAND["brokerage"]},
    "sameAs": SITE["profiles"],
}, ensure_ascii=False).replace("</", "<\\/")

# Meta Pixel (J.R., 11/10/2026), exactly as J.R. gave it, plus his autoConfig line (a second lock
# against Facebook reading form fields on its own; added 11/10 at his request). Goes in the <head> of every layout() page.
META_PIXEL = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('set','autoConfig',false,'1432161975184837');
fbq('init', '1432161975184837');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1432161975184837&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""

# Runs before the Pixel: if a street address arrived in the page address (?address=..., from an
# old link), move it into this visit's storage and take it out of the address bar, so the Pixel
# never sends a street address to Facebook as part of the page address.
ADDR_SCRUB = ("<script>(function(){try{var u=new URL(location.href),a=u.searchParams.get('address');"
              "if(a!==null){try{sessionStorage.setItem('jr_addr',a);}catch(e){}u.searchParams.delete('address');"
              "history.replaceState(null,'',u.pathname+u.search+u.hash);}}catch(e){}})();</script>")

# Pages kept out of search and the sitemap: the unlisted Buyer's Guide page, and the letter-only
# FSBO page (fsbo-guide-info.html is the FSBO page for Google).
NOINDEX_PAGES = {"buyers-guide.html", "fsbo-guide.html", "tax-sale-guide.html"}  # tax-sale: unlisted + noindex at launch (J.R. 11/13)

# Share pictures (og:image) that differ from the default share.jpg: the guide pages show
# their own cover when shared on Facebook (J.R., 11/10/2026). Key: (language, page).
OG_IMAGES = {("en", "sellers-guide.html"): "share-sellers-guide.jpg",
             ("es", "sellers-guide.html"): "share-guia-vendedores.jpg",
             ("en", "fsbo-guide.html"): "share-fsbo-guide.jpg",
             ("en", "fsbo-guide-info.html"): "share-fsbo-guide.jpg",
             ("en", "buyers-guide.html"): "share-buyers-guide.jpg"}

def footer_signup(T):
    """Small newsletter sign-up in every footer. Same Formspree form and subject as the newsletter page; source=footer."""
    es = T["lang"] == "es"
    if not SITE["formspree_id"]:
        return ""
    subj = "Newsletter sign-up from " + SITE["domain"] if not es else "Inscripción al boletín desde " + SITE["domain"]
    if es:
        line = ("Front Porch Notes", ": una nota mensual breve sobre lo que se vendieron las casas en nuestros pueblos. Solo su correo.")
        btn, lab, ph = "Suscribirme", "Su correo electrónico", "Su correo"
        ok = T["nl_fields"]["ok"]
        bad = "No se pudo enviar. Por favor envíe un texto a J.R. al " + SITE["phone"] + "."
        sending = "Enviando…"
    else:
        line = ("Front Porch Notes", ": a short monthly note on what homes in our towns sold for. Your email, nothing else.")
        btn, lab, ph = "Sign me up", "Your email", "Your email"
        ok = T["nl_fields"]["ok"]
        bad = "That didn't go through. Please text J.R. at " + SITE["phone"] + "."
        sending = "Sending…"
    return (f'<form class="nl-foot js-fs" id="nl-foot" data-fs="https://formspree.io/f/{SITE["formspree_id"]}" method="POST" '
            f'data-ok="{esc(ok)}" data-bad="{esc(bad)}" data-sending="{esc(sending)}">'
            f'<input type="hidden" name="_subject" value="{esc(subj)}">'
            f'<input type="hidden" name="language" value="{"Spanish" if es else "English"}">'
            '<input type="hidden" name="source" value="footer">'
            '<div style="display:none" aria-hidden="true"><input type="text" name="_gotcha" tabindex="-1" autocomplete="off" value=""></div>'
            f'<p class="t"><b>{esc(line[0])}</b>{esc(line[1])}</p>'
            f'<div class="row"><label><span class="vh">{esc(lab)}</span><input type="email" name="email" required placeholder="{esc(ph)}" autocomplete="email"></label>'
            f'<button type="submit">{esc(btn)}</button></div>'
            '<p class="form-msg" role="status" aria-live="polite" hidden></p></form>')

# Layout review 11/13/2026: smaller photo copies for phones (name-600.jpg) and photos far down the page
# load only when the visitor scrolls near them. No visible change.
import re as _re
def _img_opt(html_s):
    def fix(m):
        tag = m.group(0)
        src = _re.search(r'src="([^"]+)"', tag)
        if not src: return tag
        u = src.group(1)
        if "headshot" not in u and "loading=" not in tag:
            tag = tag.replace("<img ", '<img loading="lazy" ', 1)
        base = u.rsplit("/", 1)[-1]
        if base.endswith(".jpg") and "-600" not in base and "headshot" not in base:
            small = base[:-4] + "-600.jpg"
            if (SRC / "assets" / small).exists() and "srcset=" not in tag:
                su = u[:-len(base)] + small
                tag = tag.replace('<img ', f'<img srcset="{su} 600w, {u} 1200w" sizes="(max-width: 899px) 50vw, 600px" ', 1)
        return tag
    return _re.sub(r'<img [^>]*>', fix, html_s)

def layout(T, page, title, body, lang_switch, desc=None, alt=None):
    body = _img_opt(body)
    p = T["dir_prefix"]
    up = "../" if p else ""
    nav_links = ""
    drawer = ""
    for href, label in T["nav"]:
        cur = ' aria-current="page"' if href.endswith(page) and not href.startswith("..") else ""
        nav_links += f'<a href="{href}"{cur}>{esc(label)}</a>'
        drawer += f'<a href="{href}"{cur}>{esc(label)}</a>'
    search = f'<a class="srch" href="{BRAND["brokerage_site"]}" rel="noopener">{esc(T["search_label"])}</a>'
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
<meta name="description" content="{esc(desc or T['hero_p'])}">{'<meta name="robots" content="noindex,nofollow">' if page in NOINDEX_PAGES else ''}
<meta property="og:type" content="website">
<meta property="og:site_name" content="J.R. Grimaldo, Real Estate Professional">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc or T['hero_p'])}">
<meta property="og:image" content="{('https://jrREsales.com/assets/' + OG_IMAGES[(T['lang'], page)] + '?v=' + _hl.sha1((SRC / 'assets' / OG_IMAGES[(T['lang'], page)]).read_bytes()).hexdigest()[:8]) if (T['lang'], page) in OG_IMAGES else ('https://' + SITE['domain'] + '/assets/share.jpg')}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{canon}">
<link rel="canonical" href="{canon}">{hreflang}
<script type="application/ld+json">{AGENT_LD}</script>
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<link rel="stylesheet" href="{up}assets/site.css?v={ASSET_V}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
{ADDR_SCRUB}
{META_PIXEL}
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
      <p>{esc(SITE['agent'])}, {'Profesional de Bienes Raíces · Licencia de SC #95641' if T['lang'] == 'es' else 'Real Estate Professional · ' + esc(SITE['license'])}</p>
      <p>{esc(BRAND['brokerage'])} · {'Rick Markowski, Corredor a cargo (Broker-in-Charge)' if T['lang'] == 'es' else esc(BRAND['broker_in_charge'])}</p>
      <p>{esc(BRAND['office'])}</p>
    </div>
    <div>
      <ul class="f-contact">
        <li><a href="sms:{SITE['phone_tel']}">{'Envíe un texto al 864-381-2326. Es lo más rápido.' if T['lang'] == 'es' else 'Text 864-381-2326. Fastest way to reach me.'}</a></li>
        <li><a href="tel:{SITE['phone_tel']}">{'Llamar al' if T['lang'] == 'es' else 'Call'} {SITE['phone']}</a></li>
        <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
      </ul>
      <p class="f-towns">{esc(towns_label)}:<br>{towns_links}</p>
      <p>{esc(T['footer_eho'])} © 2026 {esc(SITE['agent'])}. {esc(T['footer_rights'])} · <a href="{'privacy.html' if p in ('', 'es/') else '../privacy.html'}">{'Privacidad' if T['lang'] == 'es' else 'Privacy'}</a></p>
    </div>
    {footer_signup(T)}
  </div>
</footer>
<script src="{up}assets/site.js?v={ASSET_V}"></script>
</body>
</html>"""

def card(it, T):
    if "photo" in it and it["photo"] is None:
        phdiv = ""
    else:
        ph = f'<img src="{"../" if T["dir_prefix"] else ""}assets/{it["photo"]}" alt="{esc(it["address"])}">' if it.get("photo") else "Photo coming"
        ban = ""
        if it.get("off_market"):
            ban = ('<span class="offmk">' + ("Temporalmente fuera del mercado" if T["lang"] == "es" else "Temporarily off the market") + '</span>')
        phdiv = f'<div class="ph">{ph}{ban}</div>'
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

def _ridge_art():
    """Layered Blue Ridge silhouettes, back (hazy, light) to front (dark).
    Drawn from a fixed seed so every build looks the same."""
    import random, math
    rnd = random.Random(29356)  # Landrum ZIP
    W, H = 1440, 420
    layers = [  # (base height from top, roughness, color, opacity)
        (205, 95, "#c7d3dc", 1), (238, 90, "#a3b6c5", 1), (272, 80, "#7d97ab", 1),
        (306, 66, "#57748d", 1), (340, 50, "#395770", 1), (378, 28, "#243f54", 1)]
    def line(base, rough):
        # midpoint displacement for a natural ridge line
        pts = [base + rnd.uniform(-rough, rough * .3), base + rnd.uniform(-rough, rough * .3)]
        r = rough
        for _ in range(7):
            new = []
            for i in range(len(pts) - 1):
                new += [pts[i], (pts[i] + pts[i + 1]) / 2 + rnd.uniform(-r, r)]
            new.append(pts[-1]); pts = new; r *= .52
        n = len(pts) - 1
        return [(W * i / n, max(40, min(H, y))) for i, y in enumerate(pts)]
    out = []
    for base, rough, col, op in layers:
        pts = line(base, rough)
        d = "M0 %d " % H + " ".join("L%.0f %.0f" % (x, y) for x, y in pts) + " L%d %d Z" % (W, H)
        out.append(f'<path d="{d}" fill="{col}"/>')
    # soft foothill that hands off to the white page below
    out.append(f'<path d="M0 {H} L0 398 C360 380 720 410 1080 392 C1260 384 1380 396 {W} 390 L{W} {H} Z" fill="#ffffff"/>')
    return ('<svg class="ridges" viewBox="0 0 1440 420" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            + "".join(out) + "</svg>")
RIDGES_SVG = _ridge_art()

# Photo strip on the home page: J.R.'s own sold listings, from SOLD.
HOME_SOLD = ["248 Page Creek Blvd", "140 Belshire Dr", "420 Cloverdale Ln", "304 Talbert Trail"]

def page_home(T):
    up = "../" if T["dir_prefix"] else ""
    es = T["lang"] == "es"
    truths = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in T["truths"])
    bullets = "".join(f'<li>{esc(x)}</li>' for x in T["why_bullets"])
    def mini(it):
        street = it["address"].split(",")[0]; town = it["address"].split(",")[1].strip()
        tag = ("Temporalmente fuera del mercado" if es else "Temporarily off the market") if it.get("off_market") else ("En venta" if es else "For sale")
        return (f'<figure><div class="im"><img src="{up}assets/{it["photo"]}" alt="{esc(it["address"])}" loading="lazy">'
                f'<span class="tag{" off" if it.get("off_market") else ""}">{tag}</span></div>'
                f'<figcaption><b>{esc(it["price"])}</b>{esc(street)}, {esc(town)}</figcaption></figure>')
    minis = "".join(mini(x) for x in LISTINGS[:2] if x.get("photo"))
    cards = "".join(card(x, T) for x in LISTINGS[:2]) if LISTINGS else f'<div class="empty"><p>{esc(EN["li_empty"] if T["lang"]=="en" else "Por ahora no tengo propiedades en venta. Las nuevas aparecen aquí primero.")}</p></div>'
    listings_href = "listings.html"
    figs = ""
    for it in SOLD:
        street = it["address"].split(",")[0]
        if street not in HOME_SOLD or not it.get("photo"): continue
        town = it["address"].split(",")[1].strip()
        price = it["price"].replace("Sold for ", "")
        figs += (f'<figure><div class="im"><img src="{up}assets/{it["photo"]}" alt="{esc(it["address"])}" loading="lazy">'
                 f'<span class="tag">{"Vendida" if es else "Sold"}</span></div>'
                 f'<figcaption><b>{esc(price)}</b>{esc(street)}, {esc(town)}</figcaption></figure>')
    g_alt = GUIDE_ES["title"] if es else "Selling Your Home, Step by Step"
    covers = (f'<a class="guide" href="sellers-guide.html"><img src="{up}{GUIDE_ES["cover"] if es else GUIDE["cover"]}" alt="{esc(g_alt)}" loading="lazy"></a>'
              + "".join(f'<a href="{b["slug"]}.html"><img src="{up}assets/{b["photo"]}" alt="{esc(b["title"])}" loading="lazy"></a>' for b in BOOKS))
    town_btns = "".join(f'<a href="{up}{k}.html">{esc(TOWNS[k]["name"])}</a>' for k in TOWN_ORDER)
    if es:
        towns_band = (f'<section class="towns-band"><div class="wrap"><h2>Pueblos donde trabajo</h2>'
                      f'<p>Toque su pueblo para saber más sobre cómo vender su casa allí.</p>'
                      f'<div class="town-btns">{town_btns}</div>'
                      f'<p class="note">Las páginas de los pueblos están en inglés.</p></div></section>')
    else:
        towns_band = (f'<section class="towns-band"><div class="wrap"><h2>Towns I serve</h2>'
                      f'<p>Tap your town to learn more about selling your home there.</p>'
                      f'<div class="town-btns">{town_btns}</div></div></section>')
    q = next(r for r in REVIEWS if r["name"] == "Jeff D.")
    qt = q["quote_es"] if es else q["quote"]
    return f"""
<section class="hero"><div class="wrap"><div class="hero-grid"><div>
  <div class="hero-me-m"><img src="{up}assets/jr-headshot-400.jpg" alt="" width="64" height="64"><div><b>{esc(T['hero_who'])}</b>{esc(T['hero_where'])}</div></div>
  <h1>{esc(T['hero_h1'])}</h1>
  <p>{esc(T['hero_p'])}</p>
  <form class="addr" id="hero-addr" data-to="home-value.html">
    <label class="visually-hidden" style="position:absolute;left:-9999px" for="hero-input">{esc(T['hero_addr'])}</label>
    <input id="hero-input" type="text" placeholder="{esc(T['hero_addr'])}" autocomplete="street-address">
    <button class="btn" type="submit">{esc(T['hero_btn'])}</button>
  </form>
  <p class="hero-call"><a class="btn btn-text" href="sms:{SITE['phone_tel']}">{esc(T['text_btn'])}</a><span>{esc(T['text_fast'])}</span></p></div>
  <div class="hero-me"><img src="{up}assets/jr-headshot-600.jpg" alt="{esc(SITE['agent'])}" width="280" height="280"><b>{esc(T['hero_who'])}</b><span>{esc(T['hero_where'])}</span></div>
</div>
<div class="truths hero-truths">{truths}</div></div></section>
<section class="alt quote-band"><div class="wrap"><blockquote><span class="mark">“</span><p>{esc(qt)}</p><footer>{esc(q['name'])}{", " + ("opinión en Google" if es else "Google review")}</footer></blockquote></div></section>
<section><div class="wrap"><h2>{esc(T['hm_sold_h2'])}</h2><p>{esc(T['hm_sold_p'])}</p>
<div class="sold-strip">{figs}</div>
<p style="margin-top:22px"><a class="btn quiet" href="sold.html">{esc(T['hm_sold_btn'])}</a></p></div></section>
<section class="alt"><div class="wrap why-one">
  <h2>{esc(T['why_h2'])}</h2><p>{esc(T['why_p'])}</p><ul class="plain">{bullets}</ul>
  <a class="btn quiet" href="about.html">{esc(T['why_btn'])}</a>
</div></section>
<section class="books-band"><div class="wrap">
  <div><h2>{esc(T['hm_books_h2'])}</h2><p>{esc(T['hm_books_p'])}</p><a class="btn" href="free-books.html">{esc(T['hm_books_btn'])}</a></div>
  <div class="books-row">{covers}</div>
</div></section>
{towns_band}
<section><div class="wrap"><h2>{esc(T['listings_h2'])}</h2>{('<div class="sold-strip mini">' + minis + '</div>') if minis else ('<div class="cards">' + cards + '</div>')}
<p style="margin-top:22px"><a class="btn quiet" href="{listings_href}">{esc(T['listings_btn'])}</a></p></div></section>
<section class="alt"><div class="wrap"><h2>{esc(T['cta_h2'])}</h2><p>{esc(T['cta_p'])}</p>
<a class="btn btn-text dark" href="sms:{SITE['phone_tel']}">{esc(T['cta_btn'])}</a></div></section>"""

def page_home_value(T):
    F = T["hv_fields"]
    # Layout review 11/13/2026: four boxes first; the 8 optional ones stay, behind one line.
    more_lbl = "Agregar detalles de su casa (opcional)" if T["lang"] == "es" else "Add details about your home (optional)"
    fields = (
        '<div class="two">' + field("name", F["name"], req=True) + field("email", F["email"], "email", req=True) + '</div>'
        + field("address", F["address"], req=True, fid="addr-field")
        + field("city", F["city"], req=True)
        + f'<details class="more-boxes"><summary>{esc(more_lbl)}</summary>'
        + field("phone", F["phone"], "tel")
        + field("zip", F["zip"])
        + '<div class="three">' + field("bedrooms", F["beds"]) + field("bathrooms", F["baths"]) + field("square_feet", F["sqft"]) + '</div>'
        + field("year_built", F["year"])
        + field("updates", F["updates"], textarea=True)
        + field("timing", F["timing"], opts=F["timing_opts"])
        + '</details>'
        + f'<p class="fine">{esc(F["fine"])}</p>'
    )
    subj = "Home valuation request from " + SITE["domain"] if T["lang"] == "en" else "Solicitud de valuación desde " + SITE["domain"]
    form = mail_form(T, T["lang"], subj, fields, F["submit"], "hv-form")
    steps = "".join(f'<li>{esc(x)}</li>' for x in T["hv_after"])
    up = "../" if T["dir_prefix"] else ""
    me = "Preparada por mí, J.R. Grimaldo" if T["lang"] == "es" else "Prepared by me, J.R. Grimaldo"
    return f"""
<section><div class="wrap hv-grid"><div>
<div class="me-head"><img src="{up}assets/jr-headshot-400.jpg" alt="" width="72" height="72"><div><h1>{esc(T['hv_h1'])}</h1><p class="me-by">{esc(me)}</p></div></div>
<p>{esc(T['hv_p'])}</p>{form}</div>
<aside class="hv-side"><h2>{esc(T['hv_after_h2'])}</h2><ol class="steps">{steps}</ol>
<p class="fine hv-law">{T['hv_law']}</p>
<div class="note"><p style="margin:0">{esc(T['hv_note'])}</p></div></aside></div></section>"""

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
    guide = (f'<a href="sellers-guide.html"><img src="{up}{GUIDE_ES["cover"] if es else GUIDE["cover"]}" alt="" width="400" height="518">'
             f'<b>{esc(GUIDE_ES["title"] if es else "Selling Your Home, Step by Step")}</b>'
             f'<span>{esc("Una guía de 8 páginas para vender su casa, desde prepararla hasta el día del cierre. En español. Se la envío por correo electrónico." if es else "My 8-page guide to selling your home, from getting ready to closing day. Emailed to you.")}</span>'
             f'<span class="go btn quiet">{esc("Obtener esta guía" if es else "Get this guide")}</span></a>')
    fsbo = (f'<a href="{up}fsbo-guide-info.html"><img src="{up}{FSBO_GUIDE["cover"]}" alt="" width="400" height="518">'
            f'<b>Selling Your Home on Your Own, Step by Step</b>'
            f'<span>{esc("Para dueños que venden su casa por su cuenta. Una guía gratis de 8 páginas, con el formulario de divulgación de Carolina del Sur, por correo electrónico. La guía está en inglés." if es else "For owners selling their home on their own. A free 8-page guide, plus the South Carolina disclosure form, emailed to you.")}</span>'
            f'<span class="go btn quiet">{esc("Obtener esta guía" if es else "Get this guide")}</span></a>')
    shelf = guide + fsbo + "".join(
        f'<a href="{b["slug"]}.html"><img src="{up}assets/{b["photo"]}" alt="" width="396" height="601">'
        f'<b>{esc(b["title"])}</b><span>{esc(b["line_es"] if es else b["line"])}</span>'
        f'<span class="go btn quiet">{esc("Obtener este libro" if es else "Get this book")}</span></a>' for b in BOOKS)
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

# Monthly newsletter, "Front Porch Notes with J.R." Each issue has its own page
# under /newsletter/ (issue-1.html, issue-2.html, ...), newest first in this list.
# The email shows short teasers; its "Read more" links jump to #towns, #story
# and #tip on the issue page. Issues are in English; the Spanish archive links to them.
# Texts come from the project docs (Newsletter_Issue1_Towns.md, Newsletter_Issue1_Story.md,
# Newsletter_Seller_Tips.md), approved by J.R. Never publish the "Real facts" notes.

# Issue 1 town table: Greenville MLS and Spartanburg MLS combined (Paragon), pulled 10/29/2026.
# Same search both years: single-family, sold, $150,000-$800,000, closing date Aug 1 - Oct 28.
# A home listed in both systems is counted once. Details: project doc Newsletter_Issue1_Towns.md.
# J.R. 10/29: show last year's home count in words, not a percent change (a "-30%" next to a
# town reads like a loss in value). Price change stays.
# (town, sold 2025, sold 2026, typical price 2025, typical price 2026)
ISSUE1_TOWNS = [
    ("Landrum & Campobello", 50, 66, 333300, 364900),
    ("Inman", 150, 160, 312505, 299000),
    ("Boiling Springs", 141, 121, 297500, 306000),
    ("Greer", 233, 220, 395000, 400000),
    ("Lyman", 74, 72, 310945, 335000),
    ("Duncan", 32, 48, 377500, 334500),
    ("Wellford", 71, 50, 290000, 289450),
    ("Travelers Rest", 83, 83, 462500, 519000),
    ("Taylors", 142, 102, 326000, 339000),
]
ISSUE1_ALL = ("All 10 towns", 976, 922, 334175, 344350)

def _pct(a, b):
    v = round((b - a) / a * 100)
    return ("+" if v > 0 else "") + str(v) + "%" if v else "0%"

def page_issue1():
    def row(r, cls=""):
        t, s25, s26, p25, p26 = r
        return (f'<tr{cls}><th scope="row">{esc(t)}</th><td>{s26}</td><td>{s25}</td>'
                f'<td>${p25:,}</td><td>${p26:,}</td><td>{_pct(p25, p26)}</td></tr>')
    rows = "".join(row(r) for r in ISSUE1_TOWNS) + row(ISSUE1_ALL, ' class="tot"')
    def box(r, cls=""):
        t, s25, s26, p25, p26 = r
        return (f'<li{cls}><b>{esc(t)}</b><span>Homes sold: {s26} ({s25} the same time last year)</span>'
                f'<span>Typical price: ${p25:,} → ${p26:,} ({_pct(p25, p26)})</span></li>')
    boxes = "".join(box(r) for r in ISSUE1_TOWNS) + box(ISSUE1_ALL, ' class="tot"')
    return f"""
<section class="nl-head"><div class="wrap">
<p class="fine"><a href="../newsletter.html">&larr; All newsletters</a></p>
<p class="nl-kicker">Front Porch Notes with J.R. · Issue 1 · November 2026</p>
<h1>Front Porch Notes with J.R.</h1>
<p>News about homes in our part of the Upstate, once a month. Jump to: <a href="#towns">This month in our towns</a> · <a href="#story">One home, one story</a> · <a href="#tip">Seller tip</a></p>
</div></section>

<section id="towns"><div class="wrap nl-body">
<h2>This month in our towns</h2>
<h3>Are home sales up or down around here?</h3>
<p>922 homes sold across our towns from August 1 through October 28. Last year at the same time, 976 sold.</p>
<p>The typical price rose about 3%, to $344,350. And most homes still sold in about a month.</p>
<p>Here's how your town compares.</p>
</div><div class="wrap"><div class="tbl-wrap"><table class="nl-table">
<caption>Homes sold August 1 to October 28, 2026, compared with the same time in 2025</caption>
<thead><tr><th scope="col">Town</th><th scope="col">Homes sold 2026</th><th scope="col">Same time 2025</th>
<th scope="col">Typical price 2025</th><th scope="col">Typical price 2026</th><th scope="col">Price change</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<ul class="nl-boxes"><li class="cap">August 1 to October 28, 2026 compared with 2025</li>{boxes}</ul></div>
<div class="wrap nl-body">
<p class="fine">In smaller towns (Landrum &amp; Campobello, Duncan, Wellford, Lyman), a few sales can swing the typical price a lot from one year to the next. It depends on which homes happened to sell.</p>
<p class="fine">Where the numbers come from: the Greenville MLS and the Spartanburg MLS together, with each home counted once. Single-family homes sold from August 1 to October 28 of each year, priced from $150,000 to $800,000. "Typical price" is the middle price: half the homes sold for more, half for less.</p>
</div></section>

<section class="alt" id="story"><div class="wrap nl-body">
<h2>One home, one story</h2>
<h3>The house with the wrong kind of deed</h3>
<p>A seller in Travelers Rest called me about selling his home. I'll call him Joe. That's not his real name.</p>
<p>Joe had bought the house at a tax sale. That's when the county sells a property because the taxes weren't paid. But the deed you get from a tax sale isn't the kind most buyers can close on.</p>
<p>Before Joe could sell, an attorney had to make sure nobody else had any claim to the property. That's a legal process of its own, and it takes time.</p>
<p>We talked about this before we ever listed. So we got the attorney started right away.</p>
<p>The title work took longer than anyone expected. Our first buyer couldn't wait. The closing date moved again and again, and in the end that contract ended. We kept going.</p>
<p>Our second buyer had a deadline of his own. He was doing a 1031 exchange. That's a tax rule for people selling an investment property: they must buy the next one by a set date. By then, the title work was almost finished. The buyer agreed to close on time, and the attorney finished the work shortly after. Today the new owner has the right kind of deed.</p>
<p>That same month, I helped Joe buy his next home.</p>
<p>Joe and I still work together.</p>
<p><b>The lesson for sellers:</b> if anything about how you got your home is unusual, talk to an agent before you list. Problems with the deed can be fixed, but they take time. It's much easier to start early than to explain a delay to a buyer who's waiting.</p>
<p>Have a question like that about your own home? Text me at <a href="sms:{SITE['phone_tel']}">{SITE['phone']}</a>. It's the fastest way to reach me.</p>
</div></section>

<section id="tip"><div class="wrap nl-body">
<h2>Seller tip</h2>
<h3>Fix it, or leave it?</h3>
<p>Sellers ask me this all the time. My answer has three parts.</p>
<p><b>Fix what's broken.</b> Roof leaks, plumbing problems, anything structural, anything clearly wrong. A buyer's inspection will find these, and you'll likely have to fix them before closing anyway. Fixing them first means fewer surprises, and buyers feel better about the home.</p>
<p><b>Clean everything.</b> A deep clean, carpet cleaning where it's needed, and clearing clutter. It costs little, and the home looks its best in photos and showings.</p>
<p><b>Hold off on updates that are a matter of taste.</b> Paint colors, new carpet, new flooring. You might paint the rooms when your buyer would rather have new carpet. You might pick yellow when your buyer loves blue. Wait and see what your buyer actually wants.</p>
<p>If a buyer asks for one of those updates, we can handle it in the deal. Usually that's a credit toward the buyer's closing costs, or a lower price, so the buyer can make the change their own way. If the buyer has a mortgage, the lender sets limits on credits, and I'll walk you through them.</p>
<p>That way, you spend money only where it matters.</p>
<p>Not sure which list something in your home belongs on? Text me at <a href="sms:{SITE['phone_tel']}">{SITE['phone']}</a>. It's the fastest way to reach me.</p>
</div></section>

<section id="rates"><div class="wrap nl-body">
<h2>Rates this week</h2>
<p>The national average 30-year fixed mortgage rate was <b>7.18%</b> for the week of November 5, 2026. That's down from 7.24% the week before. (Source: Freddie Mac.)</p>
<p>Your rate depends on you. A lender can tell you yours.</p>
</div></section>

<section class="alt"><div class="wrap">
<h2>What's your home worth today?</h2>
<p>Tell me the address. I'll look at your home and the recent sales around it, and send you a written valuation within one business day. Free, no obligation.</p>
<p><a class="btn" href="../home-value.html">What's your home worth today?</a></p>
<p class="nl-sign">Principles Before Profits · J.R. Grimaldo, Real Estate Professional, SC License #95641 · NorthGroup Real Estate, P.O. Box 106, Landrum, SC 29356 · Text <a href="sms:{SITE['phone_tel']}">{SITE['phone']}</a> · Hablo español</p>
<p class="fine">Got this from a friend? <a href="../newsletter.html">Sign up to get Front Porch Notes by email.</a></p>
</div></section>"""

NEWSLETTERS = [
    {"path": "newsletter/issue-1.html", "date": "November 2026",
     "title": "Front Porch Notes, Issue 1",
     "summary": "Are home sales up or down in our towns? Plus the house with the wrong kind of deed, and when to fix it or leave it before you sell.",
     "builder": page_issue1},
]

def page_newsletter(T):
    F = T["nl_fields"]
    es = T["lang"] == "es"
    up = "../" if T["dir_prefix"] else ""
    fields = ('<div class="two">' + field("name", F["name"], req=True) + field("email", F["email"], "email", req=True) + '</div>'
              + f'<p class="fine">{esc(F["fine"])}</p>')
    subj = "Newsletter sign-up from " + SITE["domain"] if not es else "Inscripción al boletín desde " + SITE["domain"]
    form = mail_form(T, T["lang"], subj, fields, F["submit"], "nl-form", ok=F["ok"])
    if NEWSLETTERS:
        items = "".join(f'<li><a href="{up}{n["path"]}"><b>{esc(n["title"])}</b></a>'
                        f'<span class="c"> · {esc(n["date"])}</span><br><span class="fine">{esc(n.get("summary", ""))}</span></li>' for n in NEWSLETTERS)
        past = f'<ul class="nl-list">{items}</ul>'
    else:
        past = f'<div class="empty"><p style="margin:0">{esc(T["nl_empty"])}</p></div>'
    return f"""
<section><div class="wrap"><h1>{esc(T['nl_h1'])}</h1><p>{esc(T['nl_p'])}</p></div></section>
<section class="alt"><div class="wrap"><h2>{esc(T['nl_sign_h2'])}</h2>{form}</div></section>
<section><div class="wrap"><h2>{esc(T['nl_past_h2'])}</h2>{past}</div></section>"""

def page_list(T, h1, items, empty, intro=""):
    cards = "".join(card(x, T) for x in items)
    body = f'<div class="cards">{cards}</div>' if items else f'<div class="empty"><p style="margin:0">{esc(empty)}</p></div>'
    lead = f'<p>{esc(intro)}</p>' if (intro and items) else ""
    return f'<section><div class="wrap"><h1>{esc(h1)}</h1>{lead}{body}</div></section>'

def page_sold(T=EN):
    base = page_list(T, T["so_h1"], SOLD, T["so_empty"], T["so_intro"])
    n_all = len(SOLD) + len(SOLD_MORE)
    stats_top = (f'<p class="stats top"><b>{n_all}</b> {esc(T["so_stats1"])}<br>'
                 f'<b>{REPEAT_FAMILIES}</b> {esc(T["so_stats2"])}</p>')
    base = base.replace('</h1>', '</h1>' + stats_top, 1)
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
            f'<details class="all-sales"><summary>{esc(T["so_see_all"].format(n=n))}</summary>'
            f'<p class="fine">{esc(T["so_fine"])}</p>'
            f'<ul class="sold-list">{rows}</ul></details>'
            f'<p style="margin-top:28px"><a class="btn" href="home-value.html">{esc(T["val_btn"])}</a></p></div>')
    i = base.rfind("</div></section>")
    return base[:i] + more + base[i:]

PRIVACY = {
    "en": {
        "h1": "Privacy",
        "intro": "This page says what this site collects and what I do with it.",
        "sections": [
            ("What I collect", [
                "I collect only what you type into a form: your name, email, phone number, your home or mailing address, and anything you tell me about your home.",
                "I get it only when you send a form. If you don't send a form, I don't get any of it."]),
            ("Why", [
                "I use it to send you the guide or book you asked for, to send you my monthly newsletter, and to answer you.",
                "I don't sell or rent anyone's information."]),
            ("Unsubscribe", [
                "Every newsletter has an unsubscribe link. You can also email me at jr@jrREsales.com, and I'll take you off the list."]),
            ("Facebook", [
                "This site uses the Meta Pixel, a tool from Facebook, to count visits and to measure how well our Facebook ads work. It does not send your name, email or phone number to Facebook."]),
            ("Forms", [
                "The forms on this site are handled by Formspree. Formspree is the service that delivers what you send to my email."]),
        ],
        "contact_h": "Contact",
    },
    "es": {
        "h1": "Privacidad",
        "intro": "Esta página explica qué recoge este sitio y qué hago con eso.",
        "sections": [
            ("Lo que recojo", [
                "Recojo solo lo que usted escribe en un formulario: su nombre, correo electrónico, teléfono, la dirección de su casa o su dirección postal, y lo que me cuente sobre su casa.",
                "Lo recibo solo cuando usted envía un formulario. Si no envía un formulario, no recibo nada de eso."]),
            ("Para qué", [
                "Lo uso para enviarle la guía o el libro que pidió, para enviarle mi boletín mensual y para contestarle.",
                "No vendo ni alquilo la información de nadie."]),
            ("Cancelar la suscripción", [
                "Cada boletín trae un enlace para cancelar la suscripción. También puede escribirme a jr@jrREsales.com y lo quito de la lista."]),
            ("Facebook", [
                "Este sitio usa el Meta Pixel, una herramienta de Facebook, para contar las visitas y medir qué tan bien funcionan nuestros anuncios en Facebook. No envía su nombre, correo electrónico ni número de teléfono a Facebook."]),
            ("Formularios", [
                "Los formularios de este sitio los maneja Formspree. Formspree es el servicio que me entrega por correo electrónico lo que usted envía."]),
        ],
        "contact_h": "Contacto",
    },
}

def page_privacy(T):
    P = PRIVACY[T["lang"]]
    secs = "".join(f'<h2>{esc(h)}</h2>' + "".join(f'<p>{esc(x)}</p>' for x in ps) for h, ps in P["sections"])
    contact = (f'<p>J.R. Grimaldo<br>{esc(BRAND["brokerage"])}<br>{esc(BRAND["office"])}<br>'
               f'<a href="mailto:{SITE["email"]}">jr@jrREsales.com</a><br>'
               f'<a href="sms:{SITE["phone_tel"]}">{"Texto" if T["lang"] == "es" else "Text"}: {SITE["phone"]}</a></p>')
    return f"""
<section><div class="wrap privacy">
  <h1>{esc(P['h1'])}</h1>
  <p>{esc(P['intro'])}</p>
  {secs}
  <h2>{esc(P['contact_h'])}</h2>
  {contact}
</div></section>"""

def page_about(T):
    up = "../" if T["dir_prefix"] else ""
    facts = "".join(f'<div><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in T["ab_facts"])
    return f"""
<section><div class="wrap split">
  <img class="portrait" src="{up}assets/jr-headshot.jpg" alt="{esc(SITE['agent'])}">
  <div><h1>{esc(T['ab_h1'])}</h1>
  <p>{esc(T['ab_p1'])}</p><p>{esc(T['ab_p2'])}</p><p>{esc(T['ab_p4'])}</p>
  <p><a class="btn" href="home-value.html">{esc(T['hero_btn'])}</a></p>
  <p>{esc(T['ab_p3'])}</p><p>{esc(T['ab_p5'])}</p></div>
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
        order = sorted(REVIEWS, key=lambda r: len(r["quote"]))  # shortest first (layout review 11/13); words unchanged
        body = note + '<div class="rv-grid">' + "".join(f'<blockquote><p>{esc(r["quote_es"] if T["lang"] == "es" and r.get("quote_es") else r["quote"])}</p><footer>{esc(r["name"])}{(", "+esc(_where(r["where"], T))) if r.get("where") else ""}</footer></blockquote>' for r in order) + '</div>'
        body += f'<p style="margin:8px 0 26px"><a class="btn" href="home-value.html">{esc(T["val_btn"])}</a></p>'
        body += f'<p>{esc(T["rv_ask"])} <a class="btn quiet" href="{SITE["review_page"]}">{esc(T["rv_btn"])}</a></p>'
    else:
        body = f'<div class="empty"><p>{esc(T["rv_empty"])}</p><a class="btn quiet" href="{SITE["review_page"]}">{esc(T["rv_btn"])}</a></div>'
    return f'<section><div class="wrap"><h1>{esc(T["rv_h1"])}</h1>{body}</div></section>'

# Town pages for local search ("sell my house in Greer"). Sales are pulled
# automatically from SOLD and SOLD_MORE, so a new sale shows up on its town page.
# Only J.R.'s real sales; no dates; no claims about other agents.
# J.R., 10/23/2026: "Go ahead and do anything ... to promote this."
# Focus towns, in J.R.'s order (10/27/2026): footer links and "Other towns I work in".
TOWN_ORDER = ["landrum", "campobello", "inman", "boiling-springs", "greer", "lyman",
              "duncan", "wellford", "travelers-rest", "taylors"]
# Built and kept online (Google already knows them), but not linked in the footer
# or town lists. J.R.: he would not turn down a listing there; he just doesn't
# concentrate there.
TOWN_EXTRA = ["greenville", "simpsonville", "fountain-inn"]
TOWN_PAGES = TOWN_ORDER + TOWN_EXTRA
TOWNS = {
    "landrum": {"name": "Landrum",
        "intro": ["I live in Landrum, and I've been helping my neighbors here buy and sell homes since 2016.",
                  "When you sell with me, you get an agent who knows the streets, the neighborhoods, and what buyers here are looking for. I also work in the towns around us, including Campobello, Inman, and Lyman."],
        "note": "The same family on all three. They bought Page Creek with me, then came back years later to sell it and buy Talbert Trail."},
    "campobello": {"name": "Campobello"},
    "boiling-springs": {"name": "Boiling Springs"},
    "lyman": {"name": "Lyman"},
    "duncan": {"name": "Duncan"},
    "wellford": {"name": "Wellford"},
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
    "Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message.",
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
    title = f"Sell Your Home in {t['name']}, SC – J.R. Grimaldo"
    if key == "landrum":
        desc = "J.R. Grimaldo lives in Landrum and has helped neighbors buy and sell homes here since 2016. Get a free home valuation from him within one business day."
    elif n >= 1:
        desc = (f"J.R. Grimaldo has helped folks buy and sell homes in {t['name']}, SC. "
                "Get a free written home valuation, prepared by J.R. himself, within one business day.")
    else:
        desc = (f"Selling your home in {t['name']}, SC? J.R. Grimaldo lives close by in Landrum. "
                "Get a free written home valuation from him within one business day.")
    return title, desc

def page_town(key):
    t = TOWNS[key]; name = t["name"]; sales = town_sales(name)
    if "intro" in t:
        intro_l = t["intro"]
    else:
        # No numbers (J.R., 10/27/2026): counts change all the time. "Folks" (J.R.'s word, for a small-town feel), not
        # "clients," so it is true where J.R. represented only the buyer.
        n = len(sales)
        if n >= 5:
            first = f"I've been selling homes across the Upstate since 2016, and {name} is one of the places I've worked the most, helping folks buy and sell homes."
        elif n >= 3:
            first = f"I've been selling homes across the Upstate since 2016, and I've helped folks buy and sell homes in {name}."
        elif n >= 1:
            first = f"I live close by in Landrum, and {name} is part of the area I focus on. I've helped folks buy and sell homes here, and I'd be glad to help you sell."
        else:
            first = f"I live close by in Landrum, and {name} is part of the area I focus on. I'd be glad to help you sell your home here."
        intro_l = [first,
                   "I believe in quality over quantity. Every client gets my full attention."]
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
    sales_html = (f'''<section class="alt"><div class="wrap"><h2>My {esc(name)} sales</h2>
<ul class="sold-list">{rows}</ul>{note}
<p><a class="btn quiet" href="sold.html">See all my sales</a></p></div></section>''') if sales else ""
    how = "".join(f"<li>{esc(x)}</li>" for x in TOWN_HOW)
    others = " · ".join(f'<a href="{k}.html">{esc(TOWNS[k]["name"])}</a>' for k in TOWN_ORDER if k != key)
    return f"""
<section><div class="wrap"><div class="me-head"><img src="assets/jr-headshot-400.jpg" alt="" width="72" height="72"><div><h1>Selling your home in {esc(name)}</h1><p class="me-by">J.R. Grimaldo, Landrum, SC</p></div></div>{intro}
<p><a class="btn" href="home-value.html">Get my free valuation</a></p></div></section>
{lst_html}
{sales_html}
<section><div class="wrap"><h2>What you get when you sell with me</h2><ul class="plain">{how}</ul></div></section>
<section class="alt"><div class="wrap"><h2>What's your {esc(name)} home worth?</h2>
<p>A free written valuation, within one business day.</p>
<a class="btn" href="home-value.html">Get my free valuation</a>
<p class="fine" style="margin-top:22px">Other towns I work in: {others}</p></div></section>"""

def page_contact(T):
    F = T["ct_fields"]
    fields = ('<div class="two">' + field("name", F["name"], req=True) + field("email", F["email"], "email", req=True) + '</div>'
              + field("phone", F["phone"], "tel") + field("message", F["message"], textarea=True, req=True)
              + (f'<p class="fine">{esc(T["ct_fine"])}</p>' if T.get("ct_fine") else ""))
    subj = "Message from " + SITE["domain"] if T["lang"] == "en" else "Mensaje desde " + SITE["domain"]
    form = mail_form(T, T["lang"], subj, fields, F["submit"], "ct-form")
    return f"""
<section><div class="wrap ct-wrap"><div>
<h1>{esc(T['ct_h1'])}</h1><p>{esc(T['ct_p'])}</p>
<div class="ct-btns">
  <a class="btn btn-big" href="sms:{SITE['phone_tel']}">{esc(T['text_btn'])}</a>
  <div class="ct-small"><a class="btn quiet" href="tel:{SITE['phone_tel']}">{'Llamar' if T['lang'] == 'es' else 'Call'}</a><a class="btn quiet" href="mailto:{SITE['email']}">{'Correo' if T['lang'] == 'es' else 'Email'}</a></div>
  <p class="fine">{esc(SITE['email'])}<br>{esc(T['ct_office'])}: {esc(BRAND['office'])}</p>
</div></div>
<div class="ct-form"><h2>{esc(T['ct_form_h2'])}</h2>{form}</div></div></section>"""


# ------------------------------------------------------------- SELLER'S GUIDE
# Request page for J.R.'s 8-page guide. Emailed, not a plain download (J.R., 11/4/2026).
# The site address is written jrREsales.com on this page (J.R., 11/4/2026).
GUIDE = {
    "title": "Selling Your Home, Step by Step",
    "pdf": "assets/sellers-guide.pdf",
    "cover": "assets/sellers-guide-cover.jpg",
}

GUIDE_LINE_EN = "Free, 8 pages. I'll email it to you myself, usually within a few hours."
GUIDE_LINE_ES = "Gratis, 8 páginas. Se la mando yo mismo por correo electrónico, por lo general en unas pocas horas."
GUIDE_ES = {
    "title": "Cómo vender su casa, paso a paso",
    "cover": "assets/guia-vendedores-cover.jpg",
}


def guide_top(cover, kicker, h1, line, form, bullets=None, bullets_label="", who=""):
    """Phone-first top of a request page: small cover beside the title, one short line,
    then the form, all on the first phone screen (J.R., 11/5/2026)."""
    short = f'<p class="gwho">{esc(who)}</p>' if who else ""
    if bullets:
        short += (f'<p class="gshort-h">{esc(bullets_label)}</p><ul class="gshort">'
                 + "".join(f'<li>{esc(b)}</li>' for b in bullets) + '</ul>')
    return (f'<section class="gtop{" has-short" if bullets else ""}" id="request"><div class="wrap"><div class="ghead">{cover}'
            f'<div><p class="kick">{esc(kicker)}</p><h1>{esc(h1)}</h1></div></div>'
            f'{short}<p class="gline">{esc(line)}</p>{form}</div></section>')

def again_btn(label):
    """Second button at the end of a request page; jumps back up to the form (J.R., 11/6/2026)."""
    return f'<p class="gagain"><a class="btn" href="#request">{esc(label)}</a></p>'

def page_guide(T=None):
    es = bool(T) and T["lang"] == "es"
    up = "../" if es else ""
    cov = GUIDE_ES["cover"] if es else GUIDE["cover"]
    cover = ""
    if (SRC / cov).exists():
        alt = ("Portada de la guía para vendedores, Cómo vender su casa, paso a paso" if es
               else "Cover of the Seller's Guide, Selling Your Home, Step by Step")
        cover = f'<img src="{up}{cov}" alt="{esc(alt)}" width="400" height="518">'
    if es:
        fields = ('<input type="hidden" name="idioma" value="es">'
                  + '<div class="two">' + field("name", "Su nombre", req=True) + field("email", "Correo electrónico", "email", req=True) + '</div>'
                  + '<p class="fine">También recibirá mi boletín mensual, Front Porch Notes, que está en inglés. '
                    'Puede cancelarlo cuando quiera. Nunca vendo su información. La uso solo para contestarle y enviarle lo que pidió.</p>')
        form = mail_form(T, "es", "Solicitud: Guía para vendedores (español)", fields, "Envíeme la guía", "sg-form",
                         ok="Gracias. Recibí su solicitud. Le enviaré la guía yo mismo por correo electrónico, por lo general en unas pocas horas.")
        parts = [
            ("Parte 1: Antes de poner su casa a la venta", "Qué arreglar, qué limpiar y qué puede esperar. Los papeles que conviene reunir. Cómo prepararse para el día de las fotos. Cómo fijamos el precio. Y cómo comprar su próxima casa al mismo tiempo."),
            ("Parte 2: Mientras su casa está a la venta", "Cómo los compradores encuentran su casa. Cómo se programan las visitas, cómo funciona la caja para la llave y qué hacer antes de que lleguen los compradores. Y qué pensar de los comentarios de los compradores."),
            ("Parte 3: De la oferta al cierre", "Qué pasa cuando llega una oferta. El período de revisión, las reparaciones, la inspección de termitas y el appraisal (el informe de valor que pide el banco). Las semanas hasta el cierre, una por una, y qué esperar el día del cierre."),
        ]
        kicker, h1 = "Guía gratis para vendedores", GUIDE_ES["title"]
        p1 = ("¿Está pensando en vender? Esta guía corta le explica toda la venta, desde que prepara su casa para ponerla a la venta "
              "hasta el día en que entrega las llaves. Son 8 páginas, en palabras sencillas, y la escribí yo a partir de mis propias ventas aquí en el Upstate.")
        p2 = "Dígame a dónde se la envío. Se la mando yo mismo por correo electrónico, por lo general en unas pocas horas. Es gratis."
        btn, inside, req_h2 = "Envíeme la guía", "Qué contiene", "Pida su copia gratis"
    else:
        fields = ('<div class="two">' + field("name", "Your name", req=True) + field("email", "Email", "email", req=True) + '</div>'
                  + '<p class="fine">You\'ll also get my monthly newsletter, Front Porch Notes. '
                    'You can stop it anytime. I never sell your information. I use it only to answer you and to send what you asked for.</p>')
        form = mail_form(EN, "en", "Seller's Guide request from jrREsales.com", fields, "Email me the guide", "sg-form",
                         ok="Thank you. I got your request. I'll email the guide to you myself, usually within a few hours.")
        parts = [
            ("Part 1: Getting ready to list", "What to fix, what to clean, and what can wait. The papers to gather. How to get ready for photo day. How we set your price. And how to buy your next home at the same time."),
            ("Part 2: While your home is for sale", "How buyers find your home. How showings get booked, how the lockbox works, and what to do before buyers arrive. And what to make of buyer feedback."),
            ("Part 3: From offer to closing", "What happens when an offer comes in. The due diligence period, repair requests, the termite inspection, and the appraisal. A week-by-week look at the road to closing, and what to expect on closing day."),
        ]
        kicker, h1 = "Free Seller's Guide", "Selling Your Home, Step by Step"
        p1 = ("Thinking about selling? This short guide walks you through the whole sale, from getting ready to list to the day you hand over the keys. "
              "It's 8 pages, in plain English, and written by me from my own sales here in the Upstate.")
        p2 = "Tell me where to send it. I'll email it to you myself, usually within a few hours. It's free."
        btn, inside, req_h2 = "Email me the guide", "What's inside", "Get your free copy"
    p_html = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in parts)
    line = (GUIDE_LINE_ES if es else GUIDE_LINE_EN)
    short = ([ "Antes de vender: arreglos, papeles, fotos, precio",
               "A la venta: visitas, caja para la llave, comentarios",
               "Oferta y cierre: inspecciones, appraisal (el informe de valor que pide el banco), cierre"] if es else
             [ "Getting ready to list: repairs, papers, photos, and price",
               "While it's for sale: showings, the lockbox, and feedback",
               "Offer to closing: inspections, the appraisal, and closing day"])
    return guide_top(cover, kicker, h1, line, form, short, inside) + f"""
<section class="alt"><div class="wrap"><h2>{esc(inside)}</h2><p class="glong">{esc(p1)}</p><div class="truths">{p_html}</div>{again_btn(btn)}</div></section>"""


# ------------------------------------------------------------- FSBO GUIDE
# Request page for J.R.'s 8-page guide for owners selling on their own (J.R., 11/5/2026).
# Emailed by J.R. with three attachments (claude/FSBO_Guide_Reply_Email.md). The QR code on
# the FSBO letter points to this page, so keep the address fsbo-guide.html.
FSBO_GUIDE = {"title": "Selling Your Home on Your Own, Step by Step", "cover": "assets/fsbo-guide-cover.jpg"}

def page_fsbo_guide(info=False):
    """info=False: fsbo-guide.html, form first (QR code on letters, source=letter).
    info=True: fsbo-guide-info.html for website visitors (source=website), short bullets before the form (J.R., 11/6/2026)."""
    cover = ""
    if (SRC / FSBO_GUIDE["cover"]).exists():
        cover = f'<img src="{FSBO_GUIDE["cover"]}" alt="Cover of the guide Selling Your Home on Your Own, Step by Step" width="400" height="518">'
    fields = (f'<input type="hidden" name="source" value="{"website" if info else "letter"}">'
              + '<div class="two">' + field("name", "Your name", req=True) + field("email", "Email", "email", req=True) + '</div>'
              + '<p class="fine">You\'ll also get my monthly newsletter, Front Porch Notes. '
                'You can stop it anytime. I never sell your information. I use it only to answer you and to send what you asked for.</p>')
    form = mail_form(EN, "en", "FSBO Guide request from jrREsales.com", fields, "Email me the guide", "fg-form",
                     ok="Thank you. I got your request. I'll email the guide to you myself, usually within a few hours.")
    parts = [
        ("Part 1: Pricing It Right on Your Own", "Where to find real sold prices, why online estimates miss, why starting high costs you, and what selling on your own still costs."),
        ("Part 2: Getting Buyers in the Door", "Where buyers actually look, tips for better photos, showings and safety, the yard sign, and what to do when agents call."),
        ("Part 3: Offers, Paperwork, and Closing in South Carolina", "What you must tell buyers by law, the contract, the due diligence period, repair requests, the appraisal, the closing attorney, and a checklist from offer to closing."),
    ]
    p_html = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in parts)
    short = ["Pricing it right, and what it still costs",
             "Where buyers look, photos, safe showings",
             "The disclosure form most owners must give buyers",
             "Offers, inspections, and closing day"] if info else None
    top = guide_top(cover, "Free guide for owners selling on their own", FSBO_GUIDE["title"],
                    "Free, 8 pages, plus the South Carolina disclosure form. I'll email it to you myself, usually within a few hours.", form,
                    short, "What's inside")
    return top + f"""
<section class="alt"><div class="wrap"><h2>What's inside</h2>
<p class="glong">Selling your home yourself? That's your call, and I respect it. This 8-page guide walks you through it in order: pricing, showings, and closing in South Carolina. It's honest about the parts that usually trip owners up.</p>
<p class="glong">It comes with the South Carolina disclosure form and a one-page showing checklist.</p>
<div class="truths">{p_html}</div>{again_btn("Email me the guide")}</div></section>"""


# ------------------------------------------------------------- SALES LIST
# Request page for a one-page list of recent sales near the visitor (J.R., 11/5/2026).
# Reached only by a QR code in J.R.'s guides; not in the menu. J.R. emails the list himself.
def page_sales_list():
    fields = ('<input type="hidden" name="request" value="saleslist">'
              + '<div class="two">' + field("name", "Your name", req=True) + field("email", "Email", "email", req=True) + '</div>'
              + '<div class="pair">' + field("street", "Home address (street)", req=True) + field("city", "Town", req=True) + '</div>'
              + '<p class="fine">You\'ll also get my monthly newsletter, Front Porch Notes. You can stop it any time. I never sell your information. I use it only to answer you and to send what you asked for.</p>')
    form = mail_form(EN, "en", "Sales list request from jrREsales.com", fields, "Send me the list", "sl-form",
                     ok="Thank you. I got your request. I'll email it to you myself, usually within a day.")
    return guide_top("", "Free, from J.R. Grimaldo", "A list of recent sales near you",
                     "Similar homes that sold near you, with the real sold prices. I'll email it to you myself, usually within a day.", form) + """
<section class="alt"><div class="wrap"><p class="glong">I'll send you a one-page list of similar homes that sold near you, with the real sold prices. No estimate, no pressure, no cost.</p>""" + again_btn("Send me the list") + """</div></section>"""


# ------------------------------------------------------------- BUYER'S GUIDE (UNLISTED)
# J.R. sends this link himself to friends, family, past clients and their referrals (11/6/2026).
# Not in the menu, home page, Free Guides & Books, or sitemap; noindex. PDF: /assets/buyers-guide.pdf
# (fixed name; later versions replace the file).
BUYERS_GUIDE_INTRO = "Thinking about buying? This short guide walks you through it in order, from getting pre-qualified to the day you get the keys."
BUYERS_GUIDE_PARTS = [
    ("Part 1: Getting Ready to Buy", "Getting pre-qualified, then pre-approved. Talk to a lender. The costs to plan for besides the down payment. The buyer agreement, my fee, and your wish list."),
    ("Part 2: Finding Your Home", "Getting new listings by email, sending me the homes you like, keeping notes as we tour, and what to look at on a showing."),
    ("Part 3: From Offer to Closing", "Deciding what to offer, the seller's disclosure form, earnest money, due diligence, inspections and repairs, the appraisal, why to hold off on new credit, and closing day."),
]
BUYERS_GUIDE = {"title": "Buying Your Home, Step by Step", "cover": "assets/buyers-guide-cover.jpg"}

def page_buyers_guide():
    cover = ""
    if (SRC / BUYERS_GUIDE["cover"]).exists():
        cover = f'<img src="{BUYERS_GUIDE["cover"]}" alt="Cover of the guide Buying Your Home, Step by Step" width="400" height="518">'
    fields = ('<input type="hidden" name="guide" value="buyers">'
              + '<div class="two">' + field("name", "Your name", req=True) + field("email", "Email", "email", req=True) + '</div>'
              + '<p class="fine">You\'ll also get my monthly newsletter, Front Porch Notes. '
                'You can stop it anytime. I never sell your information. I use it only to answer you and to send what you asked for.</p>')
    form = mail_form(EN, "en", "Buyer's Guide request from jrREsales.com", fields, "Email me the guide", "bg-form",
                     ok="Thank you. I got your request. I'll email the guide to you myself, usually within a few hours.")
    parts = BUYERS_GUIDE_PARTS
    p_html = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in parts)
    top = guide_top(cover, "Free Buyer's Guide", BUYERS_GUIDE["title"],
                    "Free, 8 pages. I'll email it to you myself, usually within a few hours.", form)
    return top + f"""
<section class="alt"><div class="wrap"><h2>What's inside</h2>
<p class="glong">{esc(BUYERS_GUIDE_INTRO)}</p>
<div class="truths">{p_html}</div>{again_btn("Email me the guide")}</div></section>"""


# ------------------------------------------------------------- TAX SALE GUIDE
# Request pages for J.R.'s 8-page tax sale guide, English and Spanish (J.R., 11/11/2026).
# The guide itself prints these exact addresses ("Newest edition of this guide"), so they never move:
# tax-sale-guide.html and es/tax-sale-guide.html. Text of the guide: claude/Tax_Sale_Guide_Draft*.md
# (owned by "Creating guides and books"). PDFs, when delivered: assets/tax-sale-guide.pdf and
# assets/guia-subastas-impuestos.pdf (same names forever; each edition replaces them).
TAX_GUIDE = {
    "en": {"title": "Tax Sales in Greenville and Spartanburg, Start to Finish",
           "sub": "From your first bid to selling the property once it's yours.",
           "cover": "assets/tax-sale-guide-cover.jpg",
           "kicker": "Free Tax Sale Guide · 2026 Edition",
           "who": "For anyone who bought, or is thinking of buying, at a Greenville or Spartanburg County tax sale.",
           "label": "What's inside",
           "short": ["Finding properties, and what to check before you bid",
                     "Sale day, county by county",
                     "The 12 months, the tax deed, and clearing the title",
                     "Pricing the property to sell"],
           "line": "Free, 8 pages. I'll email it to you myself, usually within a few hours.",
           "name": "Your name", "email": "Email",
           "fine": "You'll also get my monthly newsletter, Front Porch Notes. You can stop it anytime. I never sell your information. I use it only to answer you and to send what you asked for.",
           "subject": "Tax Sale Guide request from jrREsales.com",
           "btn": "Email me the guide",
           "ok": "Thank you. I got your request. I'll email the guide to you myself, usually within a few hours.",
           "intro": "Bought at a tax sale, or thinking about it? This guide walks you through it in order, from your first bid to selling the property once it's yours. It's 8 pages, in plain English, and covers both Greenville and Spartanburg counties.",
           "parts": [
               ("Part 1: Before the sale", "What a tax sale is. Where the counties list the properties. What to check before you bid: road access, leftover strips, mobile homes, and debts that stay with the land."),
               ("Part 2: Sale day", "How to sign up, bid, and pay. Greenville and Spartanburg side by side: dates, places, payment, and who to call."),
               ("Part 3: The 12 months", "When the owner pays back. The interest you earn and the limit on it, the money above the taxes, and mobile homes."),
               ("Part 4: The tax deed", "When the owner doesn't pay back. The last notice, getting your tax deed, and what a tax deed is and isn't."),
               ("Part 5: Once you have the deed", "Your first steps, and clearing the title with a quiet title case."),
               ("Part 6: Pricing it to sell", "What sets the price of tax-sale land, and the papers buyers will ask to see."),
           ],
           "small": "The guide explains the process in plain words. It isn't legal advice.",
           "alt": "Cover of the guide Tax Sales in Greenville and Spartanburg, Start to Finish"},
    "es": {"title": "Subastas por impuestos en Greenville y Spartanburg, de principio a fin",
           "sub": "Desde su primera oferta hasta vender la propiedad cuando ya es suya.",
           "cover": "assets/guia-subastas-impuestos-cover.jpg",
           "kicker": "Guía gratis de subastas por impuestos · Edición 2026",
           "who": "Para cualquier persona que compró, o piensa comprar, en una subasta por impuestos del condado de Greenville o de Spartanburg.",
           "label": "Qué contiene",
           "short": ["Cómo encontrar propiedades y qué revisar antes de ofrecer",
                     "El día de la subasta, condado por condado",
                     "Los 12 meses, la escritura fiscal y cómo limpiar el título",
                     "Cómo ponerle precio para vender"],
           "line": "Gratis, 8 páginas. Se la mando yo mismo por correo electrónico, por lo general en unas pocas horas. Hablo español.",
           "name": "Su nombre", "email": "Correo electrónico",
           "fine": "También recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Puede cancelarlo cuando quiera. Nunca vendo su información. La uso solo para contestarle y enviarle lo que pidió.",
           "subject": "Solicitud: Guía de subastas por impuestos (español)",
           "btn": "Envíeme la guía",
           "ok": "Gracias. Recibí su solicitud. Le enviaré la guía yo mismo por correo electrónico, por lo general en unas pocas horas.",
           "intro": "¿Compró en una subasta por impuestos, o lo está pensando? Esta guía le explica todo en orden, desde su primera oferta hasta vender la propiedad cuando ya es suya. Son 8 páginas, en palabras sencillas, para los condados de Greenville y Spartanburg.",
           "parts": [
               ("Parte 1: Antes de la subasta", "Qué es una subasta por impuestos. Dónde publican los condados las propiedades. Qué revisar antes de ofrecer: el acceso por carretera, los pedazos sobrantes, las casas móviles y las deudas que se quedan con el terreno."),
               ("Parte 2: El día de la subasta", "Cómo inscribirse, ofrecer y pagar. Greenville y Spartanburg lado a lado: fechas, lugares, pagos y a quién llamar."),
               ("Parte 3: Los 12 meses", "Cuando el dueño paga. Los intereses que usted gana y su límite, el dinero por encima de los impuestos y las casas móviles."),
               ("Parte 4: La escritura fiscal", "Cuando el dueño no paga. El último aviso, cómo recibe su escritura fiscal (tax deed) y lo que es, y no es, esa escritura."),
               ("Parte 5: Cuando ya tiene la escritura", "Sus primeros pasos, y cómo limpiar el título con un juicio para aclararlo (quiet title)."),
               ("Parte 6: Cómo ponerle precio para vender", "Lo que define el precio de un terreno de subasta, y los papeles que los compradores van a querer ver."),
           ],
           "small": "La guía explica el proceso en palabras sencillas. No es asesoría legal.",
           "alt": "Portada de la guía Subastas por impuestos en Greenville y Spartanburg, de principio a fin"},
}

def page_tax_guide(T):
    lang = T["lang"]; G = TAX_GUIDE[lang]
    up = "../" if lang == "es" else ""
    cover = ""
    if (SRC / G["cover"]).exists():
        cover = f'<img src="{up}{G["cover"]}" alt="{esc(G["alt"])}" width="400" height="518">'
    fields = ('<input type="hidden" name="guide" value="tax-sale">'
              + '<div class="two">' + field("name", G["name"], req=True) + field("email", G["email"], "email", req=True) + '</div>'
              + f'<p class="fine">{esc(G["fine"])}</p>')
    form = mail_form(T, lang, G["subject"], fields, G["btn"], "tg-form", ok=G["ok"])
    p_html = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in G["parts"])
    top = guide_top(cover, G["kicker"], G["title"], G["line"], form, G["short"], G["label"], who=G["who"])
    return top + f"""
<section class="alt"><div class="wrap"><h2>{esc(G['label'])}</h2>
<p class="glong">{esc(G['intro'])}</p>
<div class="truths">{p_html}</div>
<p class="fine">{esc(G['small'])}</p>{again_btn(G['btn'])}</div></section>"""

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
.rp pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;font-size:1rem;background:var(--stone);border-radius:10px;padding:14px 16px;max-width:620px;margin:0}
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
  <p id="tip" style="font-weight:600;color:#8a5a00;white-space:pre-line" hidden></p>
  <h2>Text message</h2><pre id="tx"></pre>
  <h2>Email</h2><pre id="em"></pre>
</main>
<script>
var NOTES={
 en:{
  v:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your home value request for {addr}. I'm pulling the recent sales near you now, and you'll have your valuation by email within one business day. Any questions in the meantime, just text me here. - J.R.",
     subj:"Your home value request for {addr}",
     mail:"Hi {first},\n\nThank you for asking me to value your home at {addr}. I got your request, and I'm on it.\n\nI'm a licensed South Carolina Real Estate Professional, and I prepare every valuation myself. I'll look at the recent sales near you and at your home's details, then send you a written valuation within one business day, with the sales I used so you can see the reasoning. It's my opinion of value as a Real Estate agent, not an appraisal.\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nIf you'd like to talk sooner, text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message."},
  n:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. Thanks for signing up for my newsletter. It comes once a month. If you ever have a question about your home, just text me here. - J.R.",
     subj:"Thanks for signing up for my newsletter",
     mail:"Hi {first},\n\nThank you for signing up for my monthly newsletter. You're on the list, and the next issue will come to this email address.\n\nIf you ever have a question about your home or the market, text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message."},
  b:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your book request from my website. It goes in the mail in the next few days. If you ever want to talk about your home, just text me here. - J.R.",
     subj:"Your free book request",
     mail:"Hi {first},\n\nThank you for asking. I got your request, and it will go in the mail to {addr} in the next few days.\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nNo strings attached. If you ever want to talk about selling or buying a home, text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message."},
  g:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. Thanks for asking for my Seller's Guide. Here it is: https://jrREsales.com/assets/sellers-guide.pdf - J.R.",
     subj:"Your Seller's Guide: Selling Your Home, Step by Step",
     mail:"Hi {first},\n\nThank you for asking for my Seller's Guide, \"Selling Your Home, Step by Step.\" You can open or save it here:\n\nhttps://jrREsales.com/assets/sellers-guide.pdf\n\nIt walks through a home sale from getting ready to list all the way to closing day.\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nIf you have a question about your own home, text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message."},
  f:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I just emailed you the guide you asked for. - J.R.",
     subj:"The guide you asked for",
     mail:"Hi {first},\n\nHere's the guide you asked for, plus two things that go with it:\n\n1. Selling Your Home on Your Own, Step by Step.\nhttps://jrREsales.com/assets/fsbo-guide.pdf\n\n2. The South Carolina disclosure form. You must give this to the buyer before you both sign a contract.\nhttps://jrREsales.com/assets/sc-disclosure-form.pdf\n\n3. A one-page showing checklist for your fridge.\nhttps://jrREsales.com/assets/fsbo-showing-checklist.pdf\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nIf you have a question, or you'd like a list of recent sales near you, just ask. No cost, no strings. Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message.\n\nBest of luck with your sale."},
  y:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I just emailed you the guide you asked for. - J.R.",
     subj:"The guide you asked for",
     mail:"Hi {first},\n\nHere's the guide you asked for: Buying Your Home, Step by Step.\nhttps://jrREsales.com/assets/buyers-guide.pdf\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nIf you have a question, or you're ready to start looking, text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message."},
  s:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I just emailed you the list of recent sales near {addr}. - J.R.",
     subj:"Recent sales near {addr}",
     tip:"Before you send: attach the one-page sales list for this address.",
     mail:"Hi {first},\n\nHere's the list of recent sales near {addr} that you asked for. It's attached. These are similar homes that sold nearby, with the real sold prices.\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nIf you have a question about any of them, just ask. Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message."},
  c:{text:"Hi {first}, this is J.R. Grimaldo with NorthGroup Real Estate. I got your message from my website. What's a good time to talk? You can also reach me right here by text. - J.R.",
     subj:"Thanks for reaching out",
     mail:"Hi {first},\n\nThank you for your message. I got it and wanted you to know right away.\n\nYou'll also get my monthly newsletter, Front Porch Notes. If you'd rather not, just reply and let me know.\n\nWhat's a good time to talk? Text me at 864-381-2326. It's the fastest way to reach me. If you'd rather call and I don't pick up, please leave a message. You can also simply reply to this email."}},
 es:{
  v:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su solicitud de valuación para {addr}. Ya estoy revisando las ventas recientes cerca de usted, y tendrá su valuación por correo en un día hábil. Si tiene alguna pregunta, escríbame aquí. - J.R.",
     subj:"Su solicitud de valuación para {addr}",
     mail:"Hola {first}:\n\nGracias por pedirme la valuación de su casa en {addr}. Recibí su solicitud y ya estoy trabajando en ella.\n\nSoy Profesional de Bienes Raíces con licencia en Carolina del Sur y preparo cada valuación personalmente. Voy a revisar las ventas recientes cerca de usted y los detalles de su casa, y le enviaré una valuación por escrito en un día hábil, con las ventas que usé para que vea el razonamiento. Es mi opinión de valor como agente de bienes raíces, no un appraisal (el informe de valor que pide el banco).\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\nSi prefiere hablar antes, envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje."},
  n:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Gracias por inscribirse a mi boletín. Sale una vez al mes. Si algún día tiene una pregunta sobre su casa, escríbame aquí. - J.R.",
     subj:"Gracias por inscribirse a mi boletín",
     mail:"Hola {first}:\n\nGracias por inscribirse a mi boletín mensual. Ya está en la lista, y el próximo boletín le llegará a este correo.\n\nSi algún día tiene una pregunta sobre su casa o el mercado, envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje."},
  b:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su solicitud de libro desde mi página web. Sale por correo en los próximos días. Si algún día quiere hablar de su casa, escríbame aquí. - J.R.",
     subj:"Su solicitud de libro gratis",
     mail:"Hola {first}:\n\nGracias por pedirlo. Recibí su solicitud, y saldrá por correo a {addr} en los próximos días.\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\nSin compromiso. Si algún día quiere hablar de vender o comprar una casa, envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje."},
  g:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Gracias por pedir mi guía para vendedores. Aquí la tiene: https://jrREsales.com/assets/guia-vendedores.pdf - J.R.",
     subj:"Su guía para vendedores: Cómo vender su casa, paso a paso",
     mail:"Hola {first}:\n\nGracias por pedir mi guía para vendedores, \"Cómo vender su casa, paso a paso\". Puede abrirla o guardarla aquí:\n\nhttps://jrREsales.com/assets/guia-vendedores.pdf\n\nLe explica toda la venta, desde que prepara su casa hasta el día del cierre.\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\nSi tiene alguna pregunta sobre su casa, envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje."},
  y:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Le acabo de enviar por correo la guía que me pidió. - J.R.",
     subj:"La guía que me pidió",
     mail:"Hola {first}:\n\nAquí está la guía que me pidió: Buying Your Home, Step by Step (Cómo comprar su casa, paso a paso). La guía está en inglés.\nhttps://jrREsales.com/assets/buyers-guide.pdf\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\nSi tiene alguna pregunta, o ya está listo para empezar a buscar, envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje."},
  f:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Le acabo de enviar por correo la guía que me pidió. - J.R.",
     subj:"La guía que me pidió",
     mail:"Hola {first}:\n\nAquí está la guía que me pidió, y dos cosas que van con ella. Los tres documentos están en inglés.\n\n1. Selling Your Home on Your Own, Step by Step (Cómo vender su casa por su cuenta, paso a paso).\nhttps://jrREsales.com/assets/fsbo-guide.pdf\n\n2. El formulario de divulgación de Carolina del Sur. Debe entregárselo al comprador antes de que los dos firmen un contrato.\nhttps://jrREsales.com/assets/sc-disclosure-form.pdf\n\n3. Una lista de una página para las visitas, para su refrigerador.\nhttps://jrREsales.com/assets/fsbo-showing-checklist.pdf\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\nSi tiene alguna pregunta, o quiere una lista de ventas recientes cerca de usted, solo pregúnteme. Sin costo y sin compromiso. Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje.\n\nLe deseo mucha suerte con su venta."},
  s:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Le acabo de enviar por correo la lista de ventas recientes cerca de {addr}. - J.R.",
     subj:"Ventas recientes cerca de {addr}",
     tip:"Before you send: attach the one-page sales list for this address.",
     mail:"Hola {first}:\n\nAquí está la lista de ventas recientes cerca de {addr} que me pidió. Va adjunta. Son casas parecidas que se vendieron cerca, con los precios reales de venta. La lista está en inglés.\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\nSi tiene alguna pregunta, solo pregúnteme. Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje."},
  c:{text:"Hola {first}, le saluda J.R. Grimaldo de NorthGroup Real Estate. Recibí su mensaje desde mi página web. ¿A qué hora le queda bien que hablemos? También puede escribirme aquí. - J.R.",
     subj:"Gracias por comunicarse",
     mail:"Hola {first}:\n\nGracias por su mensaje. Lo recibí y quería avisarle de inmediato.\n\nTambién recibirá mi boletín mensual, Front Porch Notes, que está en inglés. Si prefiere no recibirlo, solo responda a este correo y dígamelo.\n\n¿A qué hora le queda bien que hablemos? Envíeme un texto al 864-381-2326. Es la forma más rápida de comunicarse conmigo. Si prefiere llamar y no contesto, por favor deje un mensaje. También puede simplemente responder a este correo."}}
};
var q=new URLSearchParams(location.hash.slice(1));
var d={t:['c','b','n','g','f','s','y'].indexOf(q.get('t'))>=0?q.get('t'):'v',l:q.get('l')==='es'?'es':'en',n:q.get('n')||'',p:(q.get('p')||'').replace(/[^0-9+]/g,''),e:q.get('e')||'',a:q.get('a')||''};
var first=(d.n.split(/\s+/)[0]||'').replace(/^./,function(c){return c.toUpperCase();});
function fill(s){return s.replace(/\{first\}/g,first||(d.l==='es'?'':'there')).replace(/\{addr\}/g,d.a||(d.l==='es'?'su casa':'your home')).replace(/^Hola :/,'Hola:').replace(/^Hola ,/,'Hola,');}
function show(){
  var N=NOTES[d.l][d.t]||NOTES.en[d.t],tx=fill(N.text),sj=fill(N.subj),bd=fill(N.mail);
  document.documentElement.lang=d.l;
  document.getElementById('h').textContent=(d.l==='es'?'Responder a ':'Reply to ')+(d.n||'?');
  document.getElementById('who').textContent=[d.t==='v'?(d.l==='es'?'Solicitud de valuación':'Home value request'):d.t==='b'?(d.l==='es'?'Solicitud de libros':'Book request'):d.t==='n'?(d.l==='es'?'Inscripción al boletín':'Newsletter sign-up'):d.t==='g'?(d.l==='es'?'Guía del vendedor':"Seller's Guide request"):d.t==='f'?'FSBO Guide request':d.t==='s'?'Sales list request':d.t==='y'?"Buyer's Guide request":(d.l==='es'?'Mensaje':'Message'),d.a,d.p,d.e].filter(Boolean).join(' · ');
  var tp=document.getElementById('tip');if(N.tip){tp.textContent=N.tip;tp.hidden=false;}else{tp.hidden=true;}
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

# W7 (J.R. 11/13/2026): titles about 60 characters, descriptions about 160, important words first. No REALTOR® (W4).
META_EN = {
 "index.html": ("Sell Your Home in Landrum & the Upstate SC – J.R. Grimaldo",
   "Selling in Landrum or the Upstate SC? J.R. Grimaldo, Real Estate Professional since 2016, prepares a free written home valuation himself within one business day."),
 "home-value.html": ("What's My Home Worth? Free Home Valuation – J.R. Grimaldo",
   "Find out what your Upstate SC home is worth. J.R. Grimaldo prepares a free written valuation himself, from recent sales near you, within one business day."),
 "listings.html": ("My Listings – J.R. Grimaldo, Real Estate Professional",
   "Homes for sale now with J.R. Grimaldo, Real Estate Professional, in Landrum and the Upstate SC."),
 "sold.html": ("Sold Homes – J.R. Grimaldo, Real Estate Professional",
   "{n} homes sold and bought since 2016 in Greer, Taylors, Inman, Landrum, and across the Upstate SC. {r} families came back to work with J.R. again."),
 "about.html": ("About J.R. Grimaldo – Real Estate Professional, Landrum SC",
   "Meet J.R. Grimaldo, a licensed South Carolina Real Estate Professional in Landrum since 2016. Quality over quantity and quick replies. Hablo español."),
 "reviews.html": ("Client Reviews – J.R. Grimaldo, Real Estate Professional",
   "What clients say about selling and buying homes with J.R. Grimaldo, Real Estate Professional, in Landrum and the Upstate SC."),
 "free-books.html": ("Free Guides & Books on Selling Your Home – J.R. Grimaldo",
   "Free guides and books on selling your home from J.R. Grimaldo in Landrum, SC: an 8-page Seller's Guide by email and two printed books by mail. No cost."),
 "newsletter.html": ("Monthly Newsletter, Front Porch Notes – J.R. Grimaldo",
   "Free monthly email: what homes sold for in Landrum and nearby Upstate SC towns, whether sales are up or down, and where mortgage rates stand."),
 "contact.html": ("Contact J.R. Grimaldo, Real Estate Professional",
   "Text J.R. Grimaldo at 864-381-2326. It's the fastest way to reach him. If you call and he doesn't pick up, leave a message. Landrum and Upstate SC Real Estate."),
 "sellers-guide.html": ("Free Seller's Guide: Sell Your Home Step by Step",
   "Free 8-page Seller's Guide from J.R. Grimaldo in Landrum, SC: getting ready to list, showings, and the road from offer to closing. Emailed to you."),
 "fsbo-guide.html": ("Free FSBO Guide: Sell Your Home on Your Own – J.R. Grimaldo",
   "Selling your home yourself in South Carolina? A free 8-page guide from J.R. Grimaldo: pricing, showings, the disclosure form, and closing. Emailed to you."),
 "fsbo-guide-info.html": ("Free FSBO Guide: Sell Your Home on Your Own – J.R. Grimaldo",
   "Selling your home yourself in SC? A free 8-page guide: pricing, showings, the disclosure form, and closing. Emailed to you with the state disclosure form."),
 "sales-list.html": ("Recent Sales Near You, Free List – J.R. Grimaldo",
   "Get a free one-page list of similar homes that sold near you, with the real sold prices, from J.R. Grimaldo. No estimate, no pressure, no cost."),
 "buyers-guide.html": ("Free Buyer's Guide: Buy Your Home Step by Step",
   "A free 8-page guide to buying a home in the Upstate SC, from J.R. Grimaldo, Real Estate Professional. Emailed to you."),
 "privacy.html": ("Privacy – J.R. Grimaldo, Real Estate Professional",
   "What jrREsales.com collects, why, and how to unsubscribe. J.R. Grimaldo, Real Estate Professional, NorthGroup Real Estate, Landrum, SC."),
 "free-book-expired.html": ("Free Book for Owners Whose Home Didn't Sell – J.R. Grimaldo",
   "Free book \"Expired!?\" for owners whose home was listed and didn't sell: why it happens and what to change. Mailed to you by J.R. Grimaldo, Landrum, SC."),
 "free-book-sell-fast.html": ("Free Book: How to Sell Homes Fast for Top Dollar",
   "For homeowners thinking about selling: how to get your home ready, find buyers, and negotiate the best price. Free, mailed to you by J.R. Grimaldo."),
}
META_ES = {
 "index.html": ("Venda su casa en Landrum y el Upstate – J.R. Grimaldo",
   "¿Piensa vender en el Upstate? J.R. Grimaldo, Profesional de Bienes Raíces desde 2016, le prepara una valuación gratis por escrito en un día hábil. Hablo español."),
 "home-value.html": ("¿Cuánto vale mi casa? Valuación gratis – J.R. Grimaldo",
   "¿Cuánto vale su casa en el Upstate? J.R. Grimaldo le prepara una valuación gratis por escrito, con las ventas recientes cerca de usted, en un día hábil."),
 "listings.html": ("Mis propiedades – J.R. Grimaldo",
   "Casas en venta ahora con J.R. Grimaldo, Profesional de Bienes Raíces, en Landrum y el Upstate de Carolina del Sur. Hablo español."),
 "sold.html": ("Casas vendidas – J.R. Grimaldo",
   "{n} casas vendidas y compradas desde 2016 en Greer, Taylors, Inman, Landrum y todo el Upstate, con los precios reales. {r} familias volvieron a trabajar con J.R."),
 "about.html": ("Sobre J.R. Grimaldo – Bienes raíces en Landrum, SC",
   "Conozca a J.R. Grimaldo, Profesional de Bienes Raíces con licencia en Carolina del Sur desde 2016, en Landrum. Respuestas rápidas. Hablo español."),
 "reviews.html": ("Opiniones de clientes – J.R. Grimaldo",
   "Lo que dicen los clientes de vender y comprar casas con J.R. Grimaldo, Profesional de Bienes Raíces, en el Upstate de Carolina del Sur."),
 "free-books.html": ("Guías y libros gratis para vender su casa – J.R. Grimaldo",
   "Guías y libros gratis para vender su casa, de J.R. Grimaldo en Landrum, SC: una guía de 8 páginas en español por correo electrónico y dos libros impresos."),
 "newsletter.html": ("Boletín mensual, Front Porch Notes – J.R. Grimaldo",
   "El boletín mensual gratis de J.R. Grimaldo sobre las casas en Landrum y el Upstate de Carolina del Sur. Inscríbase por correo."),
 "contact.html": ("Contácteme – J.R. Grimaldo",
   "Envíe un texto a J.R. Grimaldo al 864-381-2326. Es la forma más rápida de comunicarse con él. Bienes raíces en Landrum y el Upstate."),
 "sellers-guide.html": ("Guía gratis para vendedores, paso a paso – J.R. Grimaldo",
   "Guía gratis de 8 páginas de J.R. Grimaldo en Landrum, SC: cómo preparar su casa, las visitas y el camino de la oferta al cierre. Se la envío por correo."),
 "privacy.html": ("Privacidad – J.R. Grimaldo",
   "Qué recoge jrREsales.com, para qué y cómo cancelar la suscripción. J.R. Grimaldo, Profesional de Bienes Raíces, NorthGroup Real Estate, Landrum, SC."),
 "free-book-expired.html": ("Libro gratis si su casa no se vendió – J.R. Grimaldo",
   "Libro gratis \"Expired!?\" (en inglés) para dueños cuya casa no se vendió: por qué pasa y qué cambiar. Se lo envía por correo J.R. Grimaldo, Landrum, SC."),
 "free-book-sell-fast.html": ("Libro gratis: How to Sell Homes Fast for Top Dollar",
   "Libro gratis (en inglés) para dueños que piensan vender: cómo preparar su casa, encontrar compradores y negociar. Se lo envía por correo J.R. Grimaldo."),
}

def _meta(M, name, title, desc, n, r):
    if name in M:
        t, d = M[name]
        return t, d.replace('{n}', str(n)).replace('{r}', str(r))
    return title, desc

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / "es").mkdir()
    for f in (SRC / "assets").iterdir(): shutil.copy(f, OUT / "assets" / f.name)
    (OUT / "assets" / "site.css").write_text(CSS)
    (OUT / "assets" / "site.js").write_text(JS)
    (OUT / "assets" / "favicon.svg").write_text(FAVICON)
    (OUT / "reply.html").write_text(REPLY_HTML.replace('assets/site.css"', 'assets/site.css?v=' + ASSET_V + '"'))
    # IONOS used to forward jrresales.com to /defaultsite. Browsers that saved
    # that forwarding land here; send them to /index.html (not /, which those
    # browsers would bounce back here).
    (OUT / "defaultsite").mkdir(exist_ok=True)
    (OUT / "defaultsite" / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/index.html"><link rel="canonical" href="https://jrresales.com/"><title>J.R. Grimaldo</title><a href="/index.html">Go to jrREsales.com</a><script>location.replace("/index.html")</script>')
    (OUT / "CNAME").write_text(SITE["domain"] + "\n")
    # Search engines: list of public pages, and where to find it.
    base = "https://" + SITE["domain"] + "/"
    urls = ["", "home-value.html", "listings.html", "sold.html", "about.html", "reviews.html", "free-books.html", "newsletter.html", "contact.html", "sellers-guide.html", "fsbo-guide-info.html", "sales-list.html",
            "es/", "es/home-value.html", "es/listings.html", "es/sold.html", "es/about.html", "es/reviews.html", "es/free-books.html", "es/newsletter.html", "es/contact.html", "es/sellers-guide.html", "privacy.html", "es/privacy.html"]
    urls += [n["path"] for n in NEWSLETTERS]
    urls += [b["slug"] + ".html" for b in BOOKS] + ["es/" + b["slug"] + ".html" for b in BOOKS] + [k + ".html" for k in TOWN_PAGES if k not in ("greenville", "simpsonville", "fountain-inn")]
    import datetime as _dt
    today = _dt.date.today().isoformat()
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{base}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /reply.html\nDisallow: /defaultsite/\nDisallow: /assets/*.pdf\nSitemap: " + base + "sitemap.xml\n")
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
        "newsletter.html": "J.R. Grimaldo's free monthly newsletter: what homes are selling for in Landrum and nearby Upstate SC towns, whether sales are up or down, and where mortgage rates stand. Sign up by email.",
        "free-books.html": "Free guides and books on selling your home from J.R. Grimaldo, REALTOR® in Landrum, SC: an 8-page Seller's Guide by email, and two printed books by mail. No cost, no obligation.",
        "contact.html": "Text J.R. Grimaldo at 864-381-2326. It's the fastest way to reach him. If you call and he doesn't pick up, leave a message. Landrum and Upstate SC Real Estate.",
        "buyers-guide.html": "A free 8-page guide to buying a home in the Upstate SC, from J.R. Grimaldo, REALTOR®. Emailed to you.",
        "sales-list.html": "Get a free one-page list of similar homes that sold near you, with the real sold prices, from J.R. Grimaldo, REALTOR®. No estimate, no pressure, no cost.",
        "fsbo-guide-info.html": "Selling your home yourself in South Carolina? A free 8-page guide from J.R. Grimaldo, REALTOR®: pricing, showings, the disclosure form, and closing. Emailed to you with the state disclosure form.",
        "fsbo-guide.html": "Selling your home yourself in South Carolina? A free 8-page guide from J.R. Grimaldo, REALTOR®: pricing, showings, the disclosure form, and closing. Emailed to you.",
        "sellers-guide.html": "Free 8-page Seller's Guide from J.R. Grimaldo, REALTOR® in Landrum, SC: getting ready to list, showings, and the road from offer to closing. Emailed to you.",
        "tax-sale-guide.html": "Bought at a Greenville or Spartanburg County tax sale, or thinking about it? A free 8-page guide from J.R. Grimaldo, REALTOR®: from your first bid to selling the property once it's yours. Emailed to you.",
        "privacy.html": "What jrREsales.com collects, why, and how to unsubscribe. J.R. Grimaldo, REALTOR®, NorthGroup Real Estate, Landrum, SC.",
    }
    DE = {
        "index.html": "¿Piensa vender en el Upstate? J.R. Grimaldo, REALTOR® desde 2016, le prepara una valuación gratis por escrito en un día hábil. Hablo español.",
        "home-value.html": "¿Cuánto vale su casa en el Upstate de Carolina del Sur? J.R. Grimaldo le prepara una valuación gratis por escrito, con las ventas recientes cerca de usted, en un día hábil.",
        "listings.html": "Casas en venta ahora con J.R. Grimaldo, REALTOR®, en el Upstate de Carolina del Sur. Hablo español.",
        "sold.html": f"{n_sales} casas vendidas y compradas desde 2016 en Greer, Taylors, Greenville, Simpsonville, Inman, Landrum y todo el Upstate de Carolina del Sur. {REPEAT_FAMILIES} familias han vuelto a trabajar con J.R.",
        "about.html": "Conozca a J.R. Grimaldo, REALTOR® de Carolina del Sur desde 2016, con base en Landrum. Calidad antes que cantidad y respuestas rápidas. Hablo español.",
        "reviews.html": "Lo que dicen los clientes de comprar y vender con J.R. Grimaldo, REALTOR®, en el Upstate de Carolina del Sur.",
        "newsletter.html": "El boletín mensual gratis de J.R. Grimaldo sobre las casas en Landrum y el Upstate de Carolina del Sur. Inscríbase por correo.",
        "free-books.html": "Guías y libros gratis sobre vender su casa de J.R. Grimaldo, REALTOR® en Landrum, SC: una guía de 8 páginas en español por correo electrónico, y dos libros impresos por correo. Sin costo ni compromiso.",
        "contact.html": "Envíe un texto a J.R. Grimaldo al 864-381-2326. Es la forma más rápida de comunicarse con él. Bienes raíces en Landrum y el Upstate.",
        "sellers-guide.html": "Guía gratis de 8 páginas de J.R. Grimaldo, REALTOR® en Landrum, SC: cómo preparar su casa, las visitas y el camino de la oferta al cierre. Se la envía por correo electrónico.",
        "tax-sale-guide.html": "¿Compró o piensa comprar en una subasta por impuestos de Greenville o Spartanburg? Guía gratis de 8 páginas de J.R. Grimaldo, REALTOR®: desde su primera oferta hasta vender la propiedad. Se la envía por correo. Hablo español.",
        "privacy.html": "Qué recoge jrREsales.com, para qué y cómo cancelar la suscripción. J.R. Grimaldo, REALTOR®, NorthGroup Real Estate, Landrum, SC.",
    }
    # English: (title, body, language switch, Spanish twin or None)
    pages = {
        "index.html": (t, page_home(EN), "es/index.html", "index.html"),
        "home-value.html": ("What's My Home Worth? Free Home Valuation – " + SITE["agent"], page_home_value(EN), "es/home-value.html", "home-value.html"),
        "listings.html": ("My Listings – " + SITE["agent"] + ", REALTOR®", page_list(EN, EN["li_h1"], LISTINGS, EN["li_empty"]), "es/listings.html", "listings.html"),
        "sold.html": ("Sold Homes – " + SITE["agent"] + ", REALTOR®", page_sold(EN), "es/sold.html", "sold.html"),
        "about.html": ("About J.R. Grimaldo, REALTOR® – Landrum, SC", page_about(EN), "es/about.html", "about.html"),
        "reviews.html": ("Client Reviews – " + SITE["agent"] + ", REALTOR®", page_reviews(EN), "es/reviews.html", "reviews.html"),
        "free-books.html": ("Free Guides & Books on Selling Your Home – " + SITE["agent"], page_books(EN), "es/free-books.html", "free-books.html"),
        "newsletter.html": ("Monthly Newsletter – " + SITE["agent"] + ", REALTOR®", page_newsletter(EN), "es/newsletter.html", "newsletter.html"),
        "contact.html": ("Contact J.R. Grimaldo, REALTOR®", page_contact(EN), "es/contact.html", "contact.html"),
        "sellers-guide.html": ("Free Seller's Guide: Selling Your Home, Step by Step – " + SITE["agent"], page_guide(EN), "es/sellers-guide.html", "sellers-guide.html"),
        "fsbo-guide.html": ("Free Guide: Selling Your Home on Your Own, Step by Step – " + SITE["agent"], page_fsbo_guide(), "es/index.html", None),
        "fsbo-guide-info.html": ("Free Guide: Selling Your Home on Your Own, Step by Step – " + SITE["agent"], page_fsbo_guide(info=True), "es/free-books.html", None),
        "sales-list.html": ("A List of Recent Sales Near You – " + SITE["agent"] + ", REALTOR®", page_sales_list(), "es/index.html", None),
        "buyers-guide.html": ("Free Buyer's Guide: Buying Your Home, Step by Step – " + SITE["agent"], page_buyers_guide(), "es/index.html", None),
        "privacy.html": ("Privacy – " + SITE["agent"] + ", REALTOR®", page_privacy(EN), "es/privacy.html", "privacy.html"),
        "tax-sale-guide.html": ("Free Tax Sale Guide: " + TAX_GUIDE["en"]["title"] + " – " + SITE["agent"], page_tax_guide(EN), "es/tax-sale-guide.html", "tax-sale-guide.html"),
    }
    for b in BOOKS:
        n = b["slug"] + ".html"
        pages[n] = ("Free Book: " + b["title"] + " – " + SITE["agent"], page_book(EN, b), "es/" + n, n)
        D[n] = b["line"] + " Free, mailed to you by J.R. Grimaldo, REALTOR® in Landrum, SC."
    if NEWSLETTERS:
        (OUT / "newsletter").mkdir(exist_ok=True)
        NLT = dict(EN, dir_prefix="newsletter/", nav=[("../" + h, l) for h, l in EN["nav"]])
        for n in NEWSLETTERS:
            fname = n["path"].split("/", 1)[1]
            (OUT / n["path"]).write_text(layout(NLT, fname, n["title"] + " – Front Porch Notes with J.R.",
                                                n["builder"](), "../es/newsletter.html", n["summary"]))
    for name, (title, body, sw, alt) in pages.items():
        title, desc = _meta(META_EN, name, title, D[name], n_sales, REPEAT_FAMILIES)
        (OUT / name).write_text(layout(EN, name, title, body, sw, desc, alt))
    for k in TOWN_PAGES:
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
        "free-books.html": ("Guías y libros gratis sobre vender su casa – " + SITE["agent"], page_books(ES), "../free-books.html"),
        "newsletter.html": ("Boletín mensual – " + SITE["agent"] + ", REALTOR®", page_newsletter(ES), "../newsletter.html"),
        "contact.html": ("Contácteme – " + SITE["agent"] + ", REALTOR®", page_contact(ES), "../contact.html"),
        "sellers-guide.html": ("Guía gratis para vendedores: Cómo vender su casa, paso a paso – " + SITE["agent"], page_guide(ES), "../sellers-guide.html"),
        "privacy.html": ("Privacidad – " + SITE["agent"] + ", REALTOR®", page_privacy(ES), "../privacy.html"),
        "tax-sale-guide.html": ("Guía gratis: " + TAX_GUIDE["es"]["title"] + " – " + SITE["agent"], page_tax_guide(ES), "../tax-sale-guide.html"),
    }
    for b in BOOKS:
        n = b["slug"] + ".html"
        es_pages[n] = ("Libro gratis: " + b["title"] + " – " + SITE["agent"], page_book(ES, b), "../" + n)
        DE[n] = b["line_es"] + " Gratis, enviado por correo por J.R. Grimaldo, REALTOR® en Landrum, SC."
    for name, (title, body, sw) in es_pages.items():
        title, desc = _meta(META_ES, name, title, DE[name], n_sales, REPEAT_FAMILIES)
        (OUT / "es" / name).write_text(layout(ES, name, title, body, sw, desc, name))
    print("built", len(pages) + len(es_pages) + len(TOWN_PAGES), "pages into", OUT)

if __name__ == "__main__":
    build()
