from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class UserServiceInterface(ABC):
    """
    Interfaz para definir los métodos que debe implementar cualquier servicio de usuarios.
    Siguiendo el principio de inversión de dependencias, los controladores dependerán
    de esta interfaz en lugar de una implementación concreta.
    """
    
    @abstractmethod
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene un usuario por su ID desde el backend.
        
        Args:
            user_id: ID del usuario a obtener
            
        Returns:
            Dict que representa los datos del usuario
        """
        pass
    
    @abstractmethod
    def get_users(self, **params) -> List[Dict[str, Any]]:
        """
        Obtiene una lista de usuarios con filtros opcionales.
        
        Args:
            **params: Parámetros de filtrado opcionales
            
        Returns:
            Lista de diccionarios representando usuarios
        """
        pass
    
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo usuario.
        
        Args:
            user_data: Datos del usuario a crear
            
        Returns:
            Dict con los datos del usuario creado
        """
        pass
    
    @abstractmethod
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un usuario existente.
        
        Args:
            user_id: ID del usuario a actualizar
            user_data: Nuevos datos del usuario
            
        Returns:
            Dict con los datos del usuario actualizado
        """
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """
        Elimina un usuario.
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        pass
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario.
        
        Args:
            credentials: Credenciales del usuario (generalmente email/username y password)
            
        Returns:
            Dict con información del token y usuario o None si la autenticación falla
        """
        pass