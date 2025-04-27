from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class FeedItemDTO:
    """
    Data Transfer Object para representar un elemento del feed.
    Puede ser una actividad, calificación, revisión, recomendación, etc.
    """
    id: str
    type: str  # tipo de elemento: 'rating', 'review', 'recommendation', etc.
    user_id: str  # ID del usuario que generó la actividad
    username: Optional[str] = None  # nombre del usuario
    profile_image: Optional[str] = None  # URL de la imagen de perfil
    content_id: Optional[str] = None  # ID del contenido relacionado (álbum, track)
    content_type: Optional[str] = None  # tipo de contenido: 'album', 'track', etc.
    content_title: Optional[str] = None  # título del contenido
    content_artist: Optional[str] = None  # artista del contenido
    content_image: Optional[str] = None  # URL de la imagen del contenido
    rating: Optional[float] = None  # calificación (si es una calificación)
    comment: Optional[str] = None  # comentario o revisión
    created_at: Optional[datetime] = None  # fecha de creación
    likes_count: Optional[int] = 0  # contador de me gusta
    comments_count: Optional[int] = 0  # contador de comentarios
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FeedItemDTO':
        """
        Crea un DTO a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del elemento de feed
            
        Returns:
            Instancia de FeedItemDTO
        """
        # Convertir la fecha si existe
        created_at = data.get('created_at') or data.get('createdAt')
        if created_at and isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                created_at = None
        
        return FeedItemDTO(
            id=data.get('id'),
            type=data.get('type'),
            user_id=data.get('user_id') or data.get('userId'),
            username=data.get('username'),
            profile_image=data.get('profile_image') or data.get('profileImage'),
            content_id=data.get('content_id') or data.get('contentId'),
            content_type=data.get('content_type') or data.get('contentType'),
            content_title=data.get('content_title') or data.get('contentTitle'),
            content_artist=data.get('content_artist') or data.get('contentArtist'),
            content_image=data.get('content_image') or data.get('contentImage'),
            rating=data.get('rating'),
            comment=data.get('comment'),
            created_at=created_at,
            likes_count=data.get('likes_count') or data.get('likesCount') or 0,
            comments_count=data.get('comments_count') or data.get('commentsCount') or 0,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el DTO a un diccionario.
        
        Returns:
            Diccionario con los datos del elemento de feed
        """
        return {
            'id': self.id,
            'type': self.type,
            'userId': self.user_id,
            'username': self.username,
            'profileImage': self.profile_image,
            'contentId': self.content_id,
            'contentType': self.content_type,
            'contentTitle': self.content_title,
            'contentArtist': self.content_artist,
            'contentImage': self.content_image,
            'rating': self.rating,
            'comment': self.comment,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'likesCount': self.likes_count,
            'commentsCount': self.comments_count,
        }
