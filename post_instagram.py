import requests
import os
import time
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────
PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]
SITE_URL   = "https://www.taximarnelavallee.com"
PHONE      = "06 XX XX XX XX"

# ─── Images publiques (taxi, route, Paris, Disneyland) ────────────────────────
IMAGES = [
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1080&q=80",
    "https://images.unsplash.com/photo-1504215680853-026ed2a45def?w=1080&q=80",
    "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1080&q=80",
    "https://images.unsplash.com/photo-1580674684081-7617fbf3d745?w=1080&q=80",
    "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=1080&q=80",
    "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1080&q=80",
]

# ─── Légendes multilingues SEO ─────────────────────────────────────────────────
CAPTIONS = [

    # 🇫🇷 FRANÇAIS
    f"""🚖 Taxi Disneyland Paris — Disponible 24h/24 !
Votre chauffeur privé pour Disneyland, Val d'Europe, CDG & Orly 🏰✈️
📞 {PHONE} | 🌐 {SITE_URL}

#TaxiDisneyland #DisneylandParis #ValDEurope #TaxiMarneLaVallée
#Chessy #TaxiParis #ChaufferPrivé #VTC77 #TaxiCDG #TaxiOrly""",

    # 🇬🇧 ENGLISH
    f"""🏰 Taxi to Disneyland Paris — Book your ride!
Professional driver for Disneyland, CDG Airport & Val d'Europe 🚖✈️
Available 24/7 — Fixed prices — Card accepted
📞 {PHONE} | 🌐 {SITE_URL}

#DisneylandParis #DisneylandTaxi #ParisTaxi #CDGAirport
#AirportTransfer #ParisTransport #DisneyTransfer #VisitParis
#FranceTaxi #DisneylandShuttle""",

    # 🇪🇸 ESPAÑOL
    f"""🏰 ¡Taxi a Disneyland París — Reserva tu viaje!
Conductor profesional para Disneyland, Aeropuerto CDG y Val d'Europe 🚖✈️
Disponible 24/7 — Precios fijos — Tarjeta aceptada
📞 {PHONE} | 🌐 {SITE_URL}

#DisneylandParís #TaxiDisney #TaxiParís #AeropuertoCDG
#TransferParís #ViajeParís #TaxiFrancia #DisneyShuttle
#TaxiCDG #FamiliaViaje""",

    # 🇮🇹 ITALIANO
    f"""🏰 Taxi per Disneyland Parigi — Prenota il tuo viaggio!
Autista professionale per Disneyland, Aeroporto CDG e Val d'Europe 🚖✈️
Disponibile 24/7 — Prezzi fissi — Carta accettata
📞 {PHONE} | 🌐 {SITE_URL}

#DisneylandParigi #TaxiDisney #TaxiParigi #AeroportoCDG
#TransferParigi #ViaggioParigi #TaxiFrancia #DisneyShuttle
#TaxiCDG #ViaggioFamiglia""",

    # 🇩🇪 DEUTSCH
    f"""🏰 Taxi nach Disneyland Paris — Jetzt buchen!
Professioneller Fahrer für Disneyland, Flughafen CDG & Val d'Europe 🚖✈️
24/7 verfügbar — Festpreise — Kartenzahlung akzeptiert
📞 {PHONE} | 🌐 {SITE_URL}

#DisneylandParis #TaxiDisney #TaxiParis #CDGFlughafen
#TransferParis #ParisReise #TaxiFrankreich #DisneyShuttle
#TaxiCDG #Familienreise""",

    # 💡 BONUS — Post zone géographique (FR + EN)
    f"""📍 Taxi Marne-la-Vallée — We speak your language!
🇫🇷 Français • 🇬🇧 English • 🇪🇸 Español • 🇮🇹 Italiano • 🇩🇪 Deutsch

Chessy | Val d'Europe | Bussy | Noisy | CDG | Orly | Disneyland
📞 {PHONE} | 🌐 {SITE_URL}

#TaxiMarneLaVallée #DisneylandParis #ParisTaxi #TaxiCDG
#MultilingualTaxi #TaxiInternational #ValDEurope #TaxiDisney""",
]

# ─── Sélection intelligente ────────────────────────────────────────────────────
hour    = datetime.utcnow().hour
day     = datetime.utcnow().timetuple().tm_yday
index   = (hour * 7 + day * 3) % len(CAPTIONS)
caption = CAPTIONS[index]
image   = IMAGES[index % len(IMAGES)]

print(f"🌍 Caption langue: {caption[:50]}...")
print(f"📸 Image: {image}")

# ─── Étape 1 : Créer le container Instagram ────────────────────────────────────
print("\n⏳ Création du container Instagram...")
create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
create_payload = {
    "image_url":    image,
    "caption":      caption,
    "access_token": PAGE_TOKEN,
}
response = requests.post(create_url, data=create_payload)
result   = response.json()

if "id" not in result:
    print(f"❌ Erreur création container : {result}")
    exit(1)

container_id = result["id"]
print(f"✅ Container créé : {container_id}")

# ─── Attente recommandée par Instagram ────────────────────────────────────────
print("⏳ Attente 15 secondes...")
time.sleep(15)

# ─── Étape 2 : Publier le container ───────────────────────────────────────────
print("📤 Publication sur Instagram...")
publish_url     = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
publish_payload = {
    "creation_id":  container_id,
    "access_token": PAGE_TOKEN,
}
pub_response = requests.post(publish_url, data=publish_payload)
pub_result   = pub_response.json()

if "id" in pub_result:
    print(f"✅ Post Instagram publié ! ID: {pub_result['id']}")
else:
    print(f"❌ Erreur publication : {pub_result}")
    exit(1)
