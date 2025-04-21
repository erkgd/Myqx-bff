from django.conf import settings
from typing import Dict, List, Any, Optional
from ..base_service import BaseService
from ...interfaces.user_service_interface import UserServiceInterface

class UsersServiceImpl(BaseService, UserServiceInterface):
    """
    Implementación concreta del servicio de usuarios que implementa la interfaz UserServiceInterface.
    Esta clase se comunica con el backend de usuarios y proporciona métodos para interactuar con él.
    """
    
    def __init__(self):
        # Obtenemos la URL base del servicio desde configuración
        base_url = getattr(settings, 'USERS_SERVICE_URL', 'http://localhost:8001/api')
        super().__init__(base_url=base_url)
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene un usuario por su ID desde el backend.
        
        Args:
            user_id: ID del usuario a obtener
            
        Returns:
            Dict que representa los datos del usuario
        """
        try:
            return self.get(f'/users/{user_id}/')
        except Exception as e:
            # Loggeo de error y manejo específico para el BFF
            self._handle_error(f"Error al obtener usuario con ID {user_id}", e)
            raise
    
    def get_users(self, **params) -> List[Dict[str, Any]]:
        """
        Obtiene una lista de usuarios con filtros opcionales.
        
        Args:
            **params: Parámetros de filtrado opcionales
            
        Returns:
            Lista de diccionarios representando usuarios
        """
        try:
            response = self.get('/users/', params=params)
            # Asumimos que la respuesta tiene una estructura como {'results': [...]}
            return response.get('results', [])
        except Exception as e:
            self._handle_error("Error al obtener lista de usuarios", e)
            raise
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo usuario.
        
        Args:
            user_data: Datos del usuario a crear
            
        Returns:
            Dict con los datos del usuario creado
        """
        try:
            return self.post('/users/', data=user_data)
        except Exception as e:
            self._handle_error("Error al crear usuario", e)
            raise
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un usuario existente.
        
        Args:
            user_id: ID del usuario a actualizar
            user_data: Nuevos datos del usuario
            
        Returns:
            Dict con los datos del usuario actualizado
        """
        try:
            return self.put(f'/users/{user_id}/', data=user_data)
        except Exception as e:
            self._handle_error(f"Error al actualizar usuario con ID {user_id}", e)
            raise
    
    def delete_user(self, user_id: str) -> bool:
        """
        Elimina un usuario.
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        try:
            self.delete(f'/users/{user_id}/')
            return True
        except Exception as e:
            self._handle_error(f"Error al eliminar usuario con ID {user_id}", e)
            return False
    
    def authenticate(self, credentials: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario.
        
        Args:
            credentials: Credenciales del usuario (generalmente email/username y password)
            
        Returns:
            Dict con información del token y usuario o None si la autenticación falla
        """
        try:
            return self.post('/auth/token/', data=credentials)
        except Exception:
            # Para autenticación, no queremos propagar la excepción ya que es un caso de uso común
            return None

    def get_following_network(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene la red de seguidos de un usuario desde el backend.

        Args:
            user_id: ID del usuario

        Returns:
            Lista de diccionarios representando los usuarios seguidos.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Preparamos headers para la solicitud
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Log para inspeccionar los headers enviados
            logger.info(f"Headers enviados en la solicitud: {headers}")
            
            # Log de la URL del endpoint
            endpoint_url = f'/{user_id}/following_network/'
            logger.info(f"URL del endpoint: {endpoint_url}")
            
            # Realizar la solicitud
            response = self.get(endpoint_url, headers=headers)
            
            # Registrar la respuesta para depuración
            logger.info(f"Respuesta del endpoint following_network: {response}")
            
            # Asumimos que la respuesta es una lista de usuarios
            return response if isinstance(response, list) else []
        except Exception as e:
            self._handle_error(f"Error al obtener la red de seguidos para el usuario {user_id}", e)
            # Para un mejor manejo del error, retornamos una lista vacía
            return []

    def _handle_error(self, message: str, exception: Exception) -> None:
        """
        Método auxiliar para manejar errores de manera consistente.
        
        Args:
            message: Mensaje descriptivo del error
            exception: Excepción capturada
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"{message}: {str(exception)}")