from typing import List, Dict, Any, Optional
import logging
import sys
from ...interfaces.album_service_interface import AlbumServiceInterface
from ...services.base_service import BaseService

logger = logging.getLogger(__name__)


class AlbumsServiceImpl(BaseService, AlbumServiceInterface):
    """
    Implementación del servicio de álbumes que se comunica con el backend.
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la URL base y timeout configurados.
        """
        from django.conf import settings
        base_url = getattr(settings, 'ALBUMS_SERVICE_URL', settings.USERS_SERVICE_URL)
        timeout = getattr(settings, 'SERVICES_TIMEOUT', 30)
        super().__init__(base_url=base_url, timeout=timeout)
    
    def get_album(self, album_id: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un álbum por su ID.
        
        Args:
            album_id: ID del álbum (puede ser ID de Spotify)
            
        Returns:
            Diccionario con la información del álbum
        """
        try:
            print(f"[ALBUM_SERVICE] Buscando álbum con ID: {album_id}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Llamada al backend
            endpoint_url = f"/albums/{album_id}"
            print(f"[ALBUM_SERVICE] Realizando solicitud GET a: {endpoint_url}", file=sys.stderr)
            
            response = self.get(endpoint_url, headers=headers)
            print(f"[ALBUM_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
            
            return response
        except Exception as e:
            error_msg = f"[ALBUM_SERVICE] Error al obtener información del álbum {album_id}: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return {}
    
    def get_album_ratings(self, album_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las calificaciones de un álbum específico.
        
        Args:
            album_id: ID del álbum
            
        Returns:
            Lista de calificaciones
        """
        try:
            print(f"[ALBUM_SERVICE] Obteniendo calificaciones para álbum ID: {album_id}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Llamada al backend
            endpoint_url = f"/albums/{album_id}/ratings"
            print(f"[ALBUM_SERVICE] Realizando solicitud GET a: {endpoint_url}", file=sys.stderr)
            
            response = self.get(endpoint_url, headers=headers)
            print(f"[ALBUM_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
            
            if isinstance(response, dict) and 'ratings' in response:
                return response.get('ratings', [])
            elif isinstance(response, list):
                return response
            else:
                return []
        except Exception as e:
            error_msg = f"[ALBUM_SERVICE] Error al obtener calificaciones del álbum {album_id}: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return []
      def rate_album(self, rating_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Califica un álbum o canción.
        
        Args:
            rating_data: Datos de la calificación (debe incluir user_id, album_id/content_id, rating)
                         También puede incluir un campo 'comment' opcional para agregar un comentario a la calificación
            
        Returns:
            Información de la calificación guardada
        """
        try:            # Enmascaramos información sensible en los logs pero mostramos la estructura
            safe_data = {**rating_data}
            if 'comment' in safe_data:
                print(f"[ALBUM_SERVICE] Calificación incluye comentario de longitud: {len(str(safe_data['comment']))}", file=sys.stderr)
            
            print(f"[ALBUM_SERVICE] Calificando contenido con datos: {safe_data}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }            # Usar el endpoint centralizado para calificaciones
            endpoint_url = "/ratings/submit"
            
            # Log para saber qué tipo de contenido se está calificando
            content_type = rating_data.get('contentType', 'album')
            print(f"[ALBUM_SERVICE] Calificando contenido de tipo: {content_type}", file=sys.stderr)
            
            print(f"[ALBUM_SERVICE] Realizando solicitud POST a: {endpoint_url}", file=sys.stderr)
            
            response = self.post(endpoint_url, data=rating_data, headers=headers)
            print(f"[ALBUM_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
            
            return response
        except Exception as e:
            error_msg = f"[ALBUM_SERVICE] Error al calificar contenido: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return {}
    
    def get_user_album_rating(self, user_id: str, album_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene la calificación de un usuario para un álbum específico.
        
        Args:
            user_id: ID del usuario
            album_id: ID del álbum
            
        Returns:
            Información de la calificación o None si no existe
        """
        try:
            print(f"[ALBUM_SERVICE] Buscando calificación del usuario {user_id} para álbum {album_id}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Llamada al backend
            endpoint_url = f"/albums/{album_id}/rating"
            endpoint_url_with_user = f"{endpoint_url}?user_id={user_id}"
            print(f"[ALBUM_SERVICE] Realizando solicitud GET a: {endpoint_url_with_user}", file=sys.stderr)
            
            response = self.get(endpoint_url_with_user, headers=headers)
            print(f"[ALBUM_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
            
            return response
        except Exception as e:
            error_msg = f"[ALBUM_SERVICE] Error al obtener calificación: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return None
            
    def _handle_error(self, message: str, exception: Exception) -> None:
        """
        Método auxiliar para manejar errores de manera consistente.
        
        Args:
            message: Mensaje descriptivo del error
            exception: Excepción capturada
        """
        logger.error(f"{message}: {str(exception)}")
