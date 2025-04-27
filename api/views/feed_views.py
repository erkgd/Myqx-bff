from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class FeedView(APIView):
    """
    Endpoint para obtener el feed de un usuario.
    Proporciona la actividad reciente y relevante para el usuario.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from ..repositories.feed_repository import FeedRepository
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
                from ..exceptions.api_exceptions import ValidationException
                raise ValidationException(
                    "Se requiere el ID del usuario",
                    errors={"user_id": "Este campo es requerido como parámetro de consulta"}
                )
            
            # Convertimos limit y offset a enteros
            try:
                limit = int(limit)
                offset = int(offset)
            except (ValueError, TypeError):
                from ..exceptions.api_exceptions import ValidationException
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
              from ..utils import create_response
            return create_response(
                data=feed_data,
                message="Feed obtenido con éxito",
                status_code=status.HTTP_200_OK,
                meta=metadata
            )
            
        except Exception as e:
            import logging
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
                from ..exceptions.api_exceptions import ResourceNotFoundException
                raise ResourceNotFoundException("Elemento de feed", item_id)
            
            from ..utils import create_response
            return create_response(
                data=item.to_dict(),
                message="Elemento de feed obtenido con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception(f"Error al obtener elemento de feed con ID {item_id}: {str(e)}")
            raise
