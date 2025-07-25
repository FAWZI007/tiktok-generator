@echo off
echo 🚀 Publication automatique sur GitHub
echo.

REM Vérifier si Git est installé
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git n'est pas installé
    echo.
    echo 💡 Pour installer Git:
    echo    1. Allez sur https://git-scm.com/download/win
    echo    2. Téléchargez et installez Git pour Windows
    echo    3. Redémarrez cette commande
    echo.
    pause
    exit /b 1
)

echo ✅ Git détecté
echo.

echo 📝 Configuration Git (si première fois)
set /p username="Votre nom d'utilisateur GitHub: "
set /p email="Votre email GitHub: "

git config --global user.name "%username%"
git config --global user.email "%email%"

echo.
echo 📁 Initialisation du repository Git...
git init

echo.
echo 📋 Ajout de tous les fichiers...
git add .

echo.
echo 💾 Premier commit...
git commit -m "Initial commit - TikTok Generator"

echo.
echo 🌐 Instructions pour connecter à GitHub:
echo.
echo 1️⃣ Allez sur https://github.com/
echo 2️⃣ Cliquez sur "+" puis "New repository"
echo 3️⃣ Nom du repository: tiktok-generator
echo 4️⃣ Laissez "Public" coché
echo 5️⃣ NE PAS cocher "Add README file"
echo 6️⃣ Cliquez "Create repository"
echo.
echo 7️⃣ Copiez l'URL du repository (ex: https://github.com/%username%/tiktok-generator.git)
echo.

set /p repo_url="Collez l'URL de votre repository GitHub: "

echo.
echo 🔗 Connexion au repository GitHub...
git branch -M main
git remote add origin %repo_url%

echo.
echo 📤 Upload vers GitHub...
git push -u origin main

echo.
echo 🎉 Projet publié sur GitHub avec succès !
echo.
echo 🔗 Votre repository: %repo_url%
echo.
echo ✅ Prochaine étape: Déployer sur Railway
echo    👉 https://railway.app/
echo    👉 Connect GitHub et sélectionnez votre repository
echo.

pause
