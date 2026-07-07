import requests
import random
import os
import time
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────
PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]
SITE_URL   = "https://www.taximarnelavallee.com"
PHONE      = "06 XX XX XX XX"  # ← Remplacez par votre vrai numéro

# ─── Images publiques hébergées sur Unsplash (taxi/ville/route) ───────────────
IMAGES = [
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1080&q=80",
    "https://images.unsplash.com/photo-1504215680853-026ed2a45def?w=1080&q=80",
    "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1080&q=80",
    "https://images.unsplash.com/photo-1580674684081-7617fbf3d745?w=1080&q=80",
]

# ─── Légendes SEO variées ─────────────────────────────────────────────────────
CAPTIONS = [
    f"""🚖 Taxi Disneyland Paris — Réservez maintenant !
Votre chauffeur privé pour Disneyland, Val d'Europe et toute la région !
🏰 Trajet confortable & ponctuel
📞 Appelez-nous : {PHONE}
🌐 {SITE_URL}

#TaxiDisneyland #DisneylandParis #ValDEurope #TaxiMarneLaVallée #Chessy #TaxiParis #VTCParis #ChaufeurPrivé #TaxiPro""",

    f"""✈️ Navette Aéroport CDG & Orly
Depuis Marne-la-Vallée, on vous emmène à l'aéroport à l'heure !
⏰ Disponible 24h/24 — 7j/7
💼 Prise en charge bagages incluse
📞 {PHONE} | 🌐 {SITE_URL}

#NavetteAéroport #TaxiCDG #TaxiOrly #TaxiMarneLaVallée #AéroportParis #Transfer #VTC77""",

    f"""🌟 Votre Taxi de confiance à Marne-la-Vallée !
Des milliers de clients satisfaits ⭐⭐⭐⭐⭐
✅ Véhicules climatisés et propres
✅ Tarifs fixes et transparents
✅ Chauffeurs professionnels
📞 {PHONE} | 🌐 {SITE_URL}

#TaxiMarneLaVallée #TaxiPro #ChaufeurPrivé #Disneyland #ValDEurope #Chessy #Torcy #Lognes""",

    f"""🎡 Visite Disneyland Paris ?
On s'occupe de votre transport !
🏰 Départ depuis toute l'Île-de-France
👨‍👩‍👧 Véhicules familiaux disponibles
💳 Paiement CB accepté
📞 {PHONE}
🌐 {SITE_URL}

#DisneylandParis #TaxiDisney #FamilyTrip #MarneLaVallée #TaxiIleDeFrance #WeekendDisney""",
]

# ─── Sélection du post ─────────────────────────────────────────────────────────
hour    = datetime.utcnow().hour
day     = datetime.utcnow().weekday()
index   = (hour + day * 3) % len(CAPTIONS)
caption = CAPTIONS[index]
image   = IMAGES[index % len(IMAGES)]

print(f"📸 Image: {image}")
print(f"📝 Caption: {caption[:60]}...")

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

# ─── Attente (Instagram recommande 30s) ───────────────────────────────────────
print("⏳ Attente 15 secondes...")
time.sleep(15)

# ─── Étape 2 : Publier le container ───────────────────────────────────────────
print("📤 Publication sur Instagram...")
publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
publish_payload = {
    "creation_id":  container_id,
    "access_token": PAGE_TOKEN,
}
pub_response = requests.post(publish_url, data=publish_payload)
pub_result   = pub_response.json()

if "id" in pub_result:
    print(f"✅ Post Instagram publié avec succès ! ID: {pub_result['id']}")
else:
    print(f"❌ Erreur publication : {pub_result}")
    exit(1)
