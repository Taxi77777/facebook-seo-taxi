#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post_tiktok.py
Publie la video out/tiktok.mp4 sur le compte TikTok @centraletaximlv
via la Content Posting API (Direct Post, FILE_UPLOAD).

Variables d'environnement requises :
  TIKTOK_CLIENT_KEY
  TIKTOK_CLIENT_SECRET
  TIKTOK_REFRESH_TOKEN

Optionnelles :
  TIKTOK_PRIVACY   SELF_ONLY (defaut) | PUBLIC_TO_EVERYONE | MUTUAL_FOLLOW_FRIENDS
                   -> PUBLIC necessite que ton app soit AUDITEE par TikTok.

Doc : https://developers.tiktok.com/doc/content-posting-api-get-started
"""

import os
import sys
import json
import time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(HERE, "out", "tiktok.mp4")
CAPTION = os.path.join(HERE, "out", "caption.txt")

TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
CREATOR_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
INIT_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"


def get_access_token():
    resp = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key": os.environ["TIKTOK_CLIENT_KEY"],
            "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
            "grant_type": "refresh_token",
            "refresh_token": os.environ["TIKTOK_REFRESH_TOKEN"],
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "access_token" not in data:
        sys.exit(f"[ERREUR] Pas d'access_token : {data}")
    print("[OK] Access token TikTok obtenu.")
    return data["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8"}


def query_creator(token):
    """Recupere les infos createur (niveaux de confidentialite autorises)."""
    resp = requests.post(CREATOR_URL, headers=auth(token), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    print("[OK] Creator info :", json.dumps(data.get("data", {}), ensure_ascii=False)[:300])
    return data.get("data", {})


def read_caption():
    if os.path.exists(CAPTION):
        with open(CAPTION, "r", encoding="utf-8") as f:
            return f.read().strip()[:2100]
    return "Taxi Marne-la-Vallee - Disneyland Paris & aeroports 24/7"


def init_upload(token, video_size, privacy):
    body = {
        "post_info": {
            "title": read_caption(),
            "privacy_level": privacy,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,       # un seul chunk (video courte < 64 Mo)
            "total_chunk_count": 1,
        },
    }
    resp = requests.post(INIT_URL, headers=auth(token), json=body, timeout=30)
    if resp.status_code >= 400:
        sys.exit(f"[ERREUR] init {resp.status_code} : {resp.text}")
    data = resp.json()["data"]
    print(f"[OK] publish_id = {data['publish_id']}")
    return data["publish_id"], data["upload_url"]


def upload_video(upload_url, video_size):
    with open(VIDEO, "rb") as f:
        content = f.read()
    headers = {
        "Content-Type": "video/mp4",
        "Content-Length": str(video_size),
        "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
    }
    resp = requests.put(upload_url, headers=headers, data=content, timeout=120)
    if resp.status_code not in (200, 201, 206):
        sys.exit(f"[ERREUR] upload {resp.status_code} : {resp.text}")
    print("[OK] Video envoyee a TikTok.")


def poll_status(token, publish_id, tries=12, delay=5):
    for i in range(tries):
        time.sleep(delay)
        resp = requests.post(STATUS_URL, headers=auth(token),
                             json={"publish_id": publish_id}, timeout=30)
        resp.raise_for_status()
        data = resp.json().get("data", {})
        status = data.get("status")
        print(f"[{i+1}/{tries}] status = {status}")
        if status in ("PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"):
            print("[SUCCES] Publication TikTok terminee.")
            return True
        if status == "FAILED":
            sys.exit(f"[ERREUR] Publication echouee : {data}")
    print("[INFO] Statut non finalise dans le temps imparti (peut se terminer plus tard).")
    return False


def main():
    if not os.path.exists(VIDEO):
        sys.exit("[ERREUR] out/tiktok.mp4 introuvable. Lance make_video.py d'abord.")
    video_size = os.path.getsize(VIDEO)
    privacy = os.environ.get("TIKTOK_PRIVACY", "SELF_ONLY")
    print(f"=== post_tiktok.py | taille={video_size} o | privacy={privacy} ===")

    token = get_access_token()
    query_creator(token)
    publish_id, upload_url = init_upload(token, video_size, privacy)
    upload_video(upload_url, video_size)
    poll_status(token, publish_id)


if __name__ == "__main__":
    main()
