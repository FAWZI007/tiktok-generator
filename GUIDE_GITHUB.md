# 📤 Guide: Publier sur GitHub

## Méthode 1: Script automatique (Recommandé)

1. **Double-cliquez sur `upload_to_github.bat`**
2. Suivez les instructions à l'écran
3. C'est tout ! 🎉

---

## Méthode 2: Interface GitHub (Alternative)

### Étape 1: Créer le repository
1. Allez sur https://github.com/
2. Connectez-vous (ou créez un compte)
3. Cliquez "+" puis "New repository"
4. Nom: `tiktok-generator`
5. Description: `Générateur automatique de clips TikTok`
6. Public ✅
7. NE PAS cocher "Add README file"
8. Cliquez "Create repository"

### Étape 2: Uploader les fichiers
1. Sur la page du repository, cliquez "uploading an existing file"
2. Glissez-déposez TOUS les fichiers de votre dossier `tiktok/`
3. Ou cliquez "choose your files" et sélectionnez tout
4. Message de commit: "Initial commit - TikTok Generator"
5. Cliquez "Commit changes"

---

## Méthode 3: Ligne de commande (Pour experts)

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/tiktok-generator.git
git push -u origin main
```

---

## 📁 Fichiers à uploader

Assurez-vous d'inclure TOUS ces fichiers:

### Fichiers principaux:
- ✅ `app.py` (application web)
- ✅ `tiktok_clip.py` (script original)
- ✅ `templates/index.html` (interface)

### Fichiers de déploiement:
- ✅ `Procfile`
- ✅ `requirements.txt`
- ✅ `runtime.txt`
- ✅ `railway.json`

### Documentation:
- ✅ `README.md`
- ✅ `.gitignore`

### Scripts utiles:
- ✅ `start_app.bat`
- ✅ `prepare_deploy.bat`
- ✅ Autres fichiers .bat

---

## ✅ Vérification

Une fois uploadé, votre repository devrait contenir:
- Environ 15-20 fichiers
- Dossier `templates/`
- Tous les fichiers .py, .txt, .md, .bat

---

## 🚀 Prochaine étape

Une fois sur GitHub:
1. Allez sur https://railway.app/
2. "Start a New Project"
3. "Deploy from GitHub repo"
4. Sélectionnez `tiktok-generator`
5. Déploiement automatique ! 🎉

URL finale: `https://tiktok-generator.up.railway.app`
