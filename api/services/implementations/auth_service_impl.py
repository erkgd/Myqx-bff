from django.conf import settings
from typing import Dict, Any, Optional
from ..base_service import BaseService
from ...interfaces.user_service_interface import UserServiceInterface
from ...exceptions.api_exceptions import AuthenticationException, ServiceUnavailableException
import logging

logger = logging.getLogger(__name__)

class AuthServiceImpl(BaseService):
    """
    Implementación del servicio de autenticación para comunicarse con el backend.
    Esta clase gestiona todas las operaciones relacionadas con la autenticación de usuarios.
    """
    
    def __init__(self):
        """
        Inicializa el servicio de autenticación con la URL base configurada.
        """
        base_url = getattr(settings, 'AUTH_SERVICE_URL', 'http://localhost:8001/api')
        timeout = getattr(settings, 'SERVICES_TIMEOUT', 30)
        super().__init__(base_url=base_url, timeout=timeout)
        
        # Para la autenticación de Spotify, podemos usar una URL diferente si está configurada
        self.spotify_base_url = getattr(settings, 'SPOTIFY_AUTH_SERVICE_URL', base_url)
        self.spotify_service = None
        if self.spotify_base_url != base_url:
            # Solo creamos una instancia separada si la URL es diferente
            self.spotify_service = BaseService(base_url=self.spotify_base_url, timeout=timeout)
    
    def authenticate(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """
        Autentica un usuario con sus credenciales.
        
        Args:
            credentials: Diccionario con username/email y password
            
        Returns:
            Dict con información del token y usuario autenticado
            
        Raises:
            AuthenticationException: Si las credenciales son inválidas
            ServiceUnavailableException: Si hay problemas de conexión con el backend
        """
        try:
            # Llamada al endpoint de autenticación del backend
            response = self.post('/auth/token/', data=credentials)
            
            # Verificar que la respuesta tenga la estructura esperada
            if not response.get('token') or not response.get('user'):
                raise AuthenticationException("Formato de respuesta de autenticación inválido")
                
            return response
        except Exception as e:
            # Si es un error específico de autenticación, lo propagamos
            if isinstance(e, AuthenticationException):
                raise
                
            # Para otros errores, manejamos de forma genérica
            logger.error(f"Error al autenticar usuario: {str(e)}")
            
            # Determinar el tipo de error para una mejor experiencia de usuario
            if "Connection" in str(e):
                raise ServiceUnavailableException("Servicio de autenticación")
            else:
                raise AuthenticationException("Credenciales inválidas o servicio no disponible")
    
    def verify_token(self, token: str) -> bool:
        """
        Verifica si un token JWT es válido.
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            bool: True si el token es válido, False en caso contrario
        """
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = self.post('/auth/verify/', headers=headers)
            return response.get('valid', False)
        except Exception as e:
            logger.error(f"Error al verificar token: {str(e)}")
            return False
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Actualiza un token JWT usando un refresh token.
        
        Args:
            refresh_token: Token de actualización
            
        Returns:
            Dict con el nuevo token o None si falla
        """
        try:
            response = self.post('/auth/token/refresh/', data={'refresh': refresh_token})
            return response
        except Exception as e:
            logger.error(f"Error al actualizar token: {str(e)}")
            return None
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            user_id: ID del usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña
            
        Returns:
            bool: True si el cambio fue exitoso, False en caso contrario
        """
        try:
            data = {
                'old_password': old_password,
                'new_password': new_password
            }
            self.post(f'/users/{user_id}/change_password/', data=data)
            return True
        except Exception as e:
            logger.error(f"Error al cambiar contraseña: {str(e)}")
            return False
    
    def request_password_reset(self, email: str) -> bool:
        """
        Solicita un restablecimiento de contraseña.
        
        Args:
            email: Correo electrónico del usuario
            
        Returns:
            bool: True si la solicitud fue enviada, False en caso contrario
        """
        try:
            self.post('/auth/password-reset/', data={'email': email})
            return True
        except Exception as e:
            logger.error(f"Error al solicitar restablecimiento de contraseña: {str(e)}")
            return False
            
    def authenticate_with_spotify(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Autentica un usuario utilizando credenciales de Spotify y almacena la información en Neo4j.
        
        Args:
            data: Diccionario con el token de Spotify y opcionalmente
                 información del perfil de usuario
        
        Returns:
            Dict con información del token JWT y usuario autenticado
        
        Raises:
            AuthenticationException: Si el token es inválido
            ServiceUnavailableException: Si hay problemas de conexión con el backend Neo4j
        """
        
        try:
            logger.debug(f"Datos de la petición recibidos: {data}")
            logger.info(f"Iniciando autenticación con Spotify para almacenamiento en Neo4j")
            # Extraer el token de Spotify de los datos recibidos
            spotify_token = None
            if 'spotifyToken' in data:  # Cambiado de spotify_token a spotifyToken
                spotify_token = data['spotifyToken']
            elif 'token' in data and isinstance(data['token'], str):
                spotify_token = data['token']
            elif 'access_token' in data:
                spotify_token = data['access_token']

            if not spotify_token:
                raise AuthenticationException("Falta el token de Spotify")

            # Preparar los datos para enviar al servicio de autenticación
            auth_data = {
                'spotify_token': spotify_token,
                'username': data.get('username'),
                'profile_image': data.get('profilePhoto'),  # Cambiado de profilePhoto
                'spotify_id': data.get('spotifyId'),  # Añadido el ID de Spotify
                'email': data.get('email'),  # Añadido el email
                'use_neo4j': True  # Indicador para el backend de que use Neo4j
            }
            logger.info(f"Enviando datos de autenticación Spotify al backend Neo4j en localhost:8001")
            
            # Llamada al endpoint de autenticación de Spotify en el backend
            response = self.post('/auth/spotify/', data=auth_data)
            
            # Verificar que la respuesta tenga la estructura esperada
            if not response.get('token') or not response.get('user'):
                logger.error(f"Formato de respuesta de autenticación de Spotify inválido: {response}")
                raise AuthenticationException("Formato de respuesta de autenticación inválido")
                
            # Registrar éxito de la autenticación con Neo4j
            logger.info(f"Autenticación con Spotify y Neo4j exitosa para usuario: {response.get('user', {}).get('username', 'unknown')}")
            return response
        except Exception as e:
            # Si es un error específico de autenticación, lo propagamos
            if isinstance(e, AuthenticationException):
                raise
                
            # Para otros errores, manejamos de forma genérica
            logger.error(f"Error al autenticar usuario con Spotify en Neo4j: {str(e)}")
            
            # Determinar el tipo de error para una mejor experiencia de usuario
            if "Connection" in str(e) or "connect" in str(e).lower() or "timeout" in str(e).lower():
                raise ServiceUnavailableException("Servicio de autenticación de Spotify/Neo4j no disponible")
            else:
                raise AuthenticationException("Error en autenticación de Spotify o servicio Neo4j no disponible")