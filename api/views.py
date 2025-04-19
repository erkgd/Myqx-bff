from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .controllers.users_controller import UsersController
import datetime


class HealthCheckView(APIView):
    """
    Endpoint para verificar el estado del servicio BFF.
    """
    permission_classes = [AllowAny]  # Sin requisitos de autenticación para health check

    def get(self, request, format=None):
        """
        Retorna el estado actual del servicio BFF.
        """
        data = {
            'status': 'ok',
            'message': 'MyQx BFF service is running',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0',
        }
        return Response(data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        """
        También maneja peticiones POST para health check.
        Útil para aplicaciones móviles que necesitan verificar conectividad.
        """
        # Añadimos información sobre los datos recibidos
        data = {
            'status': 'ok',
            'message': 'MyQx BFF service is running',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0',
            'method': 'POST',
            'received_data': True if request.data else False,
        }
        return Response(data, status=status.HTTP_200_OK)


class AuthTestView(APIView):
    """
    Endpoint para probar la conexión con el servicio de autenticación.
    """
    permission_classes = [AllowAny]  # Sin requisitos de autenticación para pruebas
    
    def get(self, request, format=None):
        """
        Verifica la conexión con el servicio de autenticación.
        """
        # Añadir información útil en la respuesta
        data = {
            'status': 'ok',
            'message': 'Auth service connection test successful',
            'timestamp': datetime.datetime.now().isoformat(),
            'endpoint': '/api/auth/test/',
            'auth_service_available': True,
            'method': request.method,
            'client_ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
        }
        return Response(data, status=status.HTTP_200_OK)


class UserView(APIView):
    """
    Endpoint para operaciones en un usuario específico.
    """
    # Creamos una única instancia del controlador para la vista
    users_controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene un usuario por su ID
        """
        return self.users_controller.get_user(user_id)
    
    def put(self, request, user_id, format=None):
        """
        Actualiza un usuario existente
        """
        return self.users_controller.update_user(user_id, request.data)
    
    def delete(self, request, user_id, format=None):
        """
        Elimina un usuario
        """
        return self.users_controller.delete_user(user_id)


class UsersView(APIView):
    """
    Endpoint para operaciones en la colección de usuarios.
    """
    users_controller = UsersController()
    
    def get(self, request, format=None):
        """
        Obtiene la lista de usuarios, opcionalmente filtrada
        """
        return self.users_controller.get_users(request)
    
    def post(self, request, format=None):
        """
        Crea un nuevo usuario
        """
        return self.users_controller.create_user(request.data)


class AuthView(APIView):
    """
    Endpoint para autenticación de usuarios.
    """
    permission_classes = [AllowAny]  # La autenticación no requiere estar autenticado
    users_controller = UsersController()
    
    def post(self, request, format=None):
        """
        Autentica un usuario con sus credenciales
        """
        return self.users_controller.authenticate(request.data)


class SpotifyAuthView(APIView):
    """
    Endpoint para autenticación de usuarios con Spotify.
    """
    permission_classes = [AllowAny]  # La autenticación no requiere estar autenticado
    
    def post(self, request, format=None):
        """
        Autentica un usuario con sus credenciales de Spotify.
        
        Recibe un token de Spotify obtenido previamente por el cliente Flutter,
        lo procesa y devuelve un token JWT junto con información del usuario.
        """
        import logging
        from .controllers.auth_controller import AuthController
        
        logger = logging.getLogger(__name__)
        
        # Registrar información útil para depuración
        logger.info(f"Recibida petición de autenticación Spotify desde: {request.META.get('REMOTE_ADDR')}")
        logger.info(f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        
        # Verificar que haya datos en la petición
        #if not request.data:
        #    logger.warning("Petición recibida sin datos")
        #    return Response(
        #        {"error": "No se recibieron datos en la petición"}, 
        #        status=status.HTTP_400_BAD_REQUEST
        #    )
        
        # Registrar headers y datos recibidos (excepto información sensible)
        safe_headers = {
            k: v for k, v in request.headers.items() 
            if k.lower() not in ['authorization', 'cookie']
        }
        logger.debug(f"Headers recibidos: {safe_headers}")
        
        safe_data = {
            k: "***" if k in ['spotify_token', 'token', 'access_token'] else v 
            for k, v in request.data.items()
        }
        logger.debug(f"Datos recibidos (sin tokens): {safe_data}")
        
        # Usar el controlador para procesar la autenticación
        auth_controller = AuthController()
        return auth_controller.authenticate_with_spotify(request.data)


class FollowingNetworkView(APIView):
    """
    Endpoint para obtener la red de seguidos de un usuario.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    users_controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene la red de seguidos para un usuario específico.
        """
        try:
            # Usando el método que implementamos en el controlador
            following_network = self.users_controller.get_following_network(user_id)
            
            # Crear una respuesta estructurada
            data = {
                'user_id': user_id,
                'following_network': following_network,
                'count': len(following_network) if following_network else 0,
                'timestamp': datetime.datetime.now().isoformat(),
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # Manejar errores de manera adecuada
            error_data = {
                'error': str(e),
                'user_id': user_id,
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
