# 📤 GUIDE: Créer le repository GitHub manuellement

## Méthode Simple (Recommandée)

### Étape 1: Créer le repository
1. **Allez sur** https://github.com/
2. **Connectez-vous** avec votre compte
3. **Cliquez** le bouton "+" (en haut à droite) → "New repository"
4. **Nom**: `tiktok-generator`
5. **Description**: `Générateur automatique de clips TikTok`
6. **Public** ✅ (coché)
7. **Important**: NE PAS cocher "Add a README file"
8. **Cliquez** "Create repository"

### Étape 2: Upload des fichiers
1. Sur la page du nouveau repository, cliquez **"uploading an existing file"**
2. **Glissez-déposez** ou sélectionnez ces fichiers:

**Fichiers OBLIGATOIRES pour le déploiement:**
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `templates/index.html`

**Fichiers OPTIONNELS:**
- ✅ `tiktok_clip.py`
- ✅ `README.md`
- ✅ `.gitignore`
- ✅ `railway.json`

3. **Message de commit**: "Initial commit - TikTok Generator"
4. **Cliquez** "Commit changes"

### Étape 3: Vérifier
Votre repository devrait maintenant contenir tous les fichiers !

---

## Alternative: Script automatique

Si vous préférez utiliser Git en ligne de commande:
- **Double-cliquez** sur `create_new_github.bat`
- Suivez les instructions

---

## Prochaine étape: Déploiement

Une fois le repository créé et visible:
1. **Render.com** (recommandé) - Plus stable
2. **Railway.app** (alternative)
3. **Vercel.com** (pour projets légers)

**URL final**: Votre app sera accessible 24/7 !
