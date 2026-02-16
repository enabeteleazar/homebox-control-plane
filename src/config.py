"""
Configuration du Control Plane
Charge les paramètres depuis les variables d'environnement et config.yaml
"""

import os
import yaml
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()


class Config:
    """Classe de configuration centralisée"""
    
    def __init__(self, config_file: str = "config/config.yaml"):
        self.config_file = config_file
        self._load_config()
    
    def _load_config(self):
        """Charger la configuration depuis le fichier YAML et l'environnement"""
        
        # Configuration par défaut
        defaults = {
            'check_interval': 300,  # 5 minutes
            'check_timeout': 10,    # 10 secondes
            'max_response_time': 5.0,  # 5 secondes
            'retry_attempts': 3,
            'retry_delay': 30,
            'database_path': 'data/history.db'
        }
        
        # Charger depuis YAML si le fichier existe
        config_path = Path(self.config_file)
        if config_path.exists():
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f) or {}
                defaults.update(yaml_config)
        
        # Variables obligatoires depuis l'environnement
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.telegram_bot_token or not self.telegram_chat_id:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID doivent être définis "
                "dans les variables d'environnement ou le fichier .env"
            )
        
        # URLs des services
        self.homebox_url = os.getenv('HOMEBOX_URL', defaults.get('homebox_url', 'http://localhost:7745'))
        self.neron_url = os.getenv('NERON_URL', defaults.get('neron_url', 'http://localhost:3000'))
        
        # Paramètres de vérification
        self.check_interval = int(os.getenv('CHECK_INTERVAL', defaults['check_interval']))
        self.check_timeout = int(os.getenv('CHECK_TIMEOUT', defaults['check_timeout']))
        self.max_response_time = float(os.getenv('MAX_RESPONSE_TIME', defaults['max_response_time']))
        self.retry_attempts = int(os.getenv('RETRY_ATTEMPTS', defaults['retry_attempts']))
        self.retry_delay = int(os.getenv('RETRY_DELAY', defaults['retry_delay']))
        
        # Base de données
        self.database_path = os.getenv('DATABASE_PATH', defaults['database_path'])
        
        # Créer le dossier data si nécessaire
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
    
    def __repr__(self):
        return (
            f"Config(homebox={self.homebox_url}, "
            f"neron={self.neron_url}, "
            f"interval={self.check_interval}s)"
        )
