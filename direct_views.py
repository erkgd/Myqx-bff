from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from api.repositories.feed_repository import FeedRepository
from api.utils import create_response


class DirectFeedView(APIView):
    """
    Vista directa para el feed sin el prefijo /api/.
    """
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = FeedRepository()
    
    def get(self, request, format=None):
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
                return Response(
                    {"error": "Se requiere el ID del usuario", "details": "El parámetro user_id es obligatorio."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convertimos limit y offset a enteros
            try:
                limit = int(limit)
                offset = int(offset)
            except (ValueError, TypeError):
                return Response(
                    {"error": "Parámetros inválidos", "details": "limit y offset deben ser números enteros."},
                    status=status.HTTP_400_BAD_REQUEST
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
            
            return create_response(
                data=feed_data,
                message="Feed obtenido con éxito",
                status_code=status.HTTP_200_OK,
                metadata=metadata
            )
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception(f"Error al obtener feed: {str(e)}")
            return Response(
                {"error": "Error interno", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
