from typing import List, Dict, Any, Optional
import logging
import sys
from ...interfaces.feed_service_interface import FeedServiceInterface
from ...services.base_service import BaseService

logger = logging.getLogger(__name__)


class FeedServiceImpl(BaseService, FeedServiceInterface):
    """
    Implementación del servicio de feed que se comunica con el backend.
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la URL base y timeout configurados.
        """
        from django.conf import settings
        base_url = getattr(settings, 'USERS_SERVICE_URL', None)  # Usar la misma URL que el servicio de usuarios
        timeout = getattr(settings, 'SERVICES_TIMEOUT', 30)
        super().__init__(base_url=base_url, timeout=timeout)
    
    def get_feed(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Obtiene el feed para un usuario específico.
        
        Args:
            user_id: ID del usuario
            limit: Cantidad máxima de elementos a devolver
            offset: Número de elementos a saltar (para paginación)
            
        Returns:
            Lista de elementos del feed
        """
        try:
            print(f"[FEED_SERVICE] Obteniendo feed para usuario: {user_id}, limit: {limit}, offset: {offset}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Construir la URL con los parámetros de consulta
            endpoint_url = f"/feed?user_id={user_id}&limit={limit}&offset={offset}"
            print(f"[FEED_SERVICE] Realizando solicitud GET a: {endpoint_url}", file=sys.stderr)
            
            response = self.get(endpoint_url, headers=headers)
            print(f"[FEED_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
            
            # Procesar la respuesta según la estructura devuelta por el backend
            if isinstance(response, dict) and 'items' in response:
                # Si la respuesta tiene una clave 'items', usar esa
                return response.get('items', [])
            elif isinstance(response, dict) and 'feed' in response:
                # Si la respuesta tiene una clave 'feed', usar esa
                return response.get('feed', [])
            elif isinstance(response, list):
                # Si la respuesta ya es una lista, devolverla tal cual
                return response
            else:
                # Si no se reconoce el formato, devolver una lista vacía
                return []
                
        except Exception as e:
            error_msg = f"[FEED_SERVICE] Error al obtener feed para usuario {user_id}: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return []
    
    def get_feed_item(self, item_id: str) -> Dict[str, Any]:
        """
        Obtiene un elemento específico del feed.
        
        Args:
            item_id: ID del elemento
            
        Returns:
            Datos del elemento
        """
        try:
            print(f"[FEED_SERVICE] Obteniendo elemento de feed con ID: {item_id}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Llamada al backend
            endpoint_url = f"/feed/{item_id}"
            print(f"[FEED_SERVICE] Realizando solicitud GET a: {endpoint_url}", file=sys.stderr)
            
            response = self.get(endpoint_url, headers=headers)
            print(f"[FEED_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
            
            if isinstance(response, dict):
                return response
            else:
                return {}
                
        except Exception as e:
            error_msg = f"[FEED_SERVICE] Error al obtener elemento de feed con ID {item_id}: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return {}
            
    def _handle_error(self, message: str, exception: Exception) -> None:
        """
        Método auxiliar para manejar errores de manera consistente.
        
        Args:
            message: Mensaje descriptivo del error
            exception: Excepción capturada
        """
        logger.error(f"{message}: {str(exception)}")
