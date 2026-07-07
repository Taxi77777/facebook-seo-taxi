# 🚖 Facebook SEO Auto-Post — Taxi Marne-la-Vallée

Automatisation GitHub Actions qui publie **3 fois par jour** sur votre page Facebook pour booster le SEO de [www.taximarnelavallee.com](https://www.taximarnelavallee.com).

## ✅ Ce que ça fait
- Publie automatiquement à **7h, 12h et 18h** (heure de Paris)
- **8 messages SEO variés** (aéroport, Disneyland, médical, nuit, gares...)
- Chaque post contient le lien vers votre site = **boost SEO Google**
- **100% gratuit** avec GitHub Actions

## 🔧 Configuration requise

### Étape 1 — Ajouter vos secrets GitHub
Dans votre repo GitHub → **Settings → Secrets → Actions** → New secret :

| Nom du secret | Valeur |
|---|---|
| `FB_PAGE_TOKEN` | Votre Page Access Token Facebook |
| `FB_PAGE_ID` | L'ID de votre page Facebook |

### Étape 2 — Obtenir votre Facebook Page Token
1. Allez sur [developers.facebook.com](https://developers.facebook.com)
2. Créez une app → **Business**
3. Ajoutez **Pages API**
4. Générez votre **Page Access Token**

## 📁 Structure
```
.github/
  workflows/
    facebook-posts.yml   ← Le workflow automatique
post_facebook.py         ← Le script de publication
```
