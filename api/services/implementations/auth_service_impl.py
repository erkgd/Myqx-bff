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
        import sys
        
        try:
            print(f"[AUTH_SERVICE] ************** AUTENTICACIÓN SPOTIFY **************", file=sys.stderr)
            print(f"[AUTH_SERVICE] Iniciando procesamiento de datos en servicio", file=sys.stderr)
            print(f"[AUTH_SERVICE] Campos recibidos: {list(data.keys())}", file=sys.stderr)
            
            logger.debug(f"Datos de la petición recibidos: {data}")
            logger.info(f"Iniciando autenticación con Spotify para almacenamiento en Neo4j")
            
            # Extraer el token de Spotify de los datos recibidos
            spotify_token = None
            token_source = None
            
            if 'spotifyToken' in data:  # Cambiado de spotify_token a spotifyToken
                spotify_token = data['spotifyToken']
                token_source = 'spotifyToken'
                print(f"[AUTH_SERVICE] Token encontrado en campo 'spotifyToken'", file=sys.stderr)
            elif 'token' in data and isinstance(data['token'], str):
                spotify_token = data['token']
                token_source = 'token'
                print(f"[AUTH_SERVICE] Token encontrado en campo 'token'", file=sys.stderr)
            elif 'access_token' in data:
                spotify_token = data['access_token']
                token_source = 'access_token'
                print(f"[AUTH_SERVICE] Token encontrado en campo 'access_token'", file=sys.stderr)

            if not spotify_token:
                print(f"[AUTH_SERVICE] ERROR: No se encontró un token de Spotify válido", file=sys.stderr)
                print(f"[AUTH_SERVICE] Campos disponibles: {list(data.keys())}", file=sys.stderr)
                if 'token' in data:
                    print(f"[AUTH_SERVICE] Tipo de dato en 'token': {type(data['token'])}", file=sys.stderr)
                raise AuthenticationException("Falta el token de Spotify")
            print(f"[AUTH_SERVICE] Token encontrado en campo '{token_source}' (longitud: {len(str(spotify_token))})", file=sys.stderr)            # Preparar los datos para enviar al servicio de autenticación
            # Mantener los nombres de campos originales tal como vienen del frontend
            auth_data = {
                'spotifyToken': spotify_token,  # Mantener el formato original (spotifyToken en lugar de spotify_token)
                'username': data.get('username'),
                'profilePhoto': data.get('profilePhoto'),  # Mantener como profilePhoto (no transformar)
                # También enviar como profileImage para compatibilidad con posibles diferentes nombres en el backend
                'profileImage': data.get('profilePhoto'),  # Añadido para garantizar compatibilidad
                'spotifyId': data.get('spotifyId'),  # Mantener como spotifyId (no transformar)
                'email': data.get('email'),
                'use_neo4j': True  # Este es el único campo adicional que añadimos
            }
            
            # Verificar si hay campos nulos o vacíos y convertirlos a None
            for key, value in list(auth_data.items()):
                if value == "" or (isinstance(value, str) and not value.strip()):
                    print(f"[AUTH_SERVICE] Advertencia: Campo '{key}' tiene valor vacío, estableciendo a None", file=sys.stderr)
                    auth_data[key] = None
            
            # Importar json para formatear la salida
            import json
            print(f"[AUTH_SERVICE] Auth data serializada: {json.dumps(auth_data, default=str, indent=2)}", file=sys.stderr)
            
            print(f"[AUTH_SERVICE] Datos para enviar al backend:", file=sys.stderr)
            for key, value in auth_data.items():
                if key != 'spotify_token':
                    print(f"[AUTH_SERVICE] - {key}: {value}", file=sys.stderr)
                else:
                    print(f"[AUTH_SERVICE] - {key}: ***token***", file=sys.stderr)
            logger.info(f"Enviando datos de autenticación Spotify al backend Neo4j en localhost:8001")
            print(f"[AUTH_SERVICE] Preparándose para enviar solicitud al backend...", file=sys.stderr)            # Llamada al endpoint de autenticación de Spotify en el backend
            # Definir posibles endpoints a probar (en orden de preferencia)
            endpoints = ['/auth/spotify/', '/spotify/']
            response = None
            last_error = None
            
            # Probar con cada endpoint hasta que uno funcione
            for current_endpoint in endpoints:
                print(f"[AUTH_SERVICE] Intentando con endpoint: {current_endpoint}", file=sys.stderr)
                print(f"[AUTH_SERVICE] URL completa a la que se envía la solicitud: {self.base_url}{current_endpoint}", file=sys.stderr)
                
                try:
                    print(f"[AUTH_SERVICE] Enviando datos con los nombres de campos exactos del frontend", file=sys.stderr)
                    response = self.post(current_endpoint, data=auth_data)
                    print(f"[AUTH_SERVICE] ¡ÉXITO! Respuesta recibida del backend usando endpoint: {current_endpoint}", file=sys.stderr)
                    print(f"[AUTH_SERVICE] Campos en la respuesta: {list(response.keys() if isinstance(response, dict) else [])}", file=sys.stderr)
                    # Si llegamos aquí, la solicitud fue exitosa, no necesitamos probar más endpoints
                    break
                    
                except Exception as e:
                    last_error = e
                    print(f"[AUTH_SERVICE] ERROR al usar endpoint {current_endpoint}: {str(e)}", file=sys.stderr)
                    print(f"[AUTH_SERVICE] Tipo de error: {e.__class__.__name__}", file=sys.stderr)
                    
                    # Capturar y mostrar detalles específicos de errores HTTP
                    if hasattr(e, 'response') and e.response:
                        status_code = e.response.status_code if hasattr(e.response, 'status_code') else 'Unknown'
                        print(f"[AUTH_SERVICE] Código de estado: {status_code}", file=sys.stderr)
                        
                        # Para errores 422 (Unprocessable Content), intentar obtener detalles de validación
                        if hasattr(e.response, 'status_code') and e.response.status_code == 422:
                            print(f"[AUTH_SERVICE] ERROR 422: Contenido no procesable - Problema de validación", file=sys.stderr)
                            try:
                                error_detail = e.response.json() if hasattr(e.response, 'json') else {}
                                print(f"[AUTH_SERVICE] Detalles de validación: {error_detail}", file=sys.stderr)
                            except Exception:
                                pass
                        
                        # Mostrar el texto de respuesta completo
                        if hasattr(e.response, 'text'):
                            print(f"[AUTH_SERVICE] Respuesta del servidor: {e.response.text}", file=sys.stderr)
                    
                    print(f"[AUTH_SERVICE] Probando con el siguiente endpoint (si está disponible)...", file=sys.stderr)
                    # Continuamos con el siguiente endpoint
            
            # Si ningún endpoint funcionó, lanzamos el último error que obtuvimos
            if response is None:
                print(f"[AUTH_SERVICE] TODOS LOS ENDPOINTS FALLARON. Último error: {last_error}", file=sys.stderr)
                raise last_error
              # Verificar que la respuesta tenga la estructura esperada
            if response is None:
                print(f"[AUTH_SERVICE] No se recibió respuesta válida de ningún endpoint", file=sys.stderr)
                raise AuthenticationException("No se pudo conectar con el servicio de autenticación")
                
            if not response.get('token') or not response.get('user'):
                logger.error(f"Formato de respuesta de autenticación de Spotify inválido: {response}")
                print(f"[AUTH_SERVICE] ERROR: La respuesta no tiene los campos esperados (token, user)", file=sys.stderr)
                print(f"[AUTH_SERVICE] Respuesta recibida: {response}", file=sys.stderr)
                
                # Intentar extraer un mensaje de error específico
                error_message = "Formato de respuesta de autenticación inválido"
                if isinstance(response, dict):
                    if 'error' in response:
                        error_message = f"Error: {response['error']}"
                    elif 'message' in response:
                        error_message = f"Error: {response['message']}"
                    elif 'detail' in response:
                        error_message = f"Error: {response['detail']}"
                
                raise AuthenticationException(error_message)
              # Registrar éxito de la autenticación con Neo4j
            username = response.get('user', {}).get('username', 'unknown')
            user_id = response.get('user', {}).get('id', 'unknown') or response.get('user', {}).get('userId', 'unknown')
            print(f"[AUTH_SERVICE] Autenticación exitosa para usuario: {username} (ID: {user_id})", file=sys.stderr)
            print(f"[AUTH_SERVICE] Campos en el objeto usuario: {list(response.get('user', {}).keys())}", file=sys.stderr)
            
            # Normalizar los campos de la respuesta para mantener consistencia con el frontend
            if 'user' in response:
                user_data = response['user']
                
                # Asegurar que tanto profilePhoto como profileImage estén presentes en la respuesta
                profile_image = user_data.get('profileImage', user_data.get('profilePhoto'))
                profile_photo = user_data.get('profilePhoto', user_data.get('profileImage'))
                
                if profile_image:
                    user_data['profileImage'] = profile_image
                if profile_photo:
                    user_data['profilePhoto'] = profile_photo
                
                print(f"[AUTH_SERVICE] Normalización de campos de respuesta completada", file=sys.stderr)
            
            print(f"[AUTH_SERVICE] *************************************************", file=sys.stderr)
            
            logger.info(f"Autenticación con Spotify y Neo4j exitosa para usuario: {username}")
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
            elif "422" in str(e):
                # Error de validación de datos
                error_msg = "Los datos de Spotify no tienen el formato esperado por el servidor"
                # Intentar extraer un mensaje de error más específico
                if hasattr(e, 'response') and hasattr(e.response, 'text'):
                    try:
                        import json
                        error_data = json.loads(e.response.text)
                        if 'detail' in error_data:
                            error_msg = f"Error de validación: {error_data['detail']}"
                        elif 'message' in error_data:
                            error_msg = f"Error de validación: {error_data['message']}"
                    except:
                        pass
                logger.error(f"Error de validación 422: {error_msg}")
                raise AuthenticationException(error_msg)
            else:
                raise AuthenticationException("Error en autenticación de Spotify o servicio Neo4j no disponible")