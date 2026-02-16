# 🔍 Vérification Détaillée des Services Homebox

## Vue d'ensemble

Le Control Plane peut maintenant vérifier non seulement si Homebox est accessible, mais aussi **l'état de chaque service interne** de l'API Homebox.

## Fonctionnalités

### Vérifications effectuées

Quand `CHECK_HOMEBOX_SERVICES=true`, le checker vérifie :

1. **Health Endpoint** (`/api/v1/status`)
   - État général du service
   - Version de Homebox
   - État de la base de données

2. **Endpoints API** :
   - ✅ `/api/v1/items` - Gestion des items
   - ✅ `/api/v1/locations` - Gestion des emplacements
   - ✅ `/api/v1/labels` - Gestion des étiquettes
   - ✅ `/api/v1/users/self` - Informations utilisateur

### Codes de statut

- ✅ **Service OK** - Endpoint répond correctement
- 🔒 **Auth requise** - Endpoint nécessite authentification (normal, service UP)
- ❌ **Service DOWN** - Endpoint inaccessible

## Configuration

### Activer/Désactiver

Dans votre fichier `.env` :

```env
# Activer la vérification détaillée (recommandé)
CHECK_HOMEBOX_SERVICES=true

# Désactiver (vérification basique uniquement)
CHECK_HOMEBOX_SERVICES=false
```

## Exemples de notifications

### Service complètement UP

```
🟢 RÉCUPÉRATION - Service UP

Service: Homebox
Status: Opérationnel
Temps de réponse: 0.35s
Heure: 2026-02-15 20:00:00

Détails:
   ✅ Health endpoint OK
   Version: 0.10.3
   ✅ Database
   API: ✅ items, ✅ locations, ✅ labels, 🔒 users
```

### Service partiellement UP

```
⚠️ AVERTISSEMENT - Performance dégradée

Service: Homebox
Temps de réponse: 6.2s
Seuil: 5.0s
Heure: 2026-02-15 20:05:00

Détails:
   ✅ Health endpoint OK
   ⚠️ Health endpoint indisponible
   API: ❌ items, ✅ locations, ✅ labels, ✅ users
```

### Service DOWN

```
🔴 ALERTE - Service DOWN

Service: Homebox
Status: Indisponible
Code HTTP: N/A
Erreur: Connexion impossible: Cannot connect to host
Heure: 2026-02-15 20:10:00
```

## Avantages

### 1. Détection proactive

Au lieu de simplement savoir si Homebox répond, vous savez **exactement quel service est en panne**.

Exemple :
- ❌ **Avant** : "Homebox est DOWN"
- ✅ **Après** : "Homebox est UP mais l'endpoint items ne répond pas"

### 2. Diagnostic rapide

Les notifications incluent les détails, ce qui permet de diagnostiquer rapidement :
- Problème de base de données ?
- Un endpoint spécifique qui ne répond pas ?
- Problème d'authentification ?

### 3. Monitoring granulaire

Vous pouvez surveiller la santé de chaque composant de Homebox séparément.

## Performance

### Impact

- ⏱️ **Temps additionnel** : ~0.5-1 seconde par check
- 🌐 **Requêtes supplémentaires** : 4-5 requêtes HTTP au lieu d'une seule
- 💾 **Charge réseau** : Minimale (quelques Ko par check)

### Recommandations

✅ **Activer si** :
- Vous gérez une instance Homebox critique
- Vous voulez des diagnostics détaillés
- Vous avez une bonne connexion réseau

⚠️ **Désactiver si** :
- Vous voulez minimiser les requêtes réseau
- Vous avez une connexion limitée
- Vous faites des checks très fréquents (<1 minute)

## Personnalisation

Vous pouvez modifier les endpoints vérifiés en éditant `src/checkers/homebox.py` :

```python
# Dans la méthode check_api_endpoints
endpoints = {
    'items': f"{self.api_base}/items",
    'locations': f"{self.api_base}/locations",
    'labels': f"{self.api_base}/labels",
    'users': f"{self.api_base}/users/self",
    # Ajoutez vos propres endpoints ici
    'custom': f"{self.api_base}/custom/endpoint",
}
```

## Troubleshooting

### Tous les endpoints montrent "🔒 Auth requise"

C'est **normal** si Homebox nécessite une authentification. Le checker ne s'authentifie pas (par design), mais détecte quand même que le service est UP.

### Faux positifs sur certains endpoints

Certains endpoints peuvent être désactivés selon votre configuration Homebox. Cela ne signifie pas que Homebox est DOWN.

### Performance dégradée

Si vous voyez des temps de réponse élevés uniquement quand la vérification détaillée est activée :

```env
# Désactiver temporairement
CHECK_HOMEBOX_SERVICES=false

# Ou augmenter le timeout
CHECK_TIMEOUT=20
```

## Questions fréquentes

### Q: Faut-il fournir un token API pour la vérification ?

**Non.** Le checker ne nécessite pas d'authentification. Il vérifie simplement si les endpoints répondent (même avec une erreur 401 "non autorisé", ce qui prouve que le service fonctionne).

### Q: Cela fonctionne-t-il avec d'autres versions de Homebox ?

**Oui.** Le checker est compatible avec toutes les versions de Homebox qui utilisent l'API `/api/v1/*`.

### Q: Puis-je ajouter d'autres services à vérifier ?

**Oui !** Vous pouvez créer des checkers similaires pour d'autres applications en vous inspirant du code de `homebox.py`.

### Q: Que se passe-t-il si un seul endpoint est DOWN ?

Le service est considéré comme **UP** (car Homebox répond), mais l'erreur est mentionnée dans les détails. Aucune alerte DOWN n'est envoyée, mais vous verrez l'info dans les logs.

## Exemples d'utilisation

### Développement

```env
# Vérification basique uniquement (plus rapide)
CHECK_HOMEBOX_SERVICES=false
CHECK_INTERVAL=60  # Check toutes les minutes
```

### Production

```env
# Vérification complète
CHECK_HOMEBOX_SERVICES=true
CHECK_INTERVAL=300  # Check toutes les 5 minutes
CHECK_TIMEOUT=15
```

### Instance critique

```env
# Vérification très fréquente avec détails
CHECK_HOMEBOX_SERVICES=true
CHECK_INTERVAL=60   # Check toutes les minutes
CHECK_TIMEOUT=10
MAX_RESPONSE_TIME=3.0  # Alerte si > 3 secondes
```

---

**Besoin d'aide ?** Consultez les logs avec `docker-compose logs -f` ou `tail -f logs/control-plane.log`
