#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration du Control Plane
"""

import sys
import asyncio
import os
from pathlib import Path

# Ajouter le dossier du projet au PYTHONPATH

project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))
os.chdir(project_dir)

print("🧪 Test du Homebox Control Plane")
print("=" * 50)
print(f"📁 Dossier de travail: {project_dir}")

# Test 1: Import des modules

print("\n1️⃣ Test des imports...")
try:
    from src.config import Config
    from src.notifiers.telegram import TelegramNotifier
    from src.checkers.homebox import HomeboxChecker
    from src.checkers.neron import NeronChecker
    from src.database.history import HistoryManager
    print("   ✅ Tous les modules importés avec succès")
except Exception as e:
    print(f"   ❌ Erreur d’import: {e}")
    print(f"   Python path: {sys.path}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Configuration

print("\n2️⃣ Test de la configuration...")
try:
    config = Config()
    print(f"   ✅ Configuration chargée")
    print(f"   - Homebox URL: {config.homebox_url}")
    print(f"   - Neron URL: {config.neron_url}")
    print(f"   - Check interval: {config.check_interval}s")

    if not config.telegram_bot_token or config.telegram_bot_token.startswith("your_"):
        print("   ⚠️  TELEGRAM_BOT_TOKEN non configuré dans .env")

    if not config.telegram_chat_id or config.telegram_chat_id.startswith("your_"):
        print("   ⚠️  TELEGRAM_CHAT_ID non configuré dans .env")

except Exception as e:
    print(f"   ❌ Erreur de configuration: {e}")
    sys.exit(1)

# Test 3: Connexion Telegram

print("\n3️⃣ Test de connexion Telegram...")

async def test_telegram():
    try:
        config = Config()
        notifier = TelegramNotifier(config.telegram_bot_token, config.telegram_chat_id)

        if await notifier.test_connection():
            print("   ✅ Connexion Telegram OK")

            # Envoyer un message de test
            if await notifier.send_info("🧪 <b>Test de connexion</b>\n\nLe Control Plane est correctement configuré!"):
                print("   ✅ Message de test envoyé avec succès")
            else:
                print("   ⚠️  Échec de l'envoi du message de test")
        else:
            print("   ❌ Échec de la connexion Telegram")
            print("   Vérifiez votre TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID dans .env")

    except ValueError as e:
        print(f"   ⚠️  Configuration Telegram incomplète: {e}")
    except Exception as e:
        print(f"   ❌ Erreur Telegram: {e}")

try:
    asyncio.run(test_telegram())
except Exception as e:
    print(f"   ❌ Erreur lors du test Telegram: {e}")

# Test 4: Base de données

print("\n4️⃣ Test de la base de données...")
try:
    config = Config()
    history = HistoryManager(config.database_path)

    # Ajouter un check de test
    history.add_check(
        service_name="Test",
        is_healthy=True,
        response_time=0.5,
        status_code=200
    )

    # Récupérer les checks
    checks = history.get_recent_checks(limit=1)

    if checks:
        print("   ✅ Base de données fonctionnelle")
        print(f"   - Chemin: {config.database_path}")

    history.close()

except Exception as e:
    print(f"   ❌ Erreur base de données: {e}")

# Test 5: Checkers

print("\n5️⃣ Test des checkers...")

async def test_checkers():
    try:
        config = Config()

        # Test Homebox
        print("   Testing Homebox...")
        homebox = HomeboxChecker(config.homebox_url, timeout=5)
        result = await homebox.check()
        status = "✅" if result.is_healthy else "❌"
        print(f"   {status} Homebox: {result.service_name} - {'UP' if result.is_healthy else 'DOWN'} ({result.response_time:.2f}s)")

        # Test Neron
        print("   Testing Neron...")
        neron = NeronChecker(config.neron_url, timeout=5)
        result = await neron.check()
        status = "✅" if result.is_healthy else "❌"
        print(f"   {status} Neron: {result.service_name} - {'UP' if result.is_healthy else 'DOWN'} ({result.response_time:.2f}s)")

    except Exception as e:
        print(f"   ❌ Erreur lors des tests de checker: {e}")

try:
    asyncio.run(test_checkers())
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "=" * 50)
print("✅ Tests terminés!")
print("\nSi tous les tests sont OK, vous pouvez lancer:")
print("  python app.py")
print()
