from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..controllers.albums_controller import AlbumsController


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
    Endpoint para calificar álbumes y canciones (tracks).
    Este endpoint maneja ambos tipos de contenido y está disponible en:
    - /albums/rate/
    - /ratings/submit/
    """
    permission_classes = [AllowAny]
    albums_controller = AlbumsController()
    
    def post(self, request, format=None):
        """
        Califica un álbum o una canción (track).
        
        El cuerpo de la solicitud debe incluir:
        - albumId o content_id: ID del contenido a calificar
        - contentType: Tipo de contenido ('album' o 'track')
        - rating: Calificación (1-5)
        - userId: ID del usuario que califica
        """
        return self.albums_controller.rate_album(request.data)


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
