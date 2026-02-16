"""
Homebox Service Checker
Vérifie l’état et la disponibilité de Homebox
"""

import aiohttp
import asyncio
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class HomeboxChecker:
    """Vérificateur pour le service Homebox"""

    def __init__(self, url: str, timeout: int = 10, max_response_time: float = 5.0):
        self.name = "Homebox"
        self.url = url.rstrip('/')
        self.timeout = timeout
        self.max_response_time = max_response_time
        self.health_endpoint = f"{self.url}/api/v1/status"  # Endpoint de health check

        logger.info(f"Homebox checker initialisé: {self.url}")

    async def check(self):
        """Effectuer la vérification de santé"""
        from app import ServiceStatus  # Import local pour éviter la circularité

        start_time = time.time()

        try:
            # Timeout pour la requête HTTP
            timeout = aiohttp.ClientTimeout(total=self.timeout)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Essayer d'abord l'endpoint de status
                try:
                    async with session.get(self.health_endpoint) as response:
                        response_time = time.time() - start_time

                        if response.status == 200:
                            # Vérifier le contenu de la réponse si c'est du JSON
                            try:
                                data = await response.json()
                                # Homebox retourne généralement {"health": true} ou similaire
                                is_healthy = data.get('health', True)
                            except Exception:
                                # Si pas de JSON, considérer comme sain si status 200
                                is_healthy = True

                            return ServiceStatus(
                                service_name=self.name,
                                is_healthy=is_healthy,
                                response_time=response_time,
                                status_code=response.status
                            )
                        else:
                            return ServiceStatus(
                                service_name=self.name,
                                is_healthy=False,
                                response_time=response_time,
                                status_code=response.status,
                                error=f"HTTP {response.status}"
                            )

                except aiohttp.ClientError:
                    # Si l'endpoint de status n'existe pas, essayer la page d'accueil
                    logger.debug(f"Endpoint {self.health_endpoint} non disponible, essai de l'URL principale")

                    start_time = time.time()
                    async with session.get(self.url) as response:
                        response_time = time.time() - start_time

                        is_healthy = response.status == 200

                        return ServiceStatus(
                            service_name=self.name,
                            is_healthy=is_healthy,
                            response_time=response_time,
                            status_code=response.status,
                            error=None if is_healthy else f"HTTP {response.status}"
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
