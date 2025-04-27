from abc import ABC, abstractmethod
from typing import List, Dict, Any


class FeedServiceInterface(ABC):
    """
    Interfaz para servicios que manejan operaciones relacionadas con el feed.
    """
    
    @abstractmethod
    def get_feed(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Obtiene el feed para un usuario específico.
        
        Args:
            user_id: ID del usuario
            limit: Cantidad máxima de elementos a devolver
            offset: Número de elementos a saltar (para paginación)
            
        Returns:
            Lista de elementos del feed
        """
        pass
    
    @abstractmethod
    def get_feed_item(self, item_id: str) -> Dict[str, Any]:
        """
        Obtiene un elemento específico del feed.
        
        Args:
            item_id: ID del elemento
            
        Returns:
            Datos del elemento
        """
        pass
