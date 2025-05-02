from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..controllers.albums_controller import AlbumsController


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
        
        Datos opcionales:
        - comment: Texto de reseña o comentario sobre el contenido
        - timestamp: Marca de tiempo de la calificación (ISO 8601)
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
