@echo off
echo 🌐 Exposition de TikTok Generator avec ngrok
echo.

REM Vérifier si ngrok est présent
if not exist "ngrok.exe" (
    echo ❌ ngrok.exe non trouvé dans ce dossier
    echo.
    echo 💡 Pour installer ngrok:
    echo    1. Allez sur https://ngrok.com/
    echo    2. Créez un compte gratuit
    echo    3. Téléchargez ngrok pour Windows
    echo    4. Copiez ngrok.exe dans ce dossier
    echo.
    pause
    exit /b 1
)

echo ✅ ngrok trouvé
echo.

echo 🚀 Lancement de l'application Flask...
start "Flask App" python app.py

echo ⏳ Attente du démarrage de Flask (5 secondes)...
timeout /t 5 /nobreak >nul

echo 🌐 Exposition publique avec ngrok...
echo.
echo 📱 Votre application sera accessible via une URL publique !
echo 🔗 Copiez l'URL https://xxxxx.ngrok.io qui s'affichera
echo.

ngrok http 5000
