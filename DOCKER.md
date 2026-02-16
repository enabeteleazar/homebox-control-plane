# 🐳 Guide Docker - Homebox Control Plane

## 📋 Table des matières

- [Démarrage rapide](#démarrage-rapide)
- [Configuration](#configuration)
- [Build et déploiement](#build-et-déploiement)
- [Gestion du conteneur](#gestion-du-conteneur)
- [Réseau et connectivité](#réseau-et-connectivité)
- [Logs et debugging](#logs-et-debugging)
- [Sauvegarde et restauration](#sauvegarde-et-restauration)

---

## 🚀 Démarrage rapide

### Option 1 : Docker Compose (Recommandé)

```bash
# 1. Créer le fichier .env avec vos configurations
cp .env.example .env
nano .env  # Éditer avec vos tokens Telegram et URLs

# 2. Build et lancer
docker-compose up -d

# 3. Voir les logs
docker-compose logs -f

# 4. Arrêter
docker-compose down
```

### Option 2 : Docker classique

```bash
# 1. Build l'image
docker build -t homebox-control-plane .

# 2. Lancer le conteneur
docker run -d \
  --name control-plane \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="votre_token" \
  -e TELEGRAM_CHAT_ID="votre_chat_id" \
  -e HOMEBOX_URL="http://192.168.1.130:7745" \
  -e NERON_URL="http://192.168.1.130:3000" \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  homebox-control-plane

# 3. Voir les logs
docker logs -f control-plane
```

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
# Obligatoire
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...
TELEGRAM_CHAT_ID=123456789

# URLs des services
HOMEBOX_URL=http://192.168.1.130:7745
NERON_URL=http://192.168.1.130:3000

# Optionnel
CHECK_INTERVAL=300
CHECK_TIMEOUT=10
MAX_RESPONSE_TIME=5.0
DATABASE_PATH=data/history.db
```

### Configuration du réseau

Si vos services (Homebox, Neron) sont dans des conteneurs Docker sur le **même réseau**, utilisez leurs noms de conteneurs :

```yaml
# docker-compose.yml
services:
  control-plane:
    environment:
      - HOMEBOX_URL=http://homebox:7745  # Nom du conteneur
      - NERON_URL=http://neron:3000
    networks:
      - your_existing_network

networks:
  your_existing_network:
    external: true
```

---

## 🔨 Build et déploiement

### Build l'image

```bash
# Build simple
docker build -t homebox-control-plane .

# Build avec tag de version
docker build -t homebox-control-plane:1.0.0 .

# Build avec docker-compose
docker-compose build

# Build sans cache
docker-compose build --no-cache
```

### Pousser vers un registry (optionnel)

```bash
# Docker Hub
docker tag homebox-control-plane username/homebox-control-plane:latest
docker push username/homebox-control-plane:latest

# Registry privé
docker tag homebox-control-plane registry.example.com/control-plane:latest
docker push registry.example.com/control-plane:latest
```

---

## 🎮 Gestion du conteneur

### Commandes de base

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Voir le statut
docker-compose ps

# Logs en temps réel
docker-compose logs -f

# Logs des 100 dernières lignes
docker-compose logs --tail=100

# Entrer dans le conteneur
docker-compose exec control-plane /bin/bash
```

### Mise à jour

```bash
# 1. Récupérer les changements
git pull

# 2. Rebuild l'image
docker-compose build

# 3. Recréer le conteneur
docker-compose up -d

# Ou en une seule commande
docker-compose up -d --build
```

### Vérification manuelle

```bash
# Lancer un check unique
docker-compose exec control-plane python3 app.py check

# Lancer un rapport
docker-compose exec control-plane python3 app.py report

# Exécuter le diagnostic
docker-compose exec control-plane python3 diagnose.py
```

---

## 🌐 Réseau et connectivité

### Cas 1 : Services sur le même réseau Docker

```yaml
# docker-compose.yml
services:
  homebox:
    image: ghcr.io/hay-kot/homebox:latest
    networks:
      - app-network

  neron:
    image: your-neron-image
    networks:
      - app-network

  control-plane:
    build: .
    environment:
      - HOMEBOX_URL=http://homebox:7745  # Utiliser le nom du service
      - NERON_URL=http://neron:3000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Cas 2 : Services sur l'hôte (host network)

```yaml
services:
  control-plane:
    build: .
    network_mode: host
    environment:
      - HOMEBOX_URL=http://localhost:7745
      - NERON_URL=http://localhost:3000
```

### Cas 3 : Services sur d'autres machines

```yaml
services:
  control-plane:
    build: .
    environment:
      - HOMEBOX_URL=http://192.168.1.100:7745
      - NERON_URL=http://192.168.1.101:3000
```

### Cas 4 : Utiliser un réseau existant

```yaml
services:
  control-plane:
    build: .
    networks:
      - existing_network

networks:
  existing_network:
    external: true
    name: traefik_network  # Nom de votre réseau existant
```

---

## 📊 Logs et debugging

### Voir les logs

```bash
# Logs en temps réel
docker-compose logs -f control-plane

# Logs depuis X minutes
docker-compose logs --since 30m control-plane

# Logs entre deux dates
docker-compose logs --since 2026-02-15T10:00:00 --until 2026-02-15T12:00:00

# Sauvegarder les logs
docker-compose logs control-plane > control-plane-logs.txt
```

### Logs applicatifs

```bash
# Voir le fichier de log de l'application
docker-compose exec control-plane tail -f /app/logs/control-plane.log

# Ou depuis l'hôte (si volume monté)
tail -f ./logs/control-plane.log
```

### Debugging

```bash
# Vérifier la configuration
docker-compose exec control-plane cat .env

# Vérifier les variables d'environnement
docker-compose exec control-plane env | grep -E "TELEGRAM|HOMEBOX|NERON"

# Test de connexion
docker-compose exec control-plane python3 -c "
from src.config import Config
c = Config()
print(f'Homebox: {c.homebox_url}')
print(f'Neron: {c.neron_url}')
"

# Tester la connectivité réseau
docker-compose exec control-plane ping -c 3 192.168.1.130
docker-compose exec control-plane curl -v http://192.168.1.130:7745
```

### Healthcheck

```bash
# Voir le statut du healthcheck
docker inspect control-plane | grep -A 10 Health

# Forcer un healthcheck
docker exec control-plane python3 -c "import sys; sys.exit(0)"
```

---

## 💾 Sauvegarde et restauration

### Sauvegarder les données

```bash
# Créer un backup
tar -czf control-plane-backup-$(date +%Y%m%d).tar.gz data/ logs/

# Ou avec docker
docker run --rm \
  -v $(pwd)/data:/data:ro \
  -v $(pwd)/logs:/logs:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d).tar.gz /data /logs
```

### Restaurer les données

```bash
# Extraire le backup
tar -xzf control-plane-backup-20260215.tar.gz

# Redémarrer le conteneur
docker-compose restart
```

### Base de données SQLite

```bash
# Backup de la base de données
docker-compose exec control-plane sqlite3 /app/data/history.db .dump > backup.sql

# Restaurer
cat backup.sql | docker-compose exec -T control-plane sqlite3 /app/data/history.db
```

---

## 🔧 Dépannage

### Conteneur ne démarre pas

```bash
# Voir les erreurs
docker-compose logs control-plane

# Vérifier la config
docker-compose config

# Reconstruire from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problèmes de permissions

```bash
# Corriger les permissions des volumes
sudo chown -R 1000:1000 data/ logs/

# Ou recréer les dossiers
rm -rf data/ logs/
mkdir data logs
chmod 755 data logs
```

### Conteneur en erreur de restart loop

```bash
# Voir les logs d'erreur
docker logs control-plane 2>&1 | grep -i error

# Lancer en mode interactif pour debug
docker-compose run --rm control-plane /bin/bash
```

### Problèmes réseau

```bash
# Lister les réseaux
docker network ls

# Inspecter le réseau
docker network inspect monitoring

# Ping depuis le conteneur
docker-compose exec control-plane ping homebox
docker-compose exec control-plane curl http://homebox:7745
```

---

## 📋 Docker Compose - Exemples complets

### Configuration complète avec tous les services

```yaml
version: '3.8'

services:
  homebox:
    image: ghcr.io/hay-kot/homebox:latest
    container_name: homebox
    restart: unless-stopped
    ports:
      - "7745:7745"
    volumes:
      - homebox-data:/data
    networks:
      - monitoring

  neron:
    image: your-neron-image:latest
    container_name: neron
    restart: unless-stopped
    ports:
      - "3000:3000"
    networks:
      - monitoring

  control-plane:
    build: .
    container_name: homebox-control-plane
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOMEBOX_URL=http://homebox:7745
      - NERON_URL=http://neron:3000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - monitoring
    depends_on:
      - homebox
      - neron

volumes:
  homebox-data:

networks:
  monitoring:
    driver: bridge
```

---

## 🎯 Bonnes pratiques

1. **Toujours utiliser `.env`** pour les secrets (ne jamais commiter)
2. **Volumes nommés** pour les données importantes
3. **Restart policy** : `unless-stopped` ou `always`
4. **Limites de ressources** pour éviter la surconsommation
5. **Healthchecks** pour monitoring automatique
6. **Logs rotatifs** pour éviter saturation disque
7. **Backups réguliers** de la base de données

---

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Besoin d'aide ?** Ouvrez une issue sur GitHub !
