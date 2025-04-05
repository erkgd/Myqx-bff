import requests
from rest_framework.response import Response
from rest_framework import status
import logging
import uuid
from datetime import datetime, timedelta
import json
from django.conf import settings
from ..services.implementations.auth_service_impl import AuthServiceImpl
from ..exceptions.api_exceptions import AuthenticationException, ServiceUnavailableException

logger = logging.getLogger(__name__)

class AuthController:
    """
    Controlador que maneja las operaciones de autenticación.
    """
    
    def __init__(self):
        """
        Inicializa el controlador con el servicio de autenticación.
        """
        self.auth_service = AuthServiceImpl()
        
    def authenticate(self, credentials):
        """
        Autentica un usuario con sus credenciales.
        
        Args:
            credentials: Dict con username/email y password
            
        Returns:
            Response: Respuesta HTTP con el token y usuario o error
        """
        try:
            result = self.auth_service.authenticate(credentials)
            return Response(result, status=status.HTTP_200_OK)
        except AuthenticationException as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ServiceUnavailableException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Error inesperado en autenticación: {str(e)}")
            return Response(
                {"error": "Error interno del servidor"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def authenticate_with_spotify(self, spotify_data):
        """
        Autentica un usuario usando Spotify como proveedor de identidad.
        Recibe el token de Spotify obtenido por el cliente y lo reenvía al backend.
        
        Args:
            spotify_data: Dict con el token de Spotify y opcionalmente
                 información del perfil de usuario
            
        Returns:
            Response: Respuesta HTTP con el token JWT y usuario o error
        """
        try:
            # Registramos los datos recibidos para debug (ocultando información sensible)
            safe_data = {k: "***" if k in ['spotify_token', 'token', 'access_token'] else v 
                        for k, v in spotify_data.items()}
            logger.info(f"Datos de autenticación Spotify recibidos del cliente: {safe_data}")
            
            # Si el backend está disponible, usar el servicio para autenticar
            if not settings.DEBUG:
                try:
                    result = self.auth_service.authenticate_with_spotify(spotify_data)
                    return Response(result, status=status.HTTP_200_OK)
                except Exception as e:
                    # Si hay un error de conexión con el backend, caemos al modo simulado en DEBUG
                    if not isinstance(e, (AuthenticationException, ServiceUnavailableException)):
                        raise
                    logger.warning(f"Usando modo simulado debido a error: {str(e)}")
            
            # Si estamos en modo DEBUG o hubo un error con el backend, usar simulación
            if settings.DEBUG:
                return self._simulate_spotify_auth(spotify_data)
            else:
                # Si no estamos en DEBUG y llegamos aquí, propagar el error original
                raise
                
        except AuthenticationException as e:
            logger.warning(f"Error de autenticación con Spotify: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ServiceUnavailableException as e:
            logger.error(f"Servicio no disponible: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            logger.error(f"Error inesperado en autenticación con Spotify: {str(e)}")
            return Response(
                {"error": "Error interno del servidor"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def _simulate_spotify_auth(self, spotify_data):
        """
        Simula la autenticación con Spotify para desarrollo.
        
        Args:
            spotify_data: Dict con los datos de Spotify
            
        Returns:
            Response: Respuesta HTTP simulada
        """
        logger.info("Utilizando autenticación simulada con Spotify")
        
        # Registrar datos recibidos para debug
        logger.info(f"Formato de los datos recibidos: {type(spotify_data)}")
        for key, value in spotify_data.items():
            logger.info(f"Campo '{key}': tipo {type(value)}")
        
        # 1. Validar que el request tenga el token de Spotify
        spotify_token = None
        
        # Buscar el token en diferentes ubicaciones posibles
        if 'spotify_token' in spotify_data:
            spotify_token = spotify_data['spotify_token']
        elif 'token' in spotify_data and isinstance(spotify_data['token'], str):
            spotify_token = spotify_data['token']
        elif 'access_token' in spotify_data:
            spotify_token = spotify_data['access_token']
        elif 'token' in spotify_data and isinstance(spotify_data['token'], dict) and 'access_token' in spotify_data['token']:
            spotify_token = spotify_data['token']['access_token']
            
        # Si no encontramos un token, usar uno simulado
        if not spotify_token:
            logger.warning("No se encontró token de Spotify. Usando token simulado para desarrollo.")
            spotify_token = "mock_spotify_token_for_development"
        
        # Generar datos de usuario simulados
        user_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Extraer datos del perfil que el cliente pueda haber enviado
        profile_name = spotify_data.get('display_name', spotify_data.get('username', f"User_{user_id[:8]}"))
        profile_email = spotify_data.get('email', f"user_{user_id[:8]}@example.com")
        profile_image = spotify_data.get('profile_image', spotify_data.get('profile_url', None))
        
        # MODIFICACIÓN: Simplificar formato de token para que sea compatible con el cliente Flutter
        # Opción 1: Token como cadena simple (versión simplificada)
        access_token = f"myqx_access_token_{user_id[:8]}"
        refresh_token = f"myqx_refresh_token_{user_id[:8]}"
        
        response_data = {
            # Enviar token de dos formas para mayor compatibilidad con diferentes
            # implementaciones del cliente
            "token": access_token,  # Formato simple como string
            "access_token": access_token,  # Alternativa común
            "refresh_token": refresh_token,
            "token_data": {  # Formato completo con datos adicionales
                "access": access_token,
                "refresh": refresh_token,
                "access_expires": (now + timedelta(hours=1)).isoformat(),
                "refresh_expires": (now + timedelta(days=7)).isoformat()
            },
            "user": {
                "id": user_id,
                "username": profile_name,
                "email": profile_email,
                "profile_image": profile_image,
                "spotify_connected": True,
                "auth_provider": "spotify",
                "created_at": now.isoformat(),
                "last_login": now.isoformat()
            }
        }
        
        logger.info(f"Autenticación Spotify simulada exitosa para usuario: {response_data['user']['username']}")
        logger.info(f"Formato de respuesta: {json.dumps(response_data, indent=2)}")
        return Response(response_data, status=status.HTTP_200_OK)