import requests
import random
import os
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────
PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]
PAGE_ID    = os.environ["FB_PAGE_ID"]
SITE_URL   = "https://www.taximarnelavallee.com"
PHONE      = "01 XX XX XX XX"  # ← Remplacez par votre vrai numéro

# ─── Messages SEO variés ───────────────────────────────────────────────────────
POSTS = [
    f"""🚖 Taxi Marne-la-Vallée — Disponible 24h/24 !
Besoin d'un taxi fiable à Marne-la-Vallée, Chessy, Val d'Europe ou Disneyland Paris ?
📞 Réservez maintenant : {PHONE}
🌐 {SITE_URL}
#TaxiMarneLaVallée #TaxiDisneyland #ValDEurope #Chessy #TaxiParis""",

    f"""✈️ Navette Aéroport depuis Marne-la-Vallée
CDG, Orly, Beauvais — On vous dépose à l'heure, à chaque fois !
💼 Prise en charge de vos bagages
⏰ Ponctualité garantie
📞 {PHONE} | 🌐 {SITE_URL}
#NavetteAéroport #TaxiCDG #TaxiOrly #TaxiMarneLaVallée""",

    f"""🎡 Taxi pour Disneyland Paris
Vous visitez Disneyland Paris ? Profitez d'un trajet confortable et sans stress !
🏰 Départ depuis toute l'Île-de-France
👨‍👩‍👧 Véhicules familiaux disponibles
📞 Réservez : {PHONE}
🌐 {SITE_URL}
#DisneylandParis #TaxiDisney #TaxiMarneLaVallée""",

    f"""🏥 Transport médical & VSL — Marne-la-Vallée
Rendez-vous médical, dialyse, kiné... Nous assurons votre transport avec respect et ponctualité.
🩺 Conventionné Sécurité Sociale
📞 {PHONE} | 🌐 {SITE_URL}
#TransportMédical #VSL #TaxiSanté #MarneLaVallée""",

    f"""🌙 Taxi de nuit — Marne-la-Vallée
Retour de soirée, train tardif, aéroport de nuit... Nous sommes là 24h/24 et 7j/7 !
🔒 Trajet sécurisé
💳 Paiement CB accepté
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiNuit #TaxiMarneLaVallée #TaxiGareDisney""",

    f"""🚉 Taxi Gare de Chessy / Val d'Europe
Prise en charge directe à la gare de Chessy ou Val d'Europe.
🚅 TGV, RER A — On s'adapte à votre horaire !
📞 {PHONE}
🌐 {SITE_URL}
#TaxiChessy #TaxiValDEurope #RERA #TGVMarneLaVallée""",

    f"""⭐ Votre taxi de confiance à Marne-la-Vallée !
Des milliers de clients satisfaits depuis des années.
✅ Véhicules propres & climatisés
✅ Chauffeurs professionnels
✅ Tarifs transparents
📞 {PHONE} | 🌐 {SITE_URL}
#TaxiMarneLaVallée #TaxiProfessionnel #AvisClients""",

    f"""📍 Zones desservies — Taxi Marne-la-Vallée
Chessy • Val d'Europe • Noisy-le-Grand • Bussy-Saint-Georges • Lagny-sur-Marne • Torcy • Lognes • et toute l'Île-de-France !
📞 {PHONE}
🌐 {SITE_URL}
#TaxiMarneLaVallée #TaxiSeineetMarne #TaxiBussySaintGeorges""",
]

# ─── Sélection du post du jour ─────────────────────────────────────────────────
hour = datetime.utcnow().hour
day  = datetime.utcnow().weekday()
# Rotation basée sur heure + jour pour varier les messages
index = (hour + day * 3) % len(POSTS)
message = POSTS[index]

# ─── Publication Facebook ──────────────────────────────────────────────────────
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
payload = {
    "message": message,
    "link":    SITE_URL,
    "access_token": PAGE_TOKEN,
}

response = requests.post(url, data=payload)
result   = response.json()

if "id" in result:
    print(f"✅ Post publié avec succès ! ID: {result['id']}")
    print(f"📝 Message : {message[:80]}...")
else:
    print(f"❌ Erreur : {result}")
    exit(1)
