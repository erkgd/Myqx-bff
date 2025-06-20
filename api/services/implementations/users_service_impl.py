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
        
        # Usar print para depuración directa
        import sys
        print("="*50, file=sys.stderr)
        print(f"ENTRANDO A get_following_network PARA USUARIO {user_id}", file=sys.stderr)
        print("="*50, file=sys.stderr)

        try:
            # Preparamos headers para la solicitud
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Log para inspeccionar los headers enviados
            logger.info(f"[FOLLOWING_NETWORK] Headers enviados en la solicitud: {headers}")
            print(f"[FOLLOWING_NETWORK] Headers enviados en la solicitud: {headers}", file=sys.stderr)            # Usamos directamente la URL que sabemos que funciona
            endpoint_url = f'/{user_id}/following_network/'
            full_url = f"{self.base_url}{endpoint_url}"
            
            # Registramos la URL para depuración
            print(f"[FOLLOWING_NETWORK] Base URL: {self.base_url}", file=sys.stderr)
            print(f"[FOLLOWING_NETWORK] Usando endpoint: {endpoint_url}", file=sys.stderr)
            print(f"[FOLLOWING_NETWORK] URL completa: {full_url}", file=sys.stderr)
            
            # Realizamos la solicitud al endpoint
            print(f"[FOLLOWING_NETWORK] Realizando solicitud GET a {endpoint_url}", file=sys.stderr)
            response = self.get(endpoint_url, headers=headers)# --------------- PROCESAMIENTO DE RESPUESTA ---------------
            # Registrar la respuesta para depuración
            print(f"[FOLLOWING_NETWORK] Tipo de respuesta: {type(response)}", file=sys.stderr)
            print(f"[FOLLOWING_NETWORK] Respuesta del endpoint following_network: {response}", file=sys.stderr)
            
            # Verificación explícita para la clave 'network'
            network_data = None
            
            # Si es un diccionario, buscamos la clave 'network'
            if isinstance(response, dict):
                print(f"[FOLLOWING_NETWORK] Respuesta es un diccionario con claves: {response.keys()}", file=sys.stderr)
                
                # CASO 1: Clave 'network' directa
                if 'network' in response:
                    network_size = len(response.get('network', []))
                    print(f"[FOLLOWING_NETWORK] ¡ENCONTRADA la clave 'network' con {network_size} elementos!", file=sys.stderr)
                    network_data = response.get('network')
                    print(f"[FOLLOWING_NETWORK] Contenido de network_data: {network_data}", file=sys.stderr)
                
                # CASO 2: Otras claves comunes
                elif 'data' in response and isinstance(response.get('data'), list):
                    print(f"[FOLLOWING_NETWORK] Usando clave 'data'", file=sys.stderr)
                    network_data = response.get('data')
                elif 'results' in response and isinstance(response.get('results'), list):
                    print(f"[FOLLOWING_NETWORK] Usando clave 'results'", file=sys.stderr)
                    network_data = response.get('results')
                elif 'users' in response and isinstance(response.get('users'), list):
                    print(f"[FOLLOWING_NETWORK] Usando clave 'users'", file=sys.stderr)
                    network_data = response.get('users')
                    
            # CASO 3: Si la respuesta ya es una lista
            elif isinstance(response, list):
                print(f"[FOLLOWING_NETWORK] La respuesta ya es una lista", file=sys.stderr)
                network_data = response
            
            # CASO 4: Respuesta inválida o vacía
            if network_data is None:
                print(f"[FOLLOWING_NETWORK] No se encontraron datos válidos en la respuesta", file=sys.stderr)
                network_data = []
            
            # Resultado final
            print(f"[FOLLOWING_NETWORK] Devolviendo {len(network_data)} elementos de la red", file=sys.stderr)
            return network_data
        except Exception as e:
            error_msg = f"[FOLLOWING_NETWORK] Error al obtener la red de seguidos para el usuario {user_id}: {str(e)}"
            print(error_msg, file=sys.stderr)
            print(f"[FOLLOWING_NETWORK] Tipo de excepción: {type(e).__name__}", file=sys.stderr)
            self._handle_error(error_msg, e)
            
            import traceback
            print(f"[FOLLOWING_NETWORK] Traceback completo:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            
            # Para un mejor manejo del error, retornamos una lista vacía
            return []

    def follow_user(self, follower_id: str, followed_id: str) -> bool:
        """
        Establece una relación de seguimiento entre dos usuarios.

        Args:
            follower_id: ID del usuario que hace el seguimiento
            followed_id: ID del usuario que es seguido

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        import logging
        import sys
        logger = logging.getLogger(__name__)
        
        print(f"[FOLLOW_USER] Intentando establecer relación: {follower_id} siguiendo a {followed_id}", file=sys.stderr)
        
        try:
            # Preparamos headers para la solicitud
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Preparamos datos para enviar
            data = {
                'follower_id': follower_id,
                'followed_id': followed_id
            }
            
            # Endpoint para la solicitud
            endpoint_url = '/users/following/'
            
            # Realizamos la solicitud POST
            print(f"[FOLLOW_USER] Realizando solicitud POST a {endpoint_url}", file=sys.stderr)
            response = self.post(endpoint_url, data=data, headers=headers)
            
            # Verificamos la respuesta
            print(f"[FOLLOW_USER] Respuesta: {response}", file=sys.stderr)
            
            # Asumimos que si la respuesta no es None, la operación fue exitosa
            return response is not None and isinstance(response, dict)
            
        except Exception as e:
            error_msg = f"[FOLLOW_USER] Error al establecer relación de seguimiento: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return False
    
    def unfollow_user(self, follower_id: str, followed_id: str) -> bool:
        """
        Elimina una relación de seguimiento entre dos usuarios.

        Args:
            follower_id: ID del usuario que hace el seguimiento
            followed_id: ID del usuario que es seguido

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario
        """
        import logging
        import sys
        logger = logging.getLogger(__name__)
        
        print(f"[UNFOLLOW_USER] Intentando eliminar relación: {follower_id} siguiendo a {followed_id}", file=sys.stderr)
        
        try:
            # Preparamos headers para la solicitud
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Endpoint para la solicitud
            endpoint_url = f'/users/following/{follower_id}/{followed_id}'
            
            # Realizamos la solicitud DELETE
            print(f"[UNFOLLOW_USER] Realizando solicitud DELETE a {endpoint_url}", file=sys.stderr)
            response = self.delete(endpoint_url, headers=headers)
            
            # Asumimos que si no hay excepciones, la operación fue exitosa
            return True
            
        except Exception as e:
            error_msg = f"[UNFOLLOW_USER] Error al eliminar relación de seguimiento: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return False
    
    def is_following(self, follower_id: str, followed_id: str) -> bool:
        """
        Verifica si un usuario sigue a otro.

        Args:
            follower_id: ID del usuario que podría estar siguiendo
            followed_id: ID del usuario que podría estar siendo seguido

        Returns:
            bool: True si existe la relación de seguimiento, False en caso contrario
        """
        import logging
        import sys
        logger = logging.getLogger(__name__)
        
        print(f"[IS_FOLLOWING] Verificando si {follower_id} sigue a {followed_id}", file=sys.stderr)
        
        try:
            # Preparamos headers para la solicitud
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Endpoint para la solicitud
            endpoint_url = f'/users/following/{follower_id}/{followed_id}'
            
            # Realizamos la solicitud GET
            print(f"[IS_FOLLOWING] Realizando solicitud GET a {endpoint_url}", file=sys.stderr)
            response = self.get(endpoint_url, headers=headers)
              # Verificamos la respuesta
            print(f"[IS_FOLLOWING] Respuesta: {response}", file=sys.stderr)
            
            # Comprobamos primero si existe el campo 'isFollowing' (camelCase)
            if isinstance(response, dict) and 'isFollowing' in response:
                result = response.get('isFollowing', False)
                print(f"[IS_FOLLOWING] Campo 'isFollowing' encontrado con valor: {result}", file=sys.stderr)
                return result
                
            # Alternativamente buscamos 'is_following' (snake_case)
            if isinstance(response, dict) and 'is_following' in response:
                result = response.get('is_following', False)
                print(f"[IS_FOLLOWING] Campo 'is_following' encontrado con valor: {result}", file=sys.stderr)
                return result
            
            # Si no encontramos ningún campo específico, asumimos que NO existe la relación
            print(f"[IS_FOLLOWING] No se encontró campo de seguimiento, asumiendo FALSE", file=sys.stderr)
            return False
            
        except Exception as e:
            # Si hay un error, asumimos que no existe la relación
            error_msg = f"[IS_FOLLOWING] Error al verificar relación de seguimiento: {str(e)}"
            print(error_msg, file=sys.stderr)
            self._handle_error(error_msg, e)
            return False

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