"""
Neron Service Checker
Vérifie l’état et la disponibilité de Neron
"""

import aiohttp
import asyncio
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class NeronChecker:
    """Vérificateur pour le service Neron"""

    def __init__(self, url: str, timeout: int = 10, max_response_time: float = 5.0):
        self.name = "Neron"
        self.url = url.rstrip('/')
        self.timeout = timeout
        self.max_response_time = max_response_time

        # Essayer différents endpoints possibles pour le health check
        self.health_endpoints = [
            f"{self.url}/health",
            f"{self.url}/api/health",
            f"{self.url}/status",
            f"{self.url}/",  # Fallback sur la racine
        ]

        logger.info(f"Neron checker initialisé: {self.url}")

    async def check(self):
        """Effectuer la vérification de santé"""
        from app import ServiceStatus  # Import local pour éviter la circularité

        start_time = time.time()

        try:
            # Timeout pour la requête HTTP
            timeout = aiohttp.ClientTimeout(total=self.timeout)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                last_error = None

                for endpoint in self.health_endpoints:
                    try:
                        start_time = time.time()
                        async with session.get(endpoint) as response:
                            response_time = time.time() - start_time

                            if response.status == 200:
                                # Vérifier le contenu de la réponse si c'est du JSON
                                try:
                                    data = await response.json()
                                    # Adapter selon la structure de réponse de Neron
                                    is_healthy = data.get('status') == 'ok' or data.get('healthy', True)
                                except Exception:
                                    # Si pas de JSON ou structure différente, considérer comme sain si status 200
                                    is_healthy = True

                                logger.debug(f"Neron accessible via {endpoint}")

                                return ServiceStatus(
                                    service_name=self.name,
                                    is_healthy=is_healthy,
                                    response_time=response_time,
                                    status_code=response.status
                                )

                            elif response.status in [404, 405]:
                                # Endpoint n'existe pas, essayer le suivant
                                continue

                            else:
                                # Autre erreur HTTP
                                last_error = f"HTTP {response.status}"
                                continue

                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        # Essayer le prochain endpoint
                        continue

                # Si on arrive ici, aucun endpoint n'a fonctionné
                response_time = time.time() - start_time
                return ServiceStatus(
                    service_name=self.name,
                    is_healthy=False,
                    response_time=response_time,
                    error=last_error or "Aucun endpoint accessible"
                )

        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            logger.error(f"Timeout lors de la vérification de {self.name}")
            return ServiceStatus(
                service_name=self.name,
                is_healthy=False,
                response_time=response_time,
                error=f"Timeout après {self.timeout}s"
            )

        except aiohttp.ClientError as e:
            response_time = time.time() - start_time
            logger.error(f"Erreur de connexion à {self.name}: {e}")
            return ServiceStatus(
                service_name=self.name,
                is_healthy=False,
                response_time=response_time,
                error=f"Connexion impossible: {str(e)}"
            )

        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Erreur inattendue lors de la vérification de {self.name}: {e}")
            return ServiceStatus(
                service_name=self.name,
                is_healthy=False,
                response_time=response_time,
                error=str(e)
            )
