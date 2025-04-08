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
            safe_data = {k: "***" if k in ['spotifyToken', 'token', 'access_token'] else v 
                        for k, v in spotify_data.items()}
            logger.info(f"Datos de autenticación Spotify recibidos del cliente: {safe_data}")
            
            # Usar el servicio para autenticar con Spotify
            result = self.auth_service.authenticate_with_spotify(spotify_data)
            logger.info(f"Respuesta del servicio de autenticación Spotify: {result}")
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
