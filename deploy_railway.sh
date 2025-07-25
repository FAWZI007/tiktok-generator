#!/bin/bash

echo "🚀 Déploiement TikTok Generator sur Railway"
echo ""

# Vérifier si Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI non installé"
    echo "💡 Installation:"
    echo "   npm install -g @railway/cli"
    echo "   Ou téléchargez depuis: https://railway.app/cli"
    exit 1
fi

echo "✅ Railway CLI détecté"
echo ""

# Login si nécessaire
echo "🔐 Connexion à Railway..."
railway login

echo ""
echo "📁 Initialisation du projet..."
railway init

echo ""
echo "🚀 Déploiement en cours..."
railway up

echo ""
echo "🎉 Déploiement terminé!"
echo "📱 Votre app sera accessible sur une URL publique Railway"
echo "🔗 Utilisez 'railway status' pour voir l'URL"
