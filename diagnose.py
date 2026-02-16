#!/usr/bin/env python3
"""
Script de diagnostic rapide pour identifier les problèmes
"""

import sys
import os
from pathlib import Path

print("🔍 Diagnostic du Homebox Control Plane")
print("=" * 60)

# 1. Informations système
print("\n📊 Informations système:")
print(f"   Python version: {sys.version}")
print(f"   Python executable: {sys.executable}")
print(f"   Dossier actuel: {os.getcwd()}")

# 2. Structure des dossiers
print("\n📁 Structure du projet:")
project_dir = Path(__file__).parent.absolute()
print(f"   Racine du projet: {project_dir}")

print("\n   Contenu de la racine:")
for item in sorted(project_dir.iterdir()):
    if item.name.startswith('.') and item.name not in ['.env', '.env.example', '.gitignore']:
        continue
    symbol = "📁" if item.is_dir() else "📄"
    print(f"   {symbol} {item.name}")

# 3. Vérifier le dossier src
src_dir = project_dir / "src"
print(f"\n   Contenu de src/:")
if src_dir.exists():
    for item in sorted(src_dir.iterdir()):
        if item.name.startswith('__pycache__'):
            continue
        symbol = "📁" if item.is_dir() else "📄"
        print(f"   {symbol} {item.name}")
        
        # Si c'est un dossier, montrer son contenu
        if item.is_dir() and item.name != '__pycache__':
            print(f"      Contenu de {item.name}/:")
            for subitem in sorted(item.iterdir()):
                if subitem.name.startswith('__pycache__'):
                    continue
                subsymbol = "📁" if subitem.is_dir() else "📄"
                print(f"      {subsymbol} {subitem.name}")
else:
    print("   ❌ Le dossier src/ n'existe pas!")

# 4. Vérifier les fichiers critiques
print("\n🔎 Vérification des fichiers critiques:")
critical_files = {
    "src/__init__.py": "Module src",
    "src/config.py": "Configuration",
    "src/checkers/__init__.py": "Module checkers",
    "src/checkers/homebox.py": "Checker Homebox",
    "src/checkers/neron.py": "Checker Neron",
    "src/notifiers/__init__.py": "Module notifiers",
    "src/notifiers/telegram.py": "Notifier Telegram",
    "src/database/__init__.py": "Module database",
    "src/database/history.py": "Gestionnaire historique",
    "requirements.txt": "Dépendances",
    "app.py": "Application principale",
    ".env.example": "Template configuration"
}

all_good = True
for file_path, description in critical_files.items():
    full_path = project_dir / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"   ✅ {description:25} ({file_path}) - {size} bytes")
    else:
        print(f"   ❌ {description:25} ({file_path}) - MANQUANT")
        all_good = False

# 5. Vérifier le virtualenv
print("\n🐍 Environnement virtuel:")
venv_dir = project_dir / "venv"
if venv_dir.exists():
    print(f"   ✅ Virtualenv trouvé: {venv_dir}")
    
    # Vérifier si on est dans le virtualenv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"   ✅ Virtualenv activé")
    else:
        print(f"   ⚠️  Virtualenv NON activé")
        print(f"      Activez-le avec: source venv/bin/activate")
else:
    print(f"   ❌ Virtualenv non trouvé")
    print(f"      Créez-le avec: python3 -m venv venv")

# 6. Vérifier les dépendances
print("\n📦 Dépendances Python:")
required_packages = ['aiohttp', 'python-dotenv', 'pyyaml']
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NON INSTALLÉ")
        all_good = False

# 7. Test d'import
print("\n🧪 Test d'import des modules:")
sys.path.insert(0, str(project_dir))

try:
    import src
    print(f"   ✅ import src")
except ImportError as e:
    print(f"   ❌ import src - {e}")
    all_good = False

try:
    from src import config
    print(f"   ✅ from src import config")
except ImportError as e:
    print(f"   ❌ from src import config - {e}")
    all_good = False

try:
    from src.config import Config
    print(f"   ✅ from src.config import Config")
except ImportError as e:
    print(f"   ❌ from src.config import Config - {e}")
    all_good = False

# 8. Configuration
print("\n⚙️  Configuration:")
env_file = project_dir / ".env"
if env_file.exists():
    print(f"   ✅ Fichier .env trouvé")
    
    # Vérifier les variables importantes (sans afficher les valeurs)
    with open(env_file, 'r') as f:
        content = f.read()
        if 'TELEGRAM_BOT_TOKEN' in content:
            print(f"   ✅ TELEGRAM_BOT_TOKEN défini")
        else:
            print(f"   ⚠️  TELEGRAM_BOT_TOKEN non défini")
        
        if 'TELEGRAM_CHAT_ID' in content:
            print(f"   ✅ TELEGRAM_CHAT_ID défini")
        else:
            print(f"   ⚠️  TELEGRAM_CHAT_ID non défini")
else:
    print(f"   ⚠️  Fichier .env non trouvé")
    print(f"      Créez-le avec: cp .env.example .env")

# Résumé
print("\n" + "=" * 60)
if all_good:
    print("✅ Diagnostic réussi - Le projet semble correctement configuré")
    print("\nProchaines étapes:")
    print("   1. Activer le virtualenv: source venv/bin/activate")
    print("   2. Lancer le test: python3 test.py")
    print("   3. Lancer l'app: python3 app.py")
else:
    print("❌ Problèmes détectés - Voir les messages ci-dessus")
    print("\nActions suggérées:")
    print("   1. Assurez-vous d'avoir extrait TOUS les fichiers du ZIP")
    print("   2. Installez les dépendances: pip install -r requirements.txt")
    print("   3. Créez le fichier .env: cp .env.example .env")
    print("   4. Réessayez ce diagnostic: python3 diagnose.py")

print()
