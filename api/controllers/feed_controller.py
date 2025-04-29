from typing import Dict, Any
from rest_framework import status
from rest_framework.request import Request
from ..repositories.feed_repository import FeedRepository
from ..exceptions.api_exceptions import ResourceNotFoundException, ValidationException
from ..utils import create_response
import logging
import sys

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
            
            # Convertimos los DTOs a diccionarios y nos aseguramos de que el campo review esté presente
            feed_data = []
            for item in feed_items:
                item_dict = item.to_dict()
                # Asegurarnos de que el campo 'review' esté presente con el mismo valor que 'comment'
                if 'comment' in item_dict and item_dict['comment'] is not None:
                    item_dict['review'] = item_dict['comment']
                feed_data.append(item_dict)
              # Preparamos metadatos para la paginación
            metadata = {
                "count": len(feed_data),
                "limit": limit,
                "offset": offset,
                "hasMore": len(feed_data) >= limit  # Si se devolvieron tantos elementos como el límite, probablemente hay más
            }
              # Agregamos un log estructurado y detallado que muestra lo que se envía al frontend
            print(f"[FEED_CONTROLLER] ********** DATOS ENVIADOS AL FRONTEND **********", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Resumen: {len(feed_data)} elementos encontrados", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Metadatos: count={len(feed_data)}, limit={limit}, offset={offset}, hasMore={len(feed_data) >= limit}", file=sys.stderr)
            
            # Loguear información sobre reviews para diagnóstico
            reviews_count = sum(1 for item in feed_data if item.get('review') is not None)
            print(f"[FEED_CONTROLLER] Elementos con reviews: {reviews_count} de {len(feed_data)}", file=sys.stderr)
            
            # Mostrar los primeros 2 elementos completos como muestra (o todos si son menos de 3)
            sample_size = min(2, len(feed_data))
            if sample_size > 0:
                print(f"[FEED_CONTROLLER] Muestra de datos (primeros {sample_size} elementos):", file=sys.stderr)
                for i in range(sample_size):
                    item = feed_data[i]
                    print(f"[FEED_CONTROLLER] Elemento {i+1}:", file=sys.stderr)
                    print(f"[FEED_CONTROLLER]   ID: {item.get('id')}", file=sys.stderr)
                    print(f"[FEED_CONTROLLER]   Usuario: {item.get('username')} (ID: {item.get('userId')})", file=sys.stderr)
                    print(f"[FEED_CONTROLLER]   Contenido: {item.get('contentType')} (ID: {item.get('contentId')})", file=sys.stderr)
                    print(f"[FEED_CONTROLLER]   Rating: {item.get('rating')}", file=sys.stderr)
                    print(f"[FEED_CONTROLLER]   Review: {item.get('review')}", file=sys.stderr)
                    print(f"[FEED_CONTROLLER]   Fecha: {item.get('date') or item.get('createdAt')}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] ************************************************", file=sys.stderr)
              
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
        try:            # Obtenemos el elemento desde el repositorio
            item = self.repository.get_feed_item(item_id)
            
            if not item:
                raise ResourceNotFoundException("Elemento de feed", item_id)
            
            # Convertimos el DTO a diccionario
            item_dict = item.to_dict()
            
            # Asegurarnos de que el campo 'review' esté presente con el mismo valor que 'comment'
            if 'comment' in item_dict and item_dict['comment'] is not None:
                item_dict['review'] = item_dict['comment']
            
            # Mostramos en log lo que se enviará al frontend
            print(f"[FEED_CONTROLLER] ********** ELEMENTO ENVIADO AL FRONTEND **********", file=sys.stderr)
            print(f"[FEED_CONTROLLER] ID: {item_dict.get('id')}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Usuario: {item_dict.get('username')} (ID: {item_dict.get('userId')})", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Tipo de contenido: {item_dict.get('contentType')}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] ID de contenido: {item_dict.get('contentId')}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Rating: {item_dict.get('rating')}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Tiene review: {'Sí' if item_dict.get('review') else 'No'}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] Review: {item_dict.get('review')}", file=sys.stderr)
            print(f"[FEED_CONTROLLER] ************************************************", file=sys.stderr)
            
            return create_response(
                data=item_dict,
                message="Elemento de feed obtenido con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al obtener elemento de feed con ID {item_id}: {str(e)}")
            raise
