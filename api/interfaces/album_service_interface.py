from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AlbumServiceInterface(ABC):
    """
    Interfaz para servicios que manejan operaciones relacionadas con álbumes.
    """
    
    @abstractmethod
    def get_album(self, album_id: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un álbum por su ID.
        
        Args:
            album_id: ID del álbum
            
        Returns:
            Diccionario con la información del álbum
        """
        pass
    
    @abstractmethod
    def get_album_ratings(self, album_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene las calificaciones de un álbum específico.
        
        Args:
            album_id: ID del álbum
            
        Returns:
            Lista de calificaciones
        """
        pass
    
    @abstractmethod
    def rate_album(self, rating_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Califica un álbum.
        
        Args:
            rating_data: Datos de la calificación
            
        Returns:
            Información de la calificación guardada
        """
        pass
    
    @abstractmethod
    def get_user_album_rating(self, user_id: str, album_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene la calificación de un usuario para un álbum específico.
        
        Args:
            user_id: ID del usuario
            album_id: ID del álbum
            
        Returns:
            Información de la calificación o None si no existe
        """
        pass
