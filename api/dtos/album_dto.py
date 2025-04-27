from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class AlbumDTO:
    """
    Data Transfer Object para representar un álbum.
    """
    id: str
    name: str
    artist: str
    release_date: Optional[datetime] = None
    spotify_id: Optional[str] = None
    cover_image: Optional[str] = None
    tracks_count: Optional[int] = None
    popularity: Optional[int] = None
    genres: Optional[List[str]] = None
    average_rating: Optional[float] = None
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AlbumDTO':
        """
        Crea un DTO a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del álbum
            
        Returns:
            Instancia de AlbumDTO
        """
        return AlbumDTO(
            id=data.get('id'),
            name=data.get('name'),
            artist=data.get('artist'),
            release_date=data.get('release_date'),
            spotify_id=data.get('spotify_id', data.get('spotifyId')),
            cover_image=data.get('cover_image', data.get('coverImage')),
            tracks_count=data.get('tracks_count', data.get('tracksCount')),
            popularity=data.get('popularity'),
            genres=data.get('genres'),
            average_rating=data.get('average_rating', data.get('averageRating'))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el DTO a un diccionario.
        
        Returns:
            Diccionario con los datos del álbum
        """
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'releaseDate': self.release_date.isoformat() if self.release_date else None,
            'spotifyId': self.spotify_id,
            'coverImage': self.cover_image,
            'tracksCount': self.tracks_count,
            'popularity': self.popularity,
            'genres': self.genres,
            'averageRating': self.average_rating
        }
