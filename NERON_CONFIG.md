# 📝 Configuration Neron via JSON

## Vue d'ensemble

Comme pour Homebox, Neron utilise maintenant un fichier JSON pour sa configuration.

**Emplacement** : `config/neron.json`

## Configuration simple (1 service)

```json
{
  "base_url": "http://192.168.1.130",
  "services": [
    {
      "name": "Neron Main",
      "port": 3000,
      "enabled": true,
      "description": "Service principal Neron",
      "critical": true
    }
  ],
  "settings": {
    "timeout": 10,
    "max_response_time": 5.0,
    "check_parallel": true
  }
}
```

## Configuration multi-services

Si Neron a plusieurs composants :

```json
{
  "base_url": "http://192.168.1.130",
  "services": [
    {
      "name": "Neron Frontend",
      "port": 3000,
      "enabled": true,
      "description": "Interface web",
      "critical": true
    },
    {
      "name": "Neron API",
      "port": 3001,
      "enabled": true,
      "description": "API REST",
      "critical": true
    },
    {
      "name": "Neron Worker",
      "port": 3002,
      "enabled": true,
      "description": "Worker background",
      "critical": false
    },
    {
      "name": "Neron WebSocket",
      "port": 3003,
      "enabled": true,
      "description": "Serveur WebSocket temps réel",
      "critical": true
    }
  ],
  "settings": {
    "timeout": 15,
    "max_response_time": 5.0,
    "check_parallel": true
  }
}
```

## Installation

```bash
cd /opt/Homebox_Control

# 1. Créer votre configuration depuis l'exemple
cp config/neron.json.example config/neron.json

# 2. Éditer avec vos valeurs
nano config/neron.json

# 3. Tester
python3 test.py

# 4. Redémarrer le conteneur
docker-compose restart
```

## Exemples de services Neron

Selon votre architecture Neron, vous pourriez avoir :

```json
{
  "services": [
    {"name": "Neron Web", "port": 3000, "enabled": true, "critical": true},
    {"name": "Neron API", "port": 8080, "enabled": true, "critical": true},
    {"name": "Neron Auth", "port": 8081, "enabled": true, "critical": true},
    {"name": "Neron Database", "port": 5432, "enabled": true, "critical": true},
    {"name": "Neron Cache", "port": 6379, "enabled": true, "critical": false},
    {"name": "Neron Queue", "port": 5672, "enabled": true, "critical": false}
  ]
}
```

## Désactiver temporairement un service

```json
{
  "name": "Neron Worker",
  "port": 3002,
  "enabled": false  // Service ignoré pendant le monitoring
}
```

## Services non-critiques

```json
{
  "name": "Neron Cache",
  "port": 6379,
  "critical": false  // Alerte 🟡 au lieu de 🔴 si DOWN
}
```

## Validation

Vérifier la syntaxe JSON :

```bash
python3 -c "import json; json.load(open('config/neron.json'))" && echo "✅ JSON valide" || echo "❌ JSON invalide"
```

## Notifications attendues

### Service unique UP
```
✅ Neron OK (0.15s)
```

### Multi-services tous UP
```
✅ Neron OK (0.42s)

Détails:
   ✅ Neron Frontend: UP (0.23s) - Interface web
   ✅ Neron API: UP (0.31s) - API REST
   ✅ Neron Worker: UP (0.55s) - Worker background
   ✅ Neron WebSocket: UP (0.15s) - Serveur WebSocket
```

### Un service DOWN
```
🔴 ALERTE - Service DOWN

Service: Neron
Erreur: Services critiques DOWN: Neron API

Détails:
   ✅ Neron Frontend: UP (0.23s) - Interface web
   🔴 Neron API: DOWN (10.00s) - API REST
   ✅ Neron Worker: UP (0.55s) - Worker background
   ✅ Neron WebSocket: UP (0.15s) - Serveur WebSocket
```

## Fichiers de configuration

Vous avez maintenant **deux fichiers JSON** à gérer :

```
config/
├── homebox.json       # Services Homebox
└── neron.json         # Services Neron
```

Chaque fichier est **indépendant** et peut avoir :
- Des URLs différentes
- Des timeouts différents
- Des nombres de services différents

## Troubleshooting

### Neron ne se charge pas

Vérifier que le fichier existe :
```bash
ls -la config/neron.json
```

Si absent, le système utilisera le fallback depuis `.env` :
```env
NERON_URL=http://192.168.1.130:3000
```

### Erreur de syntaxe JSON

```bash
# Afficher les erreurs
python3 -m json.tool config/neron.json
```

### Tester la configuration

```bash
# Test complet
python3 test.py

# Logs attendus:
# 📄 Chargement de la configuration depuis config/neron.json
# 🔧 Configuration chargée:
#    URL de base: http://192.168.1.130
#    Services configurés:
#       🔴 Neron Main:3000
# ✅ Neron checker initialisé avec 1 service(s)
```

## Avantages de la configuration JSON

✅ **Symétrie** - Même approche pour Homebox et Neron  
✅ **Flexibilité** - Gérer plusieurs services Neron facilement  
✅ **Clarté** - Configuration lisible et structurée  
✅ **Évolutivité** - Ajouter des services sans toucher au code  
✅ **Criticité** - Distinguer services critiques et non-critiques  

---

Pour plus de détails, consultez `JSON_CONFIG.md`
