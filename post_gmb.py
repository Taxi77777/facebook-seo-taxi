#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post_gmb.py
Publie automatiquement un post SEO sur la fiche Google Business Profile
(Google My Business) de Taxi Marne-la-Vallee / Taxi a Disneyland.

- Recupere le compte GMB
- Recupere la fiche locale (location)
- Publie un post SEO en rotation FR / EN / ES / IT / DE
- Ajoute un bouton d'action (LEARN_MORE par defaut, CALL possible)

Variables d'environnement requises :
  GOOGLE_REFRESH_TOKEN
  GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET

Optionnelles :
  GMB_ACCOUNT_NAME   ex: "accounts/1234567890"  (sinon: 1er compte)
  GMB_LOCATION_NAME  ex: "locations/1234567890" (sinon: 1ere fiche)
  GMB_CTA_TYPE       LEARN_MORE (defaut) ou CALL
"""

import os
import sys
import json
import datetime
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TOKEN_URL = "https://oauth2.googleapis.com/token"
ACCOUNTS_URL = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
LOCATIONS_URL = (
    "https://mybusinessbusinessinformation.googleapis.com/v1/{parent}/locations"
)
LOCALPOSTS_URL = "https://mybusiness.googleapis.com/v4/{parent}/localPosts"

LANGUAGES = ["fr", "en", "es", "it", "de"]

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(HERE, "posts.json")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def get_access_token():
    """Echange le refresh token contre un access token."""
    refresh_token = os.environ["GOOGLE_REFRESH_TOKEN"]
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]

    resp = requests.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print("[OK] Access token obtenu.")
    return token


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


# ---------------------------------------------------------------------------
# Compte + fiche
# ---------------------------------------------------------------------------
def get_account(token):
    """Retourne le nom du compte GMB (ex: 'accounts/123')."""
    override = os.environ.get("GMB_ACCOUNT_NAME")
    if override:
        print(f"[OK] Compte force via env : {override}")
        return override

    resp = requests.get(ACCOUNTS_URL, headers=auth_headers(token), timeout=30)
    resp.raise_for_status()
    accounts = resp.json().get("accounts", [])
    if not accounts:
        sys.exit("[ERREUR] Aucun compte Google Business Profile trouve.")
    name = accounts[0]["name"]
    print(f"[OK] Compte : {name} ({accounts[0].get('accountName', '')})")
    return name


def get_location(token, account_name):
    """Retourne le nom de la fiche (ex: 'locations/456')."""
    override = os.environ.get("GMB_LOCATION_NAME")
    if override:
        print(f"[OK] Fiche forcee via env : {override}")
        return override

    url = LOCATIONS_URL.format(parent=account_name)
    params = {"readMask": "name,title,storefrontAddress", "pageSize": 100}
    resp = requests.get(url, headers=auth_headers(token), params=params, timeout=30)
    resp.raise_for_status()
    locations = resp.json().get("locations", [])
    if not locations:
        sys.exit("[ERREUR] Aucune fiche locale trouvee pour ce compte.")
    loc = locations[0]
    print(f"[OK] Fiche : {loc['name']} ({loc.get('title', '')})")
    return loc["name"]


# ---------------------------------------------------------------------------
# Selection du post (rotation par numero de semaine)
# ---------------------------------------------------------------------------
def pick_post():
    """Selectionne un post en rotation.

    3 posts par jour : un creneau matin / midi / soir.
    La langue change a chaque creneau (FR/EN/ES/IT/DE), et la variante
    tourne au fil des jours -> aucun doublon dans la meme journee.
    """
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.datetime.now()
    day_of_year = now.timetuple().tm_yday  # 1..366

    # Creneau du jour selon l'heure : 0 = matin, 1 = midi, 2 = soir
    if now.hour < 11:
        slot = 0
    elif now.hour < 16:
        slot = 1
    else:
        slot = 2

    # Compteur global unique : 3 creneaux par jour
    counter = day_of_year * 3 + slot

    lang = LANGUAGES[counter % len(LANGUAGES)]
    variants = data["posts"][lang]
    variant = variants[(counter // len(LANGUAGES)) % len(variants)]

    cta_type = os.environ.get("GMB_CTA_TYPE", data.get("cta_type", "LEARN_MORE"))
    cta_url = data.get("cta_url", "https://www.taximarnelavallee.com")

    print(f"[OK] Jour {day_of_year}, creneau {slot} -> langue={lang}, CTA={cta_type}")
    return variant, cta_type, cta_url


# ---------------------------------------------------------------------------
# Publication
# ---------------------------------------------------------------------------
def build_local_post(variant, cta_type, cta_url):
    call_to_action = {"actionType": cta_type}
    # Pour LEARN_MORE il faut une URL. Pour CALL, Google utilise le numero
    # de la fiche : pas d'URL a fournir.
    if cta_type != "CALL":
        call_to_action["url"] = cta_url

    return {
        "languageCode": variant["languageCode"],
        "summary": variant["summary"],
        "callToAction": call_to_action,
        "topicType": "STANDARD",
    }


def publish(token, account_name, location_name, body):
    # v4 attend un parent "accounts/*/locations/*"
    loc_id = location_name.split("/")[-1]
    parent = f"{account_name}/locations/{loc_id}"
    url = LOCALPOSTS_URL.format(parent=parent)

    resp = requests.post(url, headers=auth_headers(token), json=body, timeout=30)
    if resp.status_code >= 400:
        print(f"[ERREUR] {resp.status_code} : {resp.text}", file=sys.stderr)
        resp.raise_for_status()
    result = resp.json()
    print(f"[SUCCES] Post publie : {result.get('name', '(sans nom)')}")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"=== post_gmb.py  {datetime.datetime.now().isoformat(timespec='seconds')} ===")
    token = get_access_token()
    account_name = get_account(token)
    location_name = get_location(token, account_name)
    variant, cta_type, cta_url = pick_post()
    body = build_local_post(variant, cta_type, cta_url)
    print("[INFO] Corps du post :")
    print(json.dumps(body, ensure_ascii=False, indent=2))
    publish(token, account_name, location_name, body)


if __name__ == "__main__":
    main()
