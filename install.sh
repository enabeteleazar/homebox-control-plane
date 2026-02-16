#!/bin/bash
# Script d'installation du Homebox Control Plane

set -e  # Arrêter en cas d'erreur

echo "========================================="
echo "   Homebox Control Plane - Installation"
echo "========================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "Installez Python 3.8+ et réessayez"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION détecté"

# Créer l'environnement virtuel
echo ""
echo "📦 Création de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "⚠️  Environnement virtuel déjà existant"
fi

# Activer l'environnement virtuel
echo ""
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo ""
echo "📥 Installation des dépendances..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

echo "✅ Dépendances installées"

# Créer les dossiers nécessaires
echo ""
echo "📁 Création des dossiers..."
mkdir -p data logs
echo "✅ Dossiers créés"

# Copier le fichier .env si nécessaire
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "✅ Fichier .env créé"
    echo ""
    echo "⚠️  IMPORTANT: Éditez le fichier .env et configurez:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_CHAT_ID"
    echo "   - Les URLs de vos services"
else
    echo "⚠️  Fichier .env déjà existant (non modifié)"
fi

# Rendre app.py exécutable
chmod +x app.py

echo ""
echo "========================================="
echo "✅ Installation terminée!"
echo "========================================="
echo ""
echo "Prochaines étapes:"
echo ""
echo "1. Configurer le fichier .env:"
echo "   nano .env"
echo ""
echo "2. Tester la configuration:"
echo "   python app.py check"
echo ""
echo "3. Lancer le monitoring:"
echo "   python app.py"
echo ""
echo "Pour plus d'informations, consultez le README.md"
echo ""
