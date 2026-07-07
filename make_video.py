#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_video.py - Genere une video verticale 9:16 pour TikTok depuis un texte SEO."""
import os, glob, json, random, textwrap, datetime, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(HERE, "posts.json")
BG_DIR = os.path.join(HERE, "assets", "bg")
MUSIC = os.path.join(HERE, "assets", "music.mp3")
OUT_DIR = os.path.join(HERE, "out")
FRAME = os.path.join(OUT_DIR, "frame.png")
VIDEO = os.path.join(OUT_DIR, "tiktok.mp4")
CAPTION = os.path.join(OUT_DIR, "caption.txt")
W, H = 1080, 1920
DURATION = 12
LANGUAGES = ["fr", "en", "es", "it", "de"]
BRAND = "Taxi Marne-la-Vallee"
SITE = "www.taximarnelavallee.com"
PHONE = "Reservation 24h/24"
HASHTAGS = ("#taxi #disneylandparis #marnelavallee #valdeurope #cdg #orly "
            "#taxiparis #navetteaeroport #chessy #bussysaintgeorges")

def load_font(size, bold=True):
    for c in [("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
               else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")]:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            pass
    return ImageFont.load_default()

def pick_post():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    now = datetime.datetime.now()
    counter = now.timetuple().tm_yday * 3 + (0 if now.hour < 11 else (1 if now.hour < 16 else 2))
    lang = LANGUAGES[counter % len(LANGUAGES)]
    variants = data["posts"][lang]
    return lang, variants[(counter // len(LANGUAGES)) % len(variants)]["summary"]

def make_background():
    imgs = glob.glob(os.path.join(BG_DIR, "*.jpg")) + glob.glob(os.path.join(BG_DIR, "*.png"))
    if imgs:
        bg = Image.open(random.choice(imgs)).convert("RGB")
        s = max(W / bg.width, H / bg.height)
        bg = bg.resize((int(bg.width * s), int(bg.height * s)))
        l, t = (bg.width - W) // 2, (bg.height - H) // 2
        bg = bg.crop((l, t, l + W, t + H)).filter(ImageFilter.GaussianBlur(4))
    else:
        bg = Image.new("RGB", (W, H), (12, 18, 38))
        d = ImageDraw.Draw(bg)
        for y in range(H):
            t = y / H
            d.line([(0, y), (W, y)], fill=(int(18*(1-t)+6*t), int(30*(1-t)+8*t), int(66*(1-t)+18*t)))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle([0, 0, W, H], fill=(0, 0, 0, 110))
    return Image.alpha_composite(bg.convert("RGBA"), ov).convert("RGB")

def _wrap(font, text, max_w=W - 160):
    avg = font.getbbox("nx")[2] / 2 or 30
    return textwrap.wrap(text, width=max(8, int(max_w / avg)))

def draw_centered(draw, text, font, y, fill=(255, 255, 255), gap=22):
    for line in _wrap(font, text):
        b = draw.textbbox((0, 0), line, font=font)
        x = (W - (b[2] - b[0])) // 2
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=fill)
        y += (b[3] - b[1]) + gap
    return y

def draw_headline(draw, text, y_top, y_bottom):
    for size in (78, 72, 66, 60, 54, 48):
        font = load_font(size)
        lines = _wrap(font, text)
        line_h = font.getbbox("Ag")[3] + 24
        if line_h * len(lines) <= (y_bottom - y_top):
            y = y_top + ((y_bottom - y_top) - line_h * len(lines)) // 2
            for line in lines:
                b = draw.textbbox((0, 0), line, font=font)
                x = (W - (b[2] - b[0])) // 2
                draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))
                draw.text((x, y), line, font=font, fill=(255, 255, 255))
                y += line_h
            return
    draw_centered(draw, text[:120], load_font(48), y_top)

def build_frame(lang, summary):
    os.makedirs(OUT_DIR, exist_ok=True)
    img = make_background()
    draw = ImageDraw.Draw(img)
    draw_centered(draw, BRAND.upper(), load_font(58), 200, fill=(255, 210, 60))
    clean = "".join(ch for ch in summary if ord(ch) < 0x2190).replace(SITE, "").strip(" .")
    headline = clean.split(". ")[0].strip()
    if len(headline) < 25 and ". " in clean:
        headline = ". ".join(clean.split(". ")[:2]).strip()
    headline = headline[:140].rstrip(" ,.") + " !"
    draw_headline(draw, headline, 520, H - 380)
    draw_centered(draw, PHONE, load_font(40), H - 300, fill=(255, 210, 60))
    draw_centered(draw, SITE, load_font(46), H - 230)
    img.save(FRAME)

def build_video():
    vf = f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.10)':d={DURATION*25}:s=1080x1920:fps=25"
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", FRAME]
    if os.path.exists(MUSIC):
        cmd += ["-i", MUSIC, "-shortest"]
    cmd += ["-t", str(DURATION), "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25"]
    if os.path.exists(MUSIC):
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    cmd += [VIDEO]
    subprocess.run(cmd, check=True)

def write_caption(summary):
    clean = "".join(ch for ch in summary if ord(ch) < 0x2190).replace(SITE, "").strip(" .")
    with open(CAPTION, "w", encoding="utf-8") as f:
        f.write(f"{clean}\n{SITE}\n\n{HASHTAGS}"[:2100])

def main():
    lang, summary = pick_post()
    print(f"[OK] Langue={lang} | {summary[:60]}...")
    build_frame(lang, summary)
    build_video()
    write_caption(summary)
    print(f"[SUCCES] Video generee : {VIDEO}")

if __name__ == "__main__":
    main()
