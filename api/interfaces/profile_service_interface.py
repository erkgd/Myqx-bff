from typing import Dict, Any, List, Optional

class ProfileServiceInterface:
    """
    Interfaz para el servicio de perfiles de usuario.
    Define los métodos que debe implementar cualquier servicio de perfiles.
    """
    
    def get_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene el perfil de un usuario específico.
        
        Args:
            user_id: ID del usuario del que se quiere obtener el perfil
            
        Returns:
            Diccionario con los datos del perfil del usuario
        """
        pass
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza el perfil de un usuario.
        
        Args:
            user_id: ID del usuario cuyo perfil se va a actualizar
            profile_data: Datos nuevos para el perfil
            
        Returns:
            Diccionario con los datos actualizados del perfil
        """
        pass
    
    def get_extended_profile(self, user_id: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Obtiene un perfil extendido con información adicional basada en las opciones.
        
        Args:
            user_id: ID del usuario del que se quiere obtener el perfil
            options: Opciones para personalizar la información que se incluye
            
        Returns:
            Diccionario con los datos extendidos del perfil
        """
        pass
