# 🏠 Homebox Control Plane

Système de monitoring automatique pour **Homebox** et **Neron** avec notifications en temps réel via Telegram.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Développement](#-développement)

## ✨ Fonctionnalités

- 🔍 **Monitoring continu** - Vérification périodique de l'état des services
- 📱 **Notifications Telegram** - Alertes instantanées en cas de problème
- 📊 **Historique** - Stockage des vérifications dans une base SQLite
- ⚡ **Asynchrone** - Vérifications parallèles pour de meilleures performances
- 🎯 **Détection intelligente** - Distinction entre DOWN, SLOW et récupération
- 📈 **Statistiques** - Rapports d'uptime et métriques de performance
- 🔄 **Auto-recovery** - Notifications quand les services reviennent en ligne

### Types de notifications

| Icône | Type | Description |
|-------|------|-------------|
| 🔴 | **ALERTE** | Service DOWN ou erreur critique |
| ⚠️ | **AVERTISSEMENT** | Service lent ou performance dégradée |
| 🟢 | **RÉCUPÉRATION** | Service revenu en ligne |
| ℹ️ | **INFO** | Démarrage, rapport, informations générales |

## 🔧 Prérequis

- **Python 3.8+**
- **Un bot Telegram** (gratuit)
- Accès réseau aux services à monitorer

### Créer un bot Telegram

1. Ouvrir Telegram et rechercher **@BotFather**
2. Envoyer `/newbot` et suivre les instructions
3. Copier le **token** fourni (format: `123456:ABCdefGHI...`)
4. Pour obtenir votre `chat_id`:
   - Envoyer un message à votre bot
   - Visiter: `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates`
   - Copier la valeur de `chat.id`

## 📥 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/enabeteleazar/homebox-control-plane.git
cd homebox-control-plane
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
nano .env  # ou utilisez votre éditeur préféré
```

Remplir les valeurs obligatoires:
```bash
TELEGRAM_BOT_TOKEN=votre_token_ici
TELEGRAM_CHAT_ID=votre_chat_id_ici
HOMEBOX_URL=http://votre-homebox:7745
NERON_URL=http://votre-neron:3000
```

## ⚙️ Configuration

### Variables d'environnement (.env)

| Variable | Obligatoire | Par défaut | Description |
|----------|-------------|------------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Token du bot Telegram |
| `TELEGRAM_CHAT_ID` | ✅ | - | ID du chat Telegram |
| `HOMEBOX_URL` | ❌ | `http://localhost:7745` | URL de Homebox |
| `NERON_URL` | ❌ | `http://localhost:3000` | URL de Neron |
| `CHECK_INTERVAL` | ❌ | `300` | Intervalle entre checks (secondes) |
| `CHECK_TIMEOUT` | ❌ | `10` | Timeout HTTP (secondes) |
| `MAX_RESPONSE_TIME` | ❌ | `5.0` | Seuil d'alerte temps de réponse (s) |
| `DATABASE_PATH` | ❌ | `data/history.db` | Chemin de la base de données |

### Configuration YAML (optionnelle)

Vous pouvez également utiliser `config/config.yaml` pour la configuration. Les variables d'environnement ont la priorité.

## 🚀 Utilisation

### Diagnostic rapide (en cas de problème)

Si vous rencontrez des problèmes d'import, lancez d'abord le diagnostic:

```bash
python3 diagnose.py
```

Ce script va vérifier:
- La structure des fichiers
- Les dépendances installées
- L'environnement virtuel
- La configuration

### Mode monitoring continu (recommandé)

Lance le monitoring en continu avec vérifications périodiques:

```bash
python app.py
```

Le système va:
- ✅ Vérifier les services toutes les 5 minutes (configurable)
- 📱 Envoyer des notifications en cas de changement d'état
- 📊 Générer un rapport quotidien automatique
- 💾 Sauvegarder l'historique dans la base de données

### Vérification unique

Pour une seule vérification (utile pour tester):

```bash
python app.py check
```

### Générer un rapport

Pour envoyer un rapport de statut immédiat:

```bash
python app.py report
```

### Lancer en arrière-plan (production)

#### Option 1: Screen

```bash
screen -S control-plane
python app.py
# Ctrl+A puis D pour détacher
```

Pour revenir:
```bash
screen -r control-plane
```

#### Option 2: Systemd (Linux)

Créer `/etc/systemd/system/control-plane.service`:

```ini
[Unit]
Description=Homebox Control Plane
After=network.target

[Service]
Type=simple
User=votre_user
WorkingDirectory=/chemin/vers/homebox-control-plane
Environment="PATH=/chemin/vers/homebox-control-plane/venv/bin"
ExecStart=/chemin/vers/homebox-control-plane/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activer et démarrer:
```bash
sudo systemctl enable control-plane
sudo systemctl start control-plane
sudo systemctl status control-plane
```

#### Option 3: Docker (à venir)

```bash
docker-compose up -d
```

## 📁 Architecture

```
homebox-control-plane/
├── app.py                          # Point d'entrée principal
├── requirements.txt                # Dépendances Python
├── .env.example                    # Template de configuration
├── .gitignore                      # Fichiers à ignorer par Git
│
├── config/
│   └── config.yaml                 # Configuration YAML optionnelle
│
├── src/
│   ├── config.py                   # Gestionnaire de configuration
│   │
│   ├── checkers/                   # Modules de vérification
│   │   ├── homebox.py             # Checker pour Homebox
│   │   └── neron.py               # Checker pour Neron
│   │
│   ├── notifiers/                  # Modules de notification
│   │   └── telegram.py            # Notifier Telegram
│   │
│   └── database/                   # Gestion de la base de données
│       └── history.py             # Historique des vérifications
│
├── data/                           # Base de données (créé automatiquement)
│   └── history.db                 # SQLite database
│
└── logs/                           # Logs (créé automatiquement)
    └── control-plane.log          # Fichier de logs
```

### Flux de fonctionnement

```
┌─────────────┐
│   app.py    │  Point d'entrée
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  ControlPlane   │  Orchestrateur principal
└────────┬────────┘
         │
         ├─────────────────────┬─────────────────────┐
         ▼                     ▼                     ▼
   ┌──────────┐         ┌──────────┐         ┌──────────┐
   │ Homebox  │         │  Neron   │         │ History  │
   │ Checker  │         │ Checker  │         │ Manager  │
   └────┬─────┘         └────┬─────┘         └────┬─────┘
        │                    │                     │
        └────────────┬───────┘                     │
                     ▼                             ▼
              ┌─────────────┐              ┌─────────────┐
              │  Telegram   │              │   SQLite    │
              │  Notifier   │              │  Database   │
              └─────────────┘              └─────────────┘
```

## 🛠️ Développement

### Structure d'un Checker

Pour ajouter un nouveau service à monitorer, créer un nouveau checker:

```python
# src/checkers/monservice.py
import aiohttp
import time
from app import ServiceStatus

class MonServiceChecker:
    def __init__(self, url: str, timeout: int = 10):
        self.name = "MonService"
        self.url = url
        self.timeout = timeout
    
    async def check(self):
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    response_time = time.time() - start_time
                    
                    return ServiceStatus(
                        service_name=self.name,
                        is_healthy=response.status == 200,
                        response_time=response_time,
                        status_code=response.status
                    )
        except Exception as e:
            return ServiceStatus(
                service_name=self.name,
                is_healthy=False,
                response_time=time.time() - start_time,
                error=str(e)
            )
```

Puis l'ajouter dans `app.py`:

```python
from src.checkers.monservice import MonServiceChecker

# Dans __init__ de ControlPlane
self.checkers.append(
    MonServiceChecker(url=self.config.monservice_url)
)
```

### Tests

```bash
# Test de connexion Telegram
python -c "
import asyncio
from src.notifiers.telegram import TelegramNotifier
from src.config import Config

config = Config()
notifier = TelegramNotifier(config.telegram_bot_token, config.telegram_chat_id)
asyncio.run(notifier.send_info('Test de connexion OK!'))
"
```

### Logs

Les logs sont enregistrés dans:
- **Console** (stdout) - Niveau INFO par défaut
- **Fichier** `logs/control-plane.log` - Tous les niveaux

Pour activer le mode debug:
```bash
# Dans config/config.yaml
log_level: "DEBUG"
```

## 📊 Base de données

### Structure

La base SQLite contient l'historique des vérifications:

```sql
CREATE TABLE checks (
    id INTEGER PRIMARY KEY,
    service_name TEXT,
    timestamp DATETIME,
    is_healthy BOOLEAN,
    response_time REAL,
    status_code INTEGER,
    error TEXT
);
```

### Requêtes utiles

```bash
# Ouvrir la base
sqlite3 data/history.db

# Voir les dernières vérifications
SELECT * FROM checks ORDER BY timestamp DESC LIMIT 10;

# Statistiques d'uptime
SELECT 
    service_name,
    COUNT(*) as total,
    SUM(is_healthy) as successes,
    ROUND(SUM(is_healthy) * 100.0 / COUNT(*), 2) as uptime_pct
FROM checks
GROUP BY service_name;

# Incidents récents
SELECT * FROM checks 
WHERE is_healthy = 0 
ORDER BY timestamp DESC 
LIMIT 20;
```

## 🤝 Contribution

Les contributions sont les bienvenues! Pour contribuer:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🐛 Signaler un bug

Si vous rencontrez un problème, ouvrez une [issue](https://github.com/enabeteleazar/homebox-control-plane/issues) avec:
- Description du problème
- Étapes pour reproduire
- Logs pertinents
- Configuration (sans les tokens!)

## 💡 Roadmap

- [ ] Interface web pour visualiser l'historique
- [ ] Support de plus de notifiers (Email, Slack, Discord)
- [ ] Docker Compose pour déploiement simplifié
- [ ] Métriques Prometheus
- [ ] Tests unitaires
- [ ] Bot Telegram interactif avec commandes

## 👤 Auteur

**enabeteleazar**

- GitHub: [@enabeteleazar](https://github.com/enabeteleazar)

---

⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile!
