# 🚀 Guide de démarrage rapide

## Installation en 5 minutes

### 1. Prérequis
- Python 3.8+ installé
- Un bot Telegram (voir ci-dessous)

### 2. Créer un bot Telegram

1. Ouvrir Telegram → Chercher `@BotFather`
2. Envoyer `/newbot`
3. Suivre les instructions
4. Copier le **token** (format: `123456:ABCdef...`)
5. Envoyer un message à votre bot
6. Visiter: `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates`
7. Copier le `chat.id` dans le résultat JSON

### 3. Installation

```bash
# Cloner le repo
git clone https://github.com/enabeteleazar/homebox-control-plane.git
cd homebox-control-plane

# Lancer l'installation automatique
bash install.sh

# Ou manuellement:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p data logs
cp .env.example .env
```

### 4. Configuration

Éditer le fichier `.env`:

```bash
nano .env
```

Remplir au minimum:
```env
TELEGRAM_BOT_TOKEN=votre_token_ici
TELEGRAM_CHAT_ID=votre_chat_id_ici
HOMEBOX_URL=http://votre-homebox:7745
NERON_URL=http://votre-neron:3000
```

### 5. Test

```bash
# Tester la configuration
python test.py

# Faire une vérification unique
python app.py check
```

### 6. Lancement

```bash
# Monitoring continu
python app.py

# En arrière-plan avec screen
screen -S control-plane
python app.py
# Ctrl+A puis D pour détacher
```

## 📱 Notifications reçues

Vous recevrez des messages comme:

```
🔴 ALERTE - Service DOWN

Service: Homebox
Status: Indisponible
Code HTTP: 502
Erreur: Bad Gateway
Heure: 2026-02-15 14:30:00
```

```
🟢 RÉCUPÉRATION - Service UP

Service: Homebox
Status: Opérationnel
Temps de réponse: 0.45s
Heure: 2026-02-15 14:35:00
```

## 🔧 Commandes utiles

```bash
# Vérification unique
python app.py check

# Rapport de statut
python app.py report

# Monitoring continu
python app.py

# Voir les logs en temps réel
tail -f logs/control-plane.log

# Consulter l'historique
sqlite3 data/history.db "SELECT * FROM checks ORDER BY timestamp DESC LIMIT 10;"
```

## 🐳 Docker

```bash
# Build et run
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

## ❓ Problèmes courants

### "TELEGRAM_BOT_TOKEN must be set"
→ Vérifiez que le fichier `.env` existe et contient votre token

### "Connection timeout"
→ Vérifiez que les URLs de services sont correctes et accessibles

### "Permission denied"
→ Rendez les scripts exécutables: `chmod +x app.py test.py install.sh`

## 📖 Documentation complète

Consultez le [README.md](README.md) pour plus de détails.

## 🆘 Support

Ouvrir une [issue](https://github.com/enabeteleazar/homebox-control-plane/issues) sur GitHub.
