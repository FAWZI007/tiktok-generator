@echo off
echo 📦 Création d'un ZIP pour upload GitHub
echo.

echo 📁 Création du dossier temporaire...
if exist "github_upload" rmdir /s /q "github_upload"
mkdir "github_upload"

echo.
echo 📋 Copie des fichiers essentiels...

copy "app.py" "github_upload\" 2>nul
copy "tiktok_clip.py" "github_upload\" 2>nul
copy "requirements.txt" "github_upload\" 2>nul
copy "Procfile" "github_upload\" 2>nul
copy "runtime.txt" "github_upload\" 2>nul
copy "railway.json" "github_upload\" 2>nul
copy "README.md" "github_upload\" 2>nul
copy ".gitignore" "github_upload\" 2>nul

echo.
echo 📁 Copie du dossier templates...
if exist "templates" (
    mkdir "github_upload\templates" 2>nul
    copy "templates\*" "github_upload\templates\" 2>nul
)

echo.
echo ✅ Fichiers préparés dans le dossier 'github_upload'
echo.
echo 📋 Contenu:
dir /b "github_upload"

echo.
echo 🚀 INSTRUCTIONS:
echo.
echo 1️⃣ Allez sur https://github.com/ et créez un nouveau repository "tiktok-generator"
echo.
echo 2️⃣ Sur la page du repository, cliquez "uploading an existing file"
echo.
echo 3️⃣ Sélectionnez TOUS les fichiers du dossier 'github_upload'
echo    👉 Ou glissez-déposez le dossier entier
echo.
echo 4️⃣ Commit message: "Initial commit - TikTok Generator"
echo.
echo 5️⃣ Cliquez "Commit changes"
echo.
echo 🎉 Votre code sera visible sur GitHub !
echo.

pause
