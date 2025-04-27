from typing import Dict, Any
from rest_framework import status
from rest_framework.request import Request
from ..repositories.feed_repository import FeedRepository
from ..exceptions.api_exceptions import ResourceNotFoundException, ValidationException
from ..utils import create_response
import logging

logger = logging.getLogger(__name__)


class FeedController:
    """
    Controlador para manejar operaciones relacionadas con el feed.
    """
    
    def __init__(self):
        """
        Constructor del controlador de feed.
        """
        self.repository = FeedRepository()
    
    def get_feed(self, request: Request):
        """
        Obtiene el feed para un usuario específico.
        
        Args:
            request: Objeto Request que contiene los parámetros de consulta
            
        Returns:
            Response: Respuesta HTTP con los elementos del feed o error
        """
        try:
            # Obtenemos los parámetros de la solicitud
            user_id = request.query_params.get('user_id')
            limit = request.query_params.get('limit', 20)
            offset = request.query_params.get('offset', 0)
            
            # Validamos que el user_id esté presente
            if not user_id:
                raise ValidationException(
                    "Se requiere el ID del usuario",
                    errors={"user_id": "Este campo es requerido como parámetro de consulta"}
                )
            
            # Convertimos limit y offset a enteros
            try:
                limit = int(limit)
                offset = int(offset)
            except (ValueError, TypeError):
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
                "hasMore": len(feed_data) >= limit  # Si se devolvieron tantos elementos como el límite, probablemente hay más
            }
              return create_response(
                data=feed_data,
                message="Feed obtenido con éxito",
                status_code=status.HTTP_200_OK,
                meta=metadata
            )
            
        except ValidationException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al obtener feed: {str(e)}")
            raise
    
    def get_feed_item(self, item_id: str):
        """
        Obtiene un elemento específico del feed.
        
        Args:
            item_id: ID del elemento
            
        Returns:
            Response: Respuesta HTTP con los datos del elemento o error
        """
        try:
            # Obtenemos el elemento desde el repositorio
            item = self.repository.get_feed_item(item_id)
            
            if not item:
                raise ResourceNotFoundException("Elemento de feed", item_id)
            
            return create_response(
                data=item.to_dict(),
                message="Elemento de feed obtenido con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al obtener elemento de feed con ID {item_id}: {str(e)}")
            raise
