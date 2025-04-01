from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class UserDTO:
    """
    DTO (Data Transfer Object) para representar usuarios.
    
    Este objeto se utiliza para transferir datos de usuario entre
    diferentes capas de la aplicación sin exponer la implementación interna.
    """
    id: Optional[str] = None
    username: str = ""
    email: str = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserDTO':
        """
        Crea un UserDTO a partir de un diccionario.
        
        Args:
            data: Diccionario con datos de usuario
            
        Returns:
            UserDTO: Objeto DTO creado
        """
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            email=data.get('email', ''),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_active=data.get('is_active', True)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el DTO a un diccionario.
        
        Returns:
            Dict: Diccionario con los datos del usuario
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active
        }


@dataclass
class AuthResponseDTO:
    """
    DTO para la respuesta de autenticación.
    """
    token: str
    user: UserDTO
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuthResponseDTO':
        """
        Crea un AuthResponseDTO a partir de un diccionario.
        
        Args:
            data: Diccionario con datos de autenticación
            
        Returns:
            AuthResponseDTO: Objeto DTO creado
        """
        return cls(
            token=data.get('token', ''),
            user=UserDTO.from_dict(data.get('user', {}))
        )