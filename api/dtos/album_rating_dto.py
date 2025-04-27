from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class AlbumRatingDTO:
    """
    Data Transfer Object para representar la calificación de un álbum o contenido.
    """
    id: Optional[str] = None
    user_id: str = None
    album_id: str = None  # ID del álbum o contenido
    rating: float = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    content_type: str = "album"  # Tipo de contenido: 'album' o 'track'
    timestamp: Optional[str] = None  # Timestamp de la operación
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AlbumRatingDTO':
        """
        Crea un DTO a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos de la calificación
            
        Returns:
            Instancia de AlbumRatingDTO
        """
        # Manejo unificado de IDs (content_id o album_id)
        content_id = data.get('content_id', data.get('albumId', data.get('album_id')))
        
        return AlbumRatingDTO(
            id=data.get('id'),
            user_id=data.get('user_id', data.get('userId')),
            album_id=content_id,
            rating=data.get('rating'),
            comment=data.get('comment'),
            created_at=data.get('created_at', data.get('createdAt')),
            updated_at=data.get('updated_at', data.get('updatedAt')),
            content_type=data.get('content_type', data.get('contentType', 'album')),
            timestamp=data.get('timestamp')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el DTO a un diccionario.
        
        Returns:
            Diccionario con los datos de la calificación
        """
        return {
            'id': self.id,
            'userId': self.user_id,
            'albumId': self.album_id,
            'contentId': self.album_id,  # Añadimos compatibilidad con content_id
            'rating': self.rating,
            'comment': self.comment,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'contentType': self.content_type,
            'timestamp': self.timestamp
        }
