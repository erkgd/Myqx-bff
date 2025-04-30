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
        import sys
        
        try:
            print(f"[AUTH_CONTROLLER] Procesando autenticación Spotify", file=sys.stderr)
            
            # Registramos los datos recibidos para debug (ocultando información sensible)
            safe_data = {k: "***" if k in ['spotifyToken', 'token', 'access_token'] else v 
                        for k, v in spotify_data.items()}
            logger.info(f"Datos de autenticación Spotify recibidos del cliente: {safe_data}")
            
            # Verificar qué tipo de token tenemos
            if 'spotifyToken' in spotify_data:
                print(f"[AUTH_CONTROLLER] Formato de token: 'spotifyToken'", file=sys.stderr)
                token_field = 'spotifyToken'
            elif 'token' in spotify_data:
                print(f"[AUTH_CONTROLLER] Formato de token: 'token'", file=sys.stderr) 
                token_field = 'token'
            elif 'access_token' in spotify_data:
                print(f"[AUTH_CONTROLLER] Formato de token: 'access_token'", file=sys.stderr)
                token_field = 'access_token'
            else:
                print(f"[AUTH_CONTROLLER] ADVERTENCIA: ¡No se encontró un token de Spotify en los datos recibidos!", file=sys.stderr)
                print(f"[AUTH_CONTROLLER] Campos disponibles: {list(spotify_data.keys())}", file=sys.stderr)
                token_field = None
            
            if token_field and spotify_data.get(token_field):
                print(f"[AUTH_CONTROLLER] Longitud del token Spotify: {len(str(spotify_data.get(token_field)))}", file=sys.stderr)
                
            # Usar el servicio para autenticar con Spotify
            print(f"[AUTH_CONTROLLER] Enviando datos al servicio de autenticación...", file=sys.stderr)
            result = self.auth_service.authenticate_with_spotify(spotify_data)
            
            # Registrar el resultado (sin mostrar el token JWT)
            if 'token' in result:
                safe_result = dict(result)
                safe_result['token'] = "***"
                print(f"[AUTH_CONTROLLER] Autenticación exitosa. Usuario: {result.get('user', {}).get('username')}", file=sys.stderr)
            else:
                safe_result = result
                print(f"[AUTH_CONTROLLER] Respuesta sin token. Verificar formato de respuesta.", file=sys.stderr)
                
            logger.info(f"Respuesta del servicio de autenticación Spotify: {safe_result}")
            return Response(result, status=status.HTTP_200_OK)
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
