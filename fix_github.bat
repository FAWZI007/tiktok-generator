@echo off
echo 🔧 Réparation du repository GitHub
echo.

echo 📋 Vérification de l'état Git...
git status

echo.
echo 📤 Push vers master...
git push origin master

echo.
echo 📤 Push vers main (au cas où)...
git push origin master:main

echo.
echo 🔍 Vérification sur GitHub...
echo.
echo ✅ Votre repository devrait maintenant être visible sur:
echo    👉 https://github.com/FAWZI007/tiktok-generator
echo.
echo 🚀 Prochaine étape: Déploiement
echo.
echo 📋 PLATEFORMES D'HÉBERGEMENT GRATUIT:
echo.
echo 1️⃣ RENDER (Recommandé - Plus stable):
echo    👉 https://render.com/
echo    ✅ 750h gratuites/mois
echo    ✅ Plus fiable que Railway
echo    ✅ Interface simple
echo.
echo 2️⃣ RAILWAY (Alternative):
echo    👉 https://railway.app/
echo    ✅ 500h gratuites/mois
echo.
echo 3️⃣ VERCEL (Pour projets légers):
echo    👉 https://vercel.com/
echo.
echo 💡 Instructions pour Render:
echo    1. Créez un compte sur render.com
echo    2. "New +" → "Web Service"
echo    3. "Connect GitHub" → Sélectionnez "tiktok-generator"
echo    4. Build Command: pip install -r requirements.txt
echo    5. Start Command: gunicorn app:app
echo    6. Cliquez "Create Web Service"
echo.

pause
