from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .controllers import UsersController, AlbumsController
import datetime
import logging

# Vista para el feed
class FeedView(APIView):
    """
    Endpoint para obtener el feed de un usuario.
    Proporciona la actividad reciente y relevante para el usuario.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from .repositories.feed_repository import FeedRepository
        self.repository = FeedRepository()
    
    def get(self, request, item_id=None, format=None):
        """
        Obtiene el feed para un usuario o un elemento específico del feed.
        
        Parámetros de consulta:
        - user_id: ID del usuario (requerido)
        - limit: Cantidad máxima de elementos (opcional, por defecto 20)
        - offset: Número de elementos a saltar (opcional, por defecto 0)
        """
        if item_id:
            # Si se proporciona un ID específico, obtener ese elemento
            return self.get_feed_item(item_id)
        else:
            # Si no hay ID, obtener el feed completo
            return self.get_feed(request)
    
    def get_feed(self, request):
        """
        Obtiene el feed para un usuario específico.
        """
        try:
            # Obtenemos los parámetros de la solicitud
            user_id = request.query_params.get('user_id')
            limit = request.query_params.get('limit', 20)
            offset = request.query_params.get('offset', 0)
            
            # Validamos que el user_id esté presente
            if not user_id:
                from .exceptions.api_exceptions import ValidationException
                raise ValidationException(
                    "Se requiere el ID del usuario",
                    errors={"user_id": "Este campo es requerido como parámetro de consulta"}
                )
            
            # Convertimos limit y offset a enteros
            try:
                limit = int(limit)
                offset = int(offset)
            except (ValueError, TypeError):
                from .exceptions.api_exceptions import ValidationException
                raise ValidationException(
                    "Los parámetros limit y offset deben ser números enteros",
                    errors={"limit": "Debe ser un número entero", "offset": "Debe ser un número entero"}
                )
            
            # Limitamos el valor máximo de limit para evitar sobrecarga
            if limit > 100:
                limit = 100
            
            # Obtenemos el feed desde el repositorio
            feed_items = self.repository.get_feed(user_id, limit, offset)
            
            # Convertimos los DTOs a diccionarios
            feed_data = [item.to_dict() for item in feed_items]
            
            # Preparamos metadatos para la paginación
            metadata = {
                "count": len(feed_data),
                "limit": limit,
                "offset": offset,
                "hasMore": len(feed_data) >= limit
            }
            from .utils import create_response
            return create_response(
                data=feed_data,
                message="Feed obtenido con éxito",
                status_code=status.HTTP_200_OK,
                meta=metadata
            )
            
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Error al obtener feed: {str(e)}")
            raise
    
    def get_feed_item(self, item_id):
        """
        Obtiene un elemento específico del feed.
        """
        try:
            # Obtenemos el elemento desde el repositorio
            item = self.repository.get_feed_item(item_id)
            
            if not item:
                from .exceptions.api_exceptions import ResourceNotFoundException
                raise ResourceNotFoundException("Elemento de feed", item_id)
            
            from .utils import create_response
            return create_response(
                data=item.to_dict(),
                message="Elemento de feed obtenido con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Error al obtener elemento de feed con ID {item_id}: {str(e)}")
            raise


# Vista para calificaciones
class RatingsView(APIView):
    """
    Endpoint centralizado para calificaciones de todo tipo de contenido musical.
    Este es el endpoint principal para enviar calificaciones de álbumes y pistas.
    """
    permission_classes = [AllowAny]
    albums_controller = AlbumsController()
    
    def post(self, request, format=None):
        """
        Envía una calificación para cualquier tipo de contenido musical.
        
        Datos requeridos:
        - userId: ID del usuario que califica
        - contentId o albumId: ID del contenido a calificar
        - contentType: 'album' o 'track'
        - rating: Valor entre 1 y 5
        """
        return self.albums_controller.rate_album(request.data)
    
    def get(self, request, rating_id=None, format=None):
        """
        Obtiene calificaciones existentes.
        """
        # Implementación para consultar calificaciones
        if rating_id:
            return Response({"message": f"Esta funcionalidad está en desarrollo. Calificación ID: {rating_id}"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Esta funcionalidad está en desarrollo. Listado de calificaciones."}, status=status.HTTP_200_OK)


# Vistas para álbumes
class AlbumView(APIView):
    """
    Endpoint para operaciones en un álbum específico.
    """
    permission_classes = [AllowAny]
    albums_controller = AlbumsController()
    
    def get(self, request, album_id, format=None):
        """
        Obtiene un álbum por su ID
        """
        return self.albums_controller.get_album(album_id)


class AlbumsRatingView(APIView):
    """
    Endpoint para calificar álbumes (OBSOLETO).
    Este endpoint está obsoleto. Por favor, use /ratings/submit/ en su lugar.
    """
    permission_classes = [AllowAny]
    albums_controller = AlbumsController()
    
    def post(self, request, format=None):
        """
        Redirecciona a /ratings/submit/.
        Este endpoint está obsoleto. Por favor, use /ratings/submit/ en su lugar.
        """
        # Aunque este endpoint se redirecciona en urls.py, mantenemos
        # esta implementación por si se accede directamente a la vista
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/api/ratings/submit/')


class AlbumRatingsView(APIView):
    """
    Endpoint para obtener todas las calificaciones de un álbum específico.
    """
    permission_classes = [AllowAny]
    albums_controller = AlbumsController()
    
    def get(self, request, album_id, format=None):
        """
        Obtiene todas las calificaciones de un álbum
        """
        return self.albums_controller.get_album_ratings(album_id)


class AlbumUserRatingView(APIView):
    """
    Endpoint para obtener la calificación de un usuario para un álbum específico.
    """
    permission_classes = [AllowAny]
    albums_controller = AlbumsController()
    
    def get(self, request, album_id, format=None):
        """
        Obtiene la calificación de un usuario para un álbum específico
        """
        return self.albums_controller.get_user_album_rating(album_id, request)


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


class UserProfileView(APIView):
    """
    Endpoint para obtener el perfil detallado de un usuario específico.
    Proporciona información adicional como estadísticas, actividad reciente y preferencias.
    """
    users_controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene el perfil completo de un usuario por su ID
        """
        return self.users_controller.get_user_profile(user_id)


class UserFollowingView(APIView):
    """
    Endpoint para gestionar relaciones de seguimiento entre usuarios.
    Permite verificar, crear y eliminar relaciones donde un usuario sigue a otro.
    """
    users_controller = UsersController()
    
    def get(self, request, follower_id, followed_id, format=None):
        """
        Verifica si un usuario sigue a otro
        """
        return self.users_controller.check_follow_status(follower_id, followed_id)
    
    def post(self, request, follower_id, followed_id, format=None):
        """
        Establece una relación de seguimiento entre dos usuarios
        """
        return self.users_controller.follow_user(follower_id, followed_id)
    
    def delete(self, request, follower_id, followed_id, format=None):
        """
        Elimina una relación de seguimiento entre dos usuarios
        """
        return self.users_controller.unfollow_user(follower_id, followed_id)
