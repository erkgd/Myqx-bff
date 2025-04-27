from typing import Dict, Any
from rest_framework import status
from rest_framework.request import Request
from ..repositories.album_repository import AlbumRepository
from ..dtos.album_rating_dto import AlbumRatingDTO
from ..exceptions.api_exceptions import ResourceNotFoundException, ValidationException
from ..utils import create_response
import logging

logger = logging.getLogger(__name__)


class AlbumsController:
    """
    Controlador para manejar operaciones relacionadas con álbumes.
    """
    
    def __init__(self):
        """
        Constructor del controlador de álbumes.
        """
        self.repository = AlbumRepository()
    
    def get_album(self, album_id: str):
        """
        Obtiene un álbum por su ID.
        
        Args:
            album_id: ID del álbum a obtener (puede ser ID de Spotify)
            
        Returns:
            Response: Respuesta HTTP con los datos del álbum o error
        """
        try:
            album = self.repository.find_by_id(album_id)
            if not album:
                raise ResourceNotFoundException("Álbum", album_id)
                
            return create_response(
                data=album.to_dict(),
                message="Álbum encontrado con éxito",
                status_code=status.HTTP_200_OK
            )
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al obtener álbum con ID {album_id}: {str(e)}")
            raise
    
    def get_album_ratings(self, album_id: str):
        """
        Obtiene todas las calificaciones de un álbum.
        
        Args:
            album_id: ID del álbum
            
        Returns:
            Response: Respuesta HTTP con la lista de calificaciones o error
        """
        try:
            ratings = self.repository.get_album_ratings(album_id)
            if not ratings:
                # No es un error, puede ser que el álbum no tenga calificaciones
                return create_response(
                    data=[],
                    message="No se encontraron calificaciones para este álbum",
                    status_code=status.HTTP_200_OK
                )
            
            # Convertir los DTOs a diccionarios
            ratings_dict = [rating.to_dict() for rating in ratings]
            
            return create_response(
                data=ratings_dict,
                message="Calificaciones obtenidas con éxito",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(f"Error al obtener calificaciones del álbum {album_id}: {str(e)}")
            raise
    
    def rate_album(self, data: Dict[str, Any]):
        """
        Califica un álbum o canción.
        
        Args:
            data: Datos de la calificación
            
        Returns:
            Response: Respuesta HTTP con la calificación guardada o error
        """
        try:
            # Validar datos requeridos
            required_fields = ['rating']
            
            # Validar el ID del contenido (puede ser albumId o content_id)
            if 'albumId' not in data and 'content_id' not in data:
                required_fields.append('content_id')
            
            # Validar el ID de usuario
            if 'userId' not in data and 'user_id' not in data:
                required_fields.append('userId')
            
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                raise ValidationException(
                    f"Faltan campos requeridos: {', '.join(missing_fields)}",
                    errors={field: "Este campo es requerido" for field in missing_fields}
                )
            
            if not 1 <= float(data['rating']) <= 5:
                raise ValidationException(
                    "La calificación debe estar entre 1 y 5",
                    errors={"rating": "La calificación debe estar entre 1 y 5"}
                )
            
            # Crear DTO y guardar
            rating_dto = AlbumRatingDTO.from_dict(data)
            saved_rating = self.repository.rate_album(rating_dto)
            
            if not saved_rating:
                raise Exception("Error al guardar la calificación")
            
            return create_response(
                data=saved_rating.to_dict(),
                message="Calificación guardada con éxito",
                status_code=status.HTTP_201_CREATED
            )
        except ValidationException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al calificar contenido: {str(e)}")
            raise
    
    def get_user_album_rating(self, album_id: str, request: Request):
        """
        Obtiene la calificación de un usuario para un álbum específico.
        
        Args:
            album_id: ID del álbum
            request: Objeto request que contiene el user_id como parámetro
            
        Returns:
            Response: Respuesta HTTP con la calificación del usuario o error
        """
        try:
            # Obtenemos el user_id del query param
            user_id = request.query_params.get('user_id')
            
            if not user_id:
                raise ValidationException(
                    "Se requiere el ID del usuario",
                    errors={"user_id": "Este campo es requerido como parámetro de consulta"}
                )
            
            # Obtenemos la calificación
            rating = self.repository.get_user_album_rating(user_id, album_id)
            
            if not rating:
                # No es un error, puede ser que el usuario no haya calificado el álbum
                return create_response(
                    data={"exists": False},
                    message="El usuario no ha calificado este álbum",
                    status_code=status.HTTP_200_OK
                )
            
            return create_response(
                data={"exists": True, "rating": rating.to_dict()},
                message="Calificación obtenida con éxito",
                status_code=status.HTTP_200_OK
            )
        except ValidationException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al obtener calificación del álbum {album_id}: {str(e)}")
            raise
