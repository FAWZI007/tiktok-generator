@echo off
echo 🚀 Déploiement TikTok Generator sur Railway
echo.

REM Vérifier si Railway CLI est installé
where railway >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Railway CLI non installé
    echo 💡 Installation:
    echo    npm install -g @railway/cli
    echo    Ou téléchargez depuis: https://railway.app/cli
    pause
    exit /b 1
)

echo ✅ Railway CLI détecté
echo.

echo 🔐 Connexion à Railway...
railway login

echo.
echo 📁 Initialisation du projet...
railway init

echo.
echo 🚀 Déploiement en cours...
railway up

echo.
echo 🎉 Déploiement terminé!
echo 📱 Votre app sera accessible sur une URL publique Railway
echo 🔗 Utilisez 'railway status' pour voir l'URL
pause
