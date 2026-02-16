# 🔧 Configuration Multi-Services Homebox

## Vue d'ensemble

Le Control Plane supporte maintenant le monitoring de **plusieurs services Homebox** fonctionnant sur **différents ports**.

## Cas d'usage

Si votre architecture Homebox ressemble à :
- `http://192.168.1.130:7745` - Homebox Main (frontend)
- `http://192.168.1.130:8080` - Homebox API
- `http://192.168.1.130:5432` - PostgreSQL Database
- `http://192.168.1.130:6379` - Redis Cache

Vous pouvez monitorer **tous ces services** individuellement et recevoir des alertes spécifiques pour chaque service.

## Configuration

### Option 1 : Service unique (par défaut)

Pour un seul service Homebox :

```env
HOMEBOX_URL=http://192.168.1.130:7745
```

### Option 2 : Plusieurs services

Pour monitorer plusieurs services sur différents ports :

```env
# URL de base (sans port)
HOMEBOX_URL=http://192.168.1.130

# Liste des services
HOMEBOX_SERVICES=Homebox Main:7745,Homebox API:8080,Homebox DB:5432,Homebox Cache:6379
```

**Format** : `NOM_SERVICE:PORT,NOM_SERVICE:PORT,...`

### Exemples de configuration

#### Exemple 1 : Architecture micro-services

```env
HOMEBOX_URL=http://192.168.1.100
HOMEBOX_SERVICES=Frontend:7745,API Gateway:8080,Auth Service:8081,Database:5432
```

#### Exemple 2 : Setup avec cache

```env
HOMEBOX_URL=http://homebox.local
HOMEBOX_SERVICES=Web:80,API:8080,Redis:6379
```

#### Exemple 3 : Configuration complète

```env
# Base
HOMEBOX_URL=http://192.168.1.130

# Services
HOMEBOX_SERVICES=Homebox Main:7745,Homebox API:8080,PostgreSQL:5432,Redis:6379,Backup Service:9000

# Autres paramètres
CHECK_INTERVAL=180
CHECK_TIMEOUT=10
```

## Notifications

### Service individuel DOWN

Quand un service spécifique tombe :

```
🔴 ALERTE - Service DOWN

Service: Homebox
Status: Indisponible
Erreur: Services DOWN: PostgreSQL

Détails:
   ✅ Homebox Main: UP (0.23s)
   ✅ Homebox API: UP (0.31s)
   🔴 PostgreSQL: DOWN (10.00s)
   ✅ Redis: UP (0.15s)

Heure: 2026-02-15 20:00:00
```

### Tous les services UP

```
🟢 RÉCUPÉRATION - Service UP

Service: Homebox
Status: Opérationnel
Temps de réponse: 0.42s

Détails:
   ✅ Homebox Main: UP (0.23s)
   ✅ Homebox API: UP (0.31s)
   ✅ PostgreSQL: UP (0.55s)
   ✅ Redis: UP (0.15s)

Heure: 2026-02-15 20:05:00
```

### Plusieurs services DOWN

```
🔴 ALERTE - Service DOWN

Service: Homebox
Status: Indisponible
Erreur: Services DOWN: PostgreSQL, Redis

Détails:
   ✅ Homebox Main: UP (0.23s)
   ✅ Homebox API: UP (0.31s)
   🔴 PostgreSQL: DOWN (10.00s)
   🔴 Redis: DOWN (10.00s)

Heure: 2026-02-15 20:10:00
```

## Comportement

### Agrégation

Le système considère que **Homebox est UP** seulement si **TOUS** les services sont UP.

Si au moins un service est DOWN, **Homebox est considéré DOWN** et une alerte est envoyée.

### Temps de réponse

Le temps de réponse affiché est la **moyenne** de tous les services.

### Vérifications parallèles

Tous les services sont vérifiés **en parallèle** pour de meilleures performances.

## Conseils de configuration

### Noms des services

Choisissez des noms **descriptifs** et **courts** :

✅ **Bon** :
```
Homebox_SERVICES=Frontend:7745,API:8080,DB:5432,Cache:6379
```

❌ **Éviter** :
```
HOMEBOX_SERVICES=Service de frontend Homebox principal:7745,Service API REST Homebox:8080
```

### Ordre des services

L'ordre n'a pas d'importance, mais il est recommandé de mettre :
1. Services critiques en premier
2. Services moins critiques ensuite

```
HOMEBOX_SERVICES=Database:5432,API:8080,Frontend:7745,Cache:6379
```

### Timeouts

Si vous avez beaucoup de services, augmentez le timeout :

```env
# Pour 4+ services
CHECK_TIMEOUT=15

# Pour 8+ services
CHECK_TIMEOUT=20
```

