import requests
import os
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────
PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]
PAGE_ID    = os.environ["FB_PAGE_ID"]
SITE_URL   = "https://www.taximarnelavallee.com"
PHONE      = "06 XX XX XX XX"

# ─── Hashtags locaux communs ─────────────────────────────────────────────────
LOCAL_TAGS = """#TaxiMarneLaVallée #Chessy #ValDEurope #BussySaintGeorges
#NoisyLeGrand #Torcy #Lognes #LagnySurMarne #SeineetMarne #77
#IleDeFrance #DisneylandParis #TaxiDisneyland #TaxiCDG #TaxiOrly
#VTC77 #TaxiParis #ChaufferPrivé #TaxiPro #TaxiConventionné"""

# ─── Posts multilingues SEO ────────────────────────────────────────────────────
POSTS = [

    # ════════════════════════════════════════════
    # 🇫🇷 FRANÇAIS
    # ════════════════════════════════════════════
    f"""🚖 Taxi Marne-la-Vallée — Disponible 24h/24 !
Besoin d'un taxi fiable ? Aéroport, Disneyland, gares, médical...
📞 {PHONE} | 🌐 {SITE_URL}

{LOCAL_TAGS}""",

    f"""✈️ Navette Aéroport CDG & Orly depuis Marne-la-Vallée
Ponctualité garantie — Prise en charge bagages incluse ✅
📞 {PHONE} | 🌐 {SITE_URL}

#NavetteAéroport #TaxiCDG #TaxiOrly #TaxiMarneLaVallée #TaxiParis
#Chessy #ValDEurope #BussySaintGeorges #NoisyLeGrand #SeineetMarne #77
#IleDeFrance #TransportAéroport #VTC77 #TaxiPro""",

    f"""🏰 Taxi pour Disneyland Paris !
Départ depuis toute l'Île-de-France — Véhicules familiaux disponibles 👨‍👩‍👧
📞 {PHONE} | 🌐 {SITE_URL}

#DisneylandParis #TaxiDisney #TaxiMarneLaVallée #Chessy #ValDEurope
#BussySaintGeorges #NoisyLeGrand #Torcy #Lognes #LagnySurMarne
#SeineetMarne #77 #IleDeFrance #VTC77 #TaxiParis #ChaufferPrivé""",

    f"""🌙 Taxi de nuit Marne-la-Vallée — 24h/24, 7j/7
Retour de soirée, train tardif, aéroport de nuit ? On est là !
💳 CB acceptée | 📞 {PHONE} | 🌐 {SITE_URL}

#TaxiNuit #TaxiMarneLaVallée #TaxiGareDisney #VTC77 #TaxiParis
#Chessy #ValDEurope #GareChessy #RERA #TGVMarneLaVallée
#SeineetMarne #77 #IleDeFrance #TaxiPro #TaxiDisneyland""",

    f"""🏥 Transport médical & VSL — Marne-la-Vallée
Dialyse, kiné, hôpital... Conventionné Sécurité Sociale 🩺
📞 {PHONE} | 🌐 {SITE_URL}

#TransportMédical #VSL #TaxiSanté #MarneLaVallée #TaxiConventionné
#Chessy #ValDEurope #BussySaintGeorges #NoisyLeGrand #Torcy
#SeineetMarne #77 #IleDeFrance #TaxiConventionnéSS #TaxiPro""",

    # ════════════════════════════════════════════
    # 🇬🇧 ENGLISH
    # ════════════════════════════════════════════
    f"""🚖 Taxi to Disneyland Paris — Book Now!
Reliable, comfortable taxi service from/to Disneyland Paris & CDG Airport 🏰✈️
📞 {PHONE} | 🌐 {SITE_URL}

#DisneylandParisTaxi #ParisAirportTransfer #CDGAirport #DisneylandTransfer
#TaxiParis #ParisTransport #Chessy #ValDEurope #MarneLaVallee
#BussySaintGeorges #NoisyLeGrand #SeineEtMarne #IleDeFrance #VTC77""",

    f"""✈️ Airport Transfer Paris — CDG & Orly
Professional taxi service available 24/7. Fixed prices, no surprises!
🧳 Luggage assistance included
📞 {PHONE} | 🌐 {SITE_URL}

#ParisAirportTaxi #CDGTransfer #OrlyAirport #ParisTaxi #AirportShuttle
#FranceTaxi #Chessy #ValDEurope #DisneylandParis #MarneLaVallee
#SeineEtMarne #77 #IleDeFrance #VTC77 #TaxiPro""",

    f"""🏰 Visiting Disneyland Paris? We drive you there!
Family-friendly taxis, child seats available 👨‍👩‍👧‍👦
Book online: {SITE_URL}
📞 {PHONE}

#DisneylandParis #DisneyTransfer #ParisTaxi #FamilyTaxi #DisneylandShuttle
#VisitParis #Chessy #ValDEurope #MarneLaVallee #BussySaintGeorges
#SeineEtMarne #77 #IleDeFrance #VTC77 #ParisWithKids""",

    f"""⭐ Your trusted taxi near Marne-la-Vallée
Val d'Europe • Chessy • Noisy-le-Grand • Bussy • Torcy • Lognes
💳 Card payment accepted | 24/7 service
📞 {PHONE} | 🌐 {SITE_URL}

#MarneLaVallee #ValDEurope #ParisTaxi #TaxiService #FranceTaxi
#DisneylandParis #Chessy #BussySaintGeorges #NoisyLeGrand #Torcy
#Lognes #LagnySurMarne #SeineEtMarne #77 #VTC77""",

    # ════════════════════════════════════════════
    # 🇪🇸 ESPAÑOL
    # ════════════════════════════════════════════
    f"""🚖 Taxi a Disneyland París — ¡Reserva ahora!
Servicio de taxi profesional desde/hasta Disneyland París y el aeropuerto CDG ✈️🏰
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiDisneylandParis #TransferParís #TaxiCDG #DisneyShutle #TaxiParís #ViajeParís""",

    f"""✈️ Traslado al Aeropuerto CDG y Orly — Marne-la-Vallée
Servicio puntual disponible 24h/7 días. ¡Precios fijos sin sorpresas!
🧳 Ayuda con equipaje incluida
📞 {PHONE} | 🌐 {SITE_URL}
#TransferAeropuerto #TaxiParís #CDGAeropuerto #TaxiCDG #FranciaViaje #DisneyShutle""",

    f"""🏰 ¿Visitando Disneyland París? ¡Te llevamos!
Taxis familiares con sillas para niños disponibles 👨‍👩‍👧‍👦
Reserva en: {SITE_URL}
📞 {PHONE}
#DisneylandParís #TaxiDisney #ViajeParís #FamiliaViaje #TaxiFrancia #DisneyShutle""",

    # ════════════════════════════════════════════
    # 🇮🇹 ITALIANO
    # ════════════════════════════════════════════
    f"""🚖 Taxi per Disneyland Parigi — Prenota Ora!
Servizio taxi professionale da/per Disneyland Parigi e l'aeroporto CDG ✈️🏰
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiDisneylandParigi #TransferParigi #TaxiCDG #DisneyTaxi #TaxiParigi #ViaggioParigi""",

    f"""✈️ Transfer Aeroporto CDG e Orly — Marne-la-Vallée
Servizio puntuale disponibile 24h/7 giorni. Prezzi fissi senza sorprese!
🧳 Assistenza bagagli inclusa
📞 {PHONE} | 🌐 {SITE_URL}
#TransferAeroporto #TaxiParigi #CDGAeroporto #TaxiFrancia #ViaggioParigi #DisneyShuttle""",

    f"""🏰 Visitate Disneyland Parigi? Vi accompagniamo!
Taxi familiari con seggiolini per bambini disponibili 👨‍👩‍👧‍👦
Prenota su: {SITE_URL}
📞 {PHONE}
#DisneylandParigi #TaxiDisney #ViaggioParigi #FamigliaViaggio #TaxiFrancia #DisneyShuttle""",

    # ════════════════════════════════════════════
    # 🇩🇪 DEUTSCH
    # ════════════════════════════════════════════
    f"""🚖 Taxi nach Disneyland Paris — Jetzt buchen!
Professioneller Taxiservice von/nach Disneyland Paris und Flughafen CDG ✈️🏰
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiDisneylandParis #TransferParis #TaxiCDG #DisneyTransfer #TaxiParis #ParisReise""",

    f"""✈️ Flughafentransfer CDG & Orly — Marne-la-Vallée
Pünktlicher Service 24h/7 Tage. Festpreise ohne Überraschungen!
🧳 Gepäckservice inklusive
📞 {PHONE} | 🌐 {SITE_URL}
#Flughafentransfer #TaxiParis #CDGFlughafen #TaxiFrankreich #ParisReise #DisneyShuttle""",

    f"""🏰 Besuch in Disneyland Paris? Wir fahren Sie hin!
Familientaxis mit Kindersitzen verfügbar 👨‍👩‍👧‍👦
Online buchen: {SITE_URL}
📞 {PHONE}
#DisneylandParis #TaxiDisney #ParisReise #Familienreise #TaxiFrankreich #DisneyShuttle""",

    # ════════════════════════════════════════════
    # 💡 BONUS SEO — Posts spéciaux haute valeur
    # ════════════════════════════════════════════
    f"""🎯 Taxi Marne-la-Vallée — Zones desservies :
📍 Chessy • Val d'Europe • Bussy-Saint-Georges
📍 Noisy-le-Grand • Torcy • Lognes • Lagny
📍 CDG • Orly • Disneyland • Paris Centre
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiMarneLaVallée #TaxiSeineetMarne #TaxiBussy #TaxiChessy #TaxiValDEurope""",

    f"""💎 Pourquoi choisir notre taxi ?
✅ Véhicules récents & climatisés
✅ Chauffeurs professionnels & discrets
✅ Paiement CB / espèces / virement
✅ Devis gratuit sur demande
✅ Disponible 24h/24 — 365 jours/an
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiMarneLaVallée #TaxiPro #DisneylandParis #TaxiParis #ValDEurope""",
]

# ─── Rotation intelligente ────────────────────────────────────────────────────
hour  = datetime.utcnow().hour
day   = datetime.utcnow().timetuple().tm_yday
index = (hour * 7 + day * 3) % len(POSTS)
message = POSTS[index]

# ─── Publication Facebook ──────────────────────────────────────────────────────
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
payload = {
    "message":      message,
    "link":         SITE_URL,
    "access_token": PAGE_TOKEN,
}
response = requests.post(url, data=payload)
result   = response.json()

if "id" in result:
    print(f"✅ Post Facebook publié ! ID: {result['id']}")
    print(f"🌍 Langue du post: {message[:30]}...")
else:
    print(f"❌ Erreur : {result}")
    exit(1)
