#!/bin/bash
# Script pour lancer le Homebox Control Plane

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🏠 Homebox Control Plane"
echo "========================"

# Se placer dans le dossier du script
cd "$(dirname "$0")"

# Vérifier si venv existe
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Environnement virtuel non trouvé${NC}"
    echo "Lancez d'abord: bash install.sh"
    exit 1
fi

# Activer l'environnement virtuel
echo -e "${GREEN}✓${NC} Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier si .env existe
if [ ! -f "/opt/Homebox_AI/.env" ]; then
    echo -e "${RED}❌ Fichier .env non trouvé${NC}"
    echo "Créez le fichier .env à partir de .env.example"
    exit 1
fi

# Définir PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Lancer l'application
echo -e "${GREEN}✓${NC} Lancement de l'application..."
echo ""

if [ "$1" == "test" ]; then
    python3 test.py
elif [ "$1" == "check" ]; then
    python3 app.py check
elif [ "$1" == "report" ]; then
    python3 app.py report
else
    python3 app.py
fi
