from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic

T = TypeVar('T')


class RepositoryInterface(Generic[T], ABC):
    """
    Interfaz genérica para repositorios.
    Define los métodos que debe implementar cualquier repositorio.
    """
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """
        Encuentra una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad
            
        Returns:
            Entidad encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def find_all(self, **filters) -> List[T]:
        """
        Encuentra todas las entidades que coinciden con los filtros.
        
        Args:
            **filters: Filtros a aplicar
            
        Returns:
            Lista de entidades
        """
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Crea una nueva entidad.
        
        Args:
            entity: Entidad a crear
            
        Returns:
            Entidad creada
        """
        pass
    
    @abstractmethod
    def update(self, entity_id: str, entity: T) -> T:
        """
        Actualiza una entidad existente.
        
        Args:
            entity_id: ID de la entidad
            entity: Entidad con los nuevos datos
            
        Returns:
            Entidad actualizada
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad.
        
        Args:
            entity_id: ID de la entidad
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        pass