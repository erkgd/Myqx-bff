from typing import List, Optional, Dict, Any
from .repository_interface import RepositoryInterface
from ..models.user_model import User
from ..dtos.user_dto import UserDTO
from ..services.implementations.users_service_impl import UsersServiceImpl


class UserRepository(RepositoryInterface[UserDTO]):
    """
    Implementación del repositorio para usuarios.
    
    En un BFF, el repositorio actúa principalmente como una fachada para
    los servicios externos, traduciendo DTOs a las respuestas de la API
    y viceversa.
    """
    
    def __init__(self):
        """
        Inicializa el repositorio de usuarios.
        """
        self.service = UsersServiceImpl()
    
    def find_by_id(self, entity_id: str) -> Optional[UserDTO]:
        """
        Encuentra un usuario por su ID.
        
        Args:
            entity_id: ID del usuario
            
        Returns:
            UserDTO: DTO del usuario encontrado o None si no existe
        """
        try:
            user_data = self.service.get_user(entity_id)
            return UserDTO.from_dict(user_data)
        except Exception:
            return None
    
    def find_all(self, **filters) -> List[UserDTO]:
        """
        Encuentra todos los usuarios que coinciden con los filtros.
        
        Args:
            **filters: Filtros a aplicar
            
        Returns:
            List[UserDTO]: Lista de DTOs de usuarios
        """
        try:
            users_data = self.service.get_users(**filters)
            return [UserDTO.from_dict(user) for user in users_data]
        except Exception:
            return []
    
    def create(self, entity: UserDTO) -> UserDTO:
        """
        Crea un nuevo usuario.
        
        Args:
            entity: DTO del usuario a crear
            
        Returns:
            UserDTO: DTO del usuario creado
        """
        try:
            user_data = self.service.create_user(entity.to_dict())
            return UserDTO.from_dict(user_data)
        except Exception as e:
            raise ValueError(f"Error al crear el usuario: {str(e)}")
    
    def update(self, entity_id: str, entity: UserDTO) -> UserDTO:
        """
        Actualiza un usuario existente.
        
        Args:
            entity_id: ID del usuario
            entity: DTO con los nuevos datos del usuario
            
        Returns:
            UserDTO: DTO del usuario actualizado
        """
        try:
            user_data = self.service.update_user(entity_id, entity.to_dict())
            return UserDTO.from_dict(user_data)
        except Exception as e:
            raise ValueError(f"Error al actualizar el usuario: {str(e)}")
    
    def delete(self, entity_id: str) -> bool:
        """
        Elimina un usuario.
        
        Args:
            entity_id: ID del usuario
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        try:
            return self.service.delete_user(entity_id)
        except Exception:
            return False
            
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Dict o None: Respuesta de autenticación o None si falló
        """
        try:
            credentials = {
                'username': username,
                'password': password
            }
            return self.service.authenticate(credentials)
        except Exception:
            return None