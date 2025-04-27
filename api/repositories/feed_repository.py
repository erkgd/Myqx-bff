from typing import List, Dict, Any, Optional
from ..dtos.feed_item_dto import FeedItemDTO
import logging

logger = logging.getLogger(__name__)


class FeedRepository:
    """
    Repositorio para operaciones relacionadas con el feed.
    """
    
    def __init__(self):
        """
        Constructor del repositorio de feed.
        """
        pass
    
    def get_feed(self, user_id: str, limit: int = 20, offset: int = 0) -> List[FeedItemDTO]:
        """
        Obtiene el feed para un usuario específico.
        
        Args:
            user_id: ID del usuario
            limit: Cantidad máxima de elementos a devolver
            offset: Número de elementos a saltar (para paginación)
            
        Returns:
            Lista de DTOs de elementos del feed
        """
        # Importamos dentro del método para evitar dependencias circulares
        from ..services.implementations.feed_service_impl import FeedServiceImpl
        feed_service = FeedServiceImpl()
        
        try:
            # Llamamos al servicio para obtener los datos
            feed_items = feed_service.get_feed(user_id, limit, offset)
            
            # Convertimos los diccionarios a DTOs
            return [FeedItemDTO.from_dict(item) for item in feed_items]
            
        except Exception as e:
            logger.error(f"Error al obtener feed para usuario {user_id}: {str(e)}")
            return []
    
    def get_feed_item(self, item_id: str) -> Optional[FeedItemDTO]:
        """
        Obtiene un elemento específico del feed.
        
        Args:
            item_id: ID del elemento
            
        Returns:
            DTO del elemento o None si no se encuentra
        """
        # Importamos dentro del método para evitar dependencias circulares
        from ..services.implementations.feed_service_impl import FeedServiceImpl
        feed_service = FeedServiceImpl()
        
        try:
            # Llamamos al servicio para obtener los datos
            item_data = feed_service.get_feed_item(item_id)
            
            if item_data:
                # Convertimos el diccionario a DTO
                return FeedItemDTO.from_dict(item_data)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error al obtener elemento de feed con ID {item_id}: {str(e)}")
            return None
