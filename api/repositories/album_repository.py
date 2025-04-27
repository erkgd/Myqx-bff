from typing import List, Dict, Any, Optional
from ..dtos.album_dto import AlbumDTO
from ..dtos.album_rating_dto import AlbumRatingDTO
import logging

logger = logging.getLogger(__name__)


class AlbumRepository:
    """
    Repositorio para operaciones relacionadas con álbumes.
    """
    
    def __init__(self):
        """
        Constructor del repositorio de álbumes.
        """
        # Inicialización si es necesario
        pass
    
    def find_by_id(self, album_id: str) -> Optional[AlbumDTO]:
        """
        Encuentra un álbum por su ID.
        
        Args:
            album_id: ID del álbum a buscar
            
        Returns:
            AlbumDTO si se encuentra, None en caso contrario
        """
        # Implementación que se conectaría con el servicio backend
        # En este punto, delegamos al servicio de álbumes
        from ..services.implementations.albums_service_impl import AlbumsServiceImpl
        service = AlbumsServiceImpl()
        
        try:
            album_data = service.get_album(album_id)
            if album_data:
                return AlbumDTO.from_dict(album_data)
            return None
        except Exception as e:
            logger.error(f"Error al buscar álbum por ID {album_id}: {str(e)}")
            return None
    
    def get_album_ratings(self, album_id: str) -> List[AlbumRatingDTO]:
        """
        Obtiene todas las calificaciones de un álbum.
        
        Args:
            album_id: ID del álbum
            
        Returns:
            Lista de calificaciones
        """
        from ..services.implementations.albums_service_impl import AlbumsServiceImpl
        service = AlbumsServiceImpl()
        
        try:
            ratings_data = service.get_album_ratings(album_id)
            return [AlbumRatingDTO.from_dict(rating) for rating in ratings_data]
        except Exception as e:
            logger.error(f"Error al obtener calificaciones del álbum {album_id}: {str(e)}")
            return []
    
    def rate_album(self, rating_data: AlbumRatingDTO) -> Optional[AlbumRatingDTO]:
        """
        Califica un álbum.
        
        Args:
            rating_data: Datos de la calificación
            
        Returns:
            Calificación guardada o None si hubo un error
        """
        from ..services.implementations.albums_service_impl import AlbumsServiceImpl
        service = AlbumsServiceImpl()
        
        try:
            result = service.rate_album(rating_data.to_dict())
            if result:
                return AlbumRatingDTO.from_dict(result)
            return None
        except Exception as e:
            logger.error(f"Error al calificar álbum: {str(e)}")
            return None
            
    def get_user_album_rating(self, user_id: str, album_id: str) -> Optional[AlbumRatingDTO]:
        """
        Obtiene la calificación de un usuario para un álbum específico.
        
        Args:
            user_id: ID del usuario
            album_id: ID del álbum
            
        Returns:
            Calificación o None si no existe
        """
        from ..services.implementations.albums_service_impl import AlbumsServiceImpl
        service = AlbumsServiceImpl()
        
        try:
            rating_data = service.get_user_album_rating(user_id, album_id)
            if rating_data:
                return AlbumRatingDTO.from_dict(rating_data)
            return None
        except Exception as e:
            logger.error(f"Error al obtener calificación del usuario {user_id} para el álbum {album_id}: {str(e)}")
            return None
