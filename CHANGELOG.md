# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [1.0.0] - 2026-02-16

### 🎉 Refonte majeure - Configuration JSON

#### Ajouté

- **Configuration JSON** : Nouveau système de configuration via fichiers JSON
  - `config/homebox.json` : Configuration complète des services Homebox
  - `config/neron.json` : Configuration complète des services Neron
  - Support multi-services pour Homebox et Neron
  - Attributs par service : `name`, `port`, `enabled`, `description`, `critical`
- **Checker Homebox amélioré** (`src/checkers/homebox.py`)
  - Lecture depuis `config/homebox.json`
  - Support de plusieurs services sur différents ports
  - Vérifications parallèles
  - Distinction services critiques (🔴) / non-critiques (🟡)
  - Fallback automatique vers `.env` si JSON absent
- **Checker Neron amélioré** (`src/checkers/neron.py`)
  - Même architecture que Homebox
  - Lecture depuis `config/neron.json`
  - Support multi-services
  - Configuration flexible
- **Notifications enrichies**
  - Détails par service dans les alertes Telegram
  - Affichage des descriptions de services
  - Distinction visuelle critique/non-critique
- **Documentation complète**
  - `JSON_CONFIG.md` : Guide complet configuration JSON
  - `NERON_CONFIG.md` : Guide spécifique Neron
  - `MULTI_SERVICES.md` : Guide architecture multi-services
  - `DETAILED_CHECKS.md` : Vérifications détaillées
  - `DOCKER.md` : Guide Docker complet
  - Exemples : `homebox.json.example`, `neron.json.example`
- **Support Docker amélioré**
  - `Dockerfile` optimisé avec utilisateur non-root
  - `docker-compose.yml` avec gestion réseau
  - `.dockerignore` pour builds optimisés
  - Volumes pour persistance données/logs

#### Modifié

- **app.py** : Intégration des nouveaux checkers JSON
- **Structure du projet** : Nouvelle organisation `config/`
- **Système de logging** : Amélioration des messages et émojis
- **Gestion des permissions** : Correction problèmes Docker

#### Corrigé

- Erreur d’indentation dans `app.py` (ligne 85)
- Duplication du `NeronChecker`
- Permissions logs/data dans conteneur Docker
- Gestion des erreurs de connexion réseau

### 🔧 Configuration

#### Avant (v1.x)

```env
HOMEBOX_URL=http://192.168.1.130:7745
HOMEBOX_SERVICES=Homebox Main:7745,API:8080,DB:5432
NERON_URL=http://192.168.1.130:3000
```

#### Maintenant (v2.0)

```json
// config/homebox.json
{
  "base_url": "http://192.168.1.130",
  "services": [
    {"name": "Homebox Main", "port": 7745, "enabled": true, "critical": true},
    {"name": "Homebox API", "port": 8080, "enabled": true, "critical": true},
    {"name": "Homebox DB", "port": 5432, "enabled": true, "critical": true}
  ]
}
```

### 📊 Statistiques

- **5 nouveaux fichiers** de documentation
- **3 fichiers JSON** de configuration
- **2 checkers** complètement réécrits
- **4 exemples** de configuration
- **Support illimité** de services par système

### 🚀 Migration depuis v1.x

1. Créer les fichiers JSON :
   
   ```bash
   cp config/homebox.json.example config/homebox.json
   cp config/neron.json.example config/neron.json
   ```
1. Éditer avec vos services :
   
   ```bash
   nano config/homebox.json
   nano config/neron.json
   ```
1. Redémarrer :
   
   ```bash
   docker-compose restart
   # ou
   python3 app.py
   ```

### ⚠️ Breaking Changes

- Les variables `HOMEBOX_SERVICES` et configuration multi-services en `.env` sont maintenant obsolètes
- La configuration se fait exclusivement via JSON
- Les checkers nécessitent les fichiers JSON (fallback vers `.env` disponible)

### 🎯 Prochaines étapes (v2.1)

- [ ] Rechargement à chaud de la configuration
- [ ] API REST pour gestion des services
- [ ] Interface web de configuration
- [ ] Graphiques de performance
- [ ] Support de plus de protocoles (TCP, UDP, ping)

-----

## [1.0.0] - 2026-02-15

### Initial Release

- Monitoring basique Homebox et Neron
- Notifications Telegram
- Configuration via `.env`
- Support Docker
- Base de données SQLite pour historique