## Migration

### Depuis configuration simple

**Avant** :
```env
HOMEBOX_URL=http://192.168.1.130:7745
```

**Après** :
```env
HOMEBOX_URL=http://192.168.1.130
HOMEBOX_SERVICES=Homebox Main:7745,Homebox API:8080,Homebox DB:5432
```

### Test de la migration

1. Sauvegarder votre `.env` actuel
2. Ajouter `HOMEBOX_SERVICES`
3. Tester avec `python3 test.py`
4. Vérifier les logs pour voir tous les services

```bash
# Test
python3 test.py

# Vous devriez voir :
# Homebox checker initialisé avec 3 service(s)
# Homebox Main checker initialisé: http://192.168.1.130:7745
# Homebox API checker initialisé: http://192.168.1.130:8080
# Homebox DB checker initialisé: http://192.168.1.130:5432
```

## Troubleshooting

### Erreur de parsing

```
⚠️ Port invalide pour Homebox Main: abc
```

**Solution** : Vérifier que tous les ports sont des nombres valides.

```env
# ❌ Mauvais
HOMEBOX_SERVICES=Frontend:abc,API:8080

# ✅ Correct
HOMEBOX_SERVICES=Frontend:7745,API:8080
```

### Services ignorés

Si certains services n'apparaissent pas dans les logs :

1. Vérifier le format : `NOM:PORT`
2. Pas d'espaces autour du `:`
3. Utiliser une virgule `,` comme séparateur

```env
# ❌ Mauvais
HOMEBOX_SERVICES=Frontend: 7745, API :8080

# ✅ Correct
HOMEBOX_SERVICES=Frontend:7745,API:8080
```

### Tous les services montrent DOWN

Vérifier que `HOMEBOX_URL` contient bien l'URL de base **sans port** :

```env
# ❌ Mauvais
HOMEBOX_URL=http://192.168.1.130:7745
HOMEBOX_SERVICES=Frontend:7745,API:8080

# ✅ Correct
HOMEBOX_URL=http://192.168.1.130
HOMEBOX_SERVICES=Frontend:7745,API:8080
```

### Performances dégradées

Avec beaucoup de services, les checks peuvent prendre du temps :

```env
# Augmenter le timeout
CHECK_TIMEOUT=20

# Ou réduire la fréquence
CHECK_INTERVAL=600  # 10 minutes au lieu de 5
```

## Exemples complets

### Exemple 1 : Setup classique avec BDD

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789

HOMEBOX_URL=http://192.168.1.130
HOMEBOX_SERVICES=Frontend:7745,API:8080,PostgreSQL:5432

NERON_URL=http://192.168.1.130:3000

CHECK_INTERVAL=300
CHECK_TIMEOUT=15
```

### Exemple 2 : Architecture complète

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789

HOMEBOX_URL=http://192.168.1.130
HOMEBOX_SERVICES=Web:80,API:8080,Auth:8081,Database:5432,Redis:6379,Worker:9000

NERON_URL=http://192.168.1.131:3000

CHECK_INTERVAL=180
CHECK_TIMEOUT=20
MAX_RESPONSE_TIME=5.0
```

### Exemple 3 : Docker avec noms de conteneurs

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789

HOMEBOX_URL=http://homebox
HOMEBOX_SERVICES=Frontend:7745,API:8080,Database:5432

NERON_URL=http://neron:3000

CHECK_INTERVAL=300
CHECK_TIMEOUT=15
```

## Questions fréquentes

### Q: Puis-je mixer services avec et sans port dans HOMEBOX_SERVICES ?

**Oui**, mais tous doivent avoir un port défini dans le format `NOM:PORT`.

### Q: Combien de services puis-je monitorer ?

**Pas de limite technique**, mais pour les performances :
- 1-5 services : Optimal
- 6-10 services : Bon (augmenter CHECK_TIMEOUT à 15-20s)
- 10+ services : Possible (CHECK_TIMEOUT=30s, CHECK_INTERVAL plus long)

### Q: Les services doivent-ils être sur le même hôte ?

**Non**. Vous pouvez modifier le code pour supporter différents hôtes par service si nécessaire.

### Q: Puis-je utiliser des noms de domaine ?

**Oui** :
```env
HOMEBOX_URL=https://homebox.mondomaine.com
HOMEBOX_SERVICES=Frontend:443,API:8080
```

### Q: Est-ce compatible avec HTTPS ?

**Oui**, utilisez simplement `https://` dans HOMEBOX_URL.

---

**Besoin d'aide ?** Consultez les logs avec `tail -f logs/control-plane.log`
