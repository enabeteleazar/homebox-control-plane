# 🔧 Guide de Dépannage

## Problème: "No module named 'src.config'"

### Solution 1: Utiliser le script run.sh (recommandé)

```bash
# Au lieu de:
python3 test.py

# Utilisez:
bash run.sh test

# Ou pour lancer l'app:
bash run.sh
```

Le script `run.sh` configure automatiquement le PYTHONPATH.

### Solution 2: Définir PYTHONPATH manuellement

```bash
# Depuis le dossier du projet
export PYTHONPATH="${PWD}:${PYTHONPATH}"
python3 test.py
```

### Solution 3: Utiliser python -m

```bash
# Depuis le dossier du projet
python3 -m test
python3 -m app
```

---

## Problème: "TELEGRAM_BOT_TOKEN must be set"

### Vérifications:

1. Le fichier `.env` existe-t-il ?
```bash
ls -la .env
```

2. Le fichier contient-il les bonnes valeurs ?
```bash
cat .env | grep TELEGRAM
```

3. Le format est-il correct ?
```bash
# BON format (pas de guillemets, pas d'espaces):
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...

# MAUVAIS formats:
TELEGRAM_BOT_TOKEN = 123456789:ABCdefGHI...    # Espaces autour du =
TELEGRAM_BOT_TOKEN="123456789:ABCdefGHI..."    # Guillemets
TELEGRAM_BOT_TOKEN=your_token_here             # Token non remplacé
```

### Solution:

```bash
# Copier le template
cp .env.example .env

# Éditer avec vos vraies valeurs
nano .env
```

---

## Problème: "Connection timeout" ou "Could not resolve host"

### Causes possibles:

1. **URL incorrecte**
```bash
# Vérifier dans .env:
echo $HOMEBOX_URL
echo $NERON_URL

# Format correct:
HOMEBOX_URL=http://192.168.1.50:7745  ✅
NERON_URL=https://neron.example.com   ✅

# Formats incorrects:
HOMEBOX_URL=192.168.1.50:7745         ❌ (manque http://)
HOMEBOX_URL=http://localhost:7745/    ❌ (trailing slash)
```

2. **Service non accessible**
```bash
# Tester manuellement:
curl http://localhost:7745
curl http://192.168.1.50:3000

# Si curl échoue, le service n'est pas accessible
```

3. **Firewall**
```bash
# Vérifier que les ports sont ouverts:
sudo ufw status
sudo iptables -L
```

### Solution:

```bash
# 1. Vérifier que les services tournent:
docker ps  # Si en Docker
systemctl status homebox  # Si service systemd

# 2. Tester la connectivité:
ping 192.168.1.50
telnet 192.168.1.50 7745

# 3. Ajuster CHECK_TIMEOUT dans .env si réseau lent:
CHECK_TIMEOUT=30
```

---

## Problème: Pas de notifications Telegram

### Vérifications:

1. **Bot Token valide ?**
```bash
# Tester l'API Telegram:
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getMe"

# Si erreur 401: token invalide
# Si succès: {"ok":true,"result":{...}}
```

2. **Chat ID correct ?**
```bash
# Obtenir votre chat_id:
# 1. Envoyer un message à votre bot
# 2. Visiter:
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates"

# Chercher "chat":{"id":123456789}
```

3. **Le bot peut-il envoyer des messages ?**
```bash
# Test manuel:
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>" \
  -d "text=Test"
```

### Solution:

```bash
# Utiliser le script de test:
bash run.sh test

# Vérifier les logs:
tail -f logs/control-plane.log
```

---

## Problème: Permission denied

### Solution:

```bash
# Rendre les scripts exécutables:
chmod +x app.py test.py install.sh run.sh

# Vérifier les permissions des dossiers:
chmod 755 data logs config
```

---

## Problème: Module 'aiohttp' not found

### Solution:

```bash
# Réinstaller les dépendances:
source venv/bin/activate
pip install -r requirements.txt

# Ou:
bash install.sh
```

---

## Problème: Database locked

### Cause:
Deux instances tournent en même temps.

### Solution:

```bash
# Trouver les processus:
ps aux | grep app.py

# Arrêter les processus:
pkill -f app.py

# Ou tuer un processus spécifique:
kill <PID>

# Puis relancer:
bash run.sh
```

---

## Commandes de diagnostic

### Vérifier l'installation complète:

```bash
# 1. Structure des fichiers
ls -la

# 2. Environnement virtuel
ls -la venv/

# 3. Configuration
cat .env

# 4. Dépendances installées
pip list | grep -E "aiohttp|telegram|yaml"

# 5. Logs récents
tail -n 50 logs/control-plane.log

# 6. Base de données
sqlite3 data/history.db "SELECT COUNT(*) FROM checks;"
```

### Tester chaque composant:

```bash
# Test complet:
bash run.sh test

# Test vérification unique:
bash run.sh check

# Test rapport:
bash run.sh report
```

---

## Logs utiles

### Activer le mode DEBUG:

Dans `config/config.yaml`:
```yaml
log_level: "DEBUG"
```

Ou directement dans le code, modifier `app.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Au lieu de INFO
    ...
)
```

### Consulter les logs:

```bash
# Logs en temps réel:
tail -f logs/control-plane.log

# Dernières erreurs:
grep ERROR logs/control-plane.log | tail -20

# Statistiques des checks:
sqlite3 data/history.db "
  SELECT service_name, COUNT(*), 
         SUM(CASE WHEN is_healthy=1 THEN 1 ELSE 0 END) as up_count
  FROM checks 
  GROUP BY service_name;
"
```

---

## Besoin d'aide supplémentaire ?

1. **Consulter les logs détaillés:**
   ```bash
   cat logs/control-plane.log
   ```

2. **Ouvrir une issue sur GitHub** avec:
   - Le message d'erreur complet
   - Le contenu de `.env` (SANS les tokens!)
   - Les logs pertinents
   - Votre configuration système (OS, Python version)

3. **Vérifier la documentation:**
   - README.md
   - QUICKSTART.md
   - env-examples.txt
