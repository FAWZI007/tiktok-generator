@echo off
echo 🚀 Création d'un nouveau repository GitHub
echo.

echo 📋 ÉTAPES À SUIVRE:
echo.

echo 1️⃣ Créer le repository sur GitHub:
echo    👉 Allez sur https://github.com/
echo    👉 Connectez-vous avec votre compte
echo    👉 Cliquez le bouton "+" en haut à droite
echo    👉 Choisissez "New repository"
echo.

echo 2️⃣ Configuration du repository:
echo    📝 Repository name: tiktok-generator
echo    📝 Description: Générateur automatique de clips TikTok
echo    ✅ Public (coché)
echo    ❌ NE PAS cocher "Add a README file"
echo    ❌ NE PAS ajouter .gitignore ou license
echo    👉 Cliquez "Create repository"
echo.

echo 3️⃣ Copier l'URL du nouveau repository:
echo    📋 Copiez l'URL qui apparaît (ex: https://github.com/FAWZI007/tiktok-generator.git)
echo.

echo 4️⃣ Revenir ici et appuyer sur une touche...
echo.

pause

echo.
echo 🔗 Configuration de la nouvelle URL...
set /p new_url="Collez l'URL de votre nouveau repository: "

echo.
echo 📤 Suppression de l'ancien remote...
git remote remove origin

echo.
echo 🔗 Ajout du nouveau remote...
git remote add origin %new_url%

echo.
echo 📋 Vérification...
git remote -v

echo.
echo 📤 Push vers le nouveau repository...
git push -u origin master

echo.
echo 🎉 Terminé ! Votre code devrait maintenant être visible sur GitHub !
echo 👉 Vérifiez sur: %new_url%
echo.

pause
