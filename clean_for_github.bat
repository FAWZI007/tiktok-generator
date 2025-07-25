@echo off
echo 🧹 Nettoyage avant upload GitHub
echo.

echo 📁 Suppression des fichiers temporaires...

REM Supprimer les vidéos et clips (trop volumineux pour GitHub)
if exist "*.mp4" (
    echo Suppression des fichiers vidéo volumineux...
    del /q *.mp4
)

if exist "clips\*.mp4" (
    echo Suppression du dossier clips...
    rmdir /s /q clips
)

if exist "videos\*.mp4" (
    echo Suppression du dossier videos...
    rmdir /s /q videos
)

REM Supprimer ngrok s'il existe
if exist "ngrok.exe" (
    echo Suppression de ngrok.exe...
    del /q ngrok.exe
)

REM Supprimer les fichiers Python temporaires
if exist "__pycache__" (
    echo Suppression de __pycache__...
    rmdir /s /q __pycache__
)

if exist "*.pyc" (
    del /q *.pyc
)

echo.
echo ✅ Nettoyage terminé !
echo.
echo 📁 Fichiers restants (prêts pour GitHub):
dir /b

echo.
echo 🚀 Prêt pour l'upload GitHub !
echo    Double-cliquez maintenant sur: upload_to_github.bat
echo.

pause
