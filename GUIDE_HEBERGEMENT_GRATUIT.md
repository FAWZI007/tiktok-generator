# 🚀 GUIDE: Hébergement permanent GRATUIT

## Option 1: Railway (Recommandé - Plus simple)

### Étapes détaillées:

#### 1. Créer un compte GitHub
- Allez sur https://github.com/
- Créez un compte gratuit
- Créez un nouveau repository "tiktok-generator"

#### 2. Uploader votre code sur GitHub
- Uploadez tous les fichiers de votre dossier tiktok/
- Ou utilisez Git:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/tiktok-generator.git
git push -u origin main
```

#### 3. Déployer sur Railway
- Allez sur https://railway.app/
- Cliquez "Start a New Project"
- Connectez votre GitHub
- Sélectionnez votre repository "tiktok-generator"
- Railway déploie automatiquement !

#### 4. Récupérer votre URL
- Dans Railway, allez dans Settings > Networking
- Cliquez "Generate Domain"
- Vous obtenez une URL permanente !

### ✅ Résultat:
- URL permanente (ex: tiktok-generator.up.railway.app)
- 500h gratuites par mois
- Redémarrage automatique
- HTTPS inclus

---

## Option 2: Render (Alternative gratuite)

### Étapes:

#### 1. GitHub (même étape qu'au-dessus)

#### 2. Déployer sur Render
- Allez sur https://render.com/
- Créez un compte gratuit
- Cliquez "New +" > "Web Service"
- Connectez votre GitHub
- Sélectionnez votre repository
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### ✅ Résultat:
- URL permanente (ex: tiktok-generator.onrender.com)
- 750h gratuites par mois
- Sleep après 15min d'inactivité

---

## 🎯 Je recommande Railway car:
- Plus simple à configurer
- Pas de "sleep"
- Interface plus claire
- Deploy automatique

## 📱 Une fois déployé:
Votre app sera accessible 24/7 depuis n'importe où !

URL exemple: https://tiktok-generator.up.railway.app
