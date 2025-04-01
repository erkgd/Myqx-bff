import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class BaseService:
    """
    Clase base para servicios que se comunican con backends externos.
    Un BFF típicamente se comunica con múltiples servicios backend.
    """
    
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        
    def _request(self, method, endpoint, **kwargs):
        """
        Realiza una petición HTTP al servicio backend.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint a llamar (sin incluir base_url)
            **kwargs: Argumentos adicionales para la petición
            
        Returns:
            dict: Respuesta JSON del servicio
        """
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        headers = {**default_headers, **headers}
        
        try:
            logger.info(f"Realizando petición {method} a {url}")
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP al comunicarse con el backend: {str(e)}")
            # Puedes personalizar cómo manejar cada tipo de error aquí
            raise
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexión con el backend: {url}")
            raise
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al conectar con el backend: {url}")
            raise
            
        except Exception as e:
            logger.error(f"Error inesperado al comunicarse con el backend: {str(e)}")
            raise
            
    def get(self, endpoint, **kwargs):
        """Realiza una petición GET"""
        return self._request('GET', endpoint, **kwargs)
        
    def post(self, endpoint, data=None, **kwargs):
        """Realiza una petición POST"""
        return self._request('POST', endpoint, json=data, **kwargs)
        
    def put(self, endpoint, data=None, **kwargs):
        """Realiza una petición PUT"""
        return self._request('PUT', endpoint, json=data, **kwargs)
        
    def delete(self, endpoint, **kwargs):
        """Realiza una petición DELETE"""
        return self._request('DELETE', endpoint, **kwargs)