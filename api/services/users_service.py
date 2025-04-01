from django.conf import settings
from .base_service import BaseService

class UsersService(BaseService):
    """
    Servicio para comunicarse con el backend de usuarios.
    Este es un ejemplo de implementación concreta para tu BFF.
    """
    
    def __init__(self):
        # En un caso real, obtendrías esta URL desde settings o variables de entorno
        base_url = getattr(settings, 'USERS_SERVICE_URL', 'http://localhost:8001/api')
        super().__init__(base_url=base_url)
    
    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID desde el backend
        """
        return self.get(f'/users/{user_id}/')
    
    def get_users(self, **params):
        """
        Obtiene una lista de usuarios con filtros opcionales
        """
        return self.get('/users/', params=params)
    
    def create_user(self, user_data):
        """
        Crea un nuevo usuario
        """
        return self.post('/users/', data=user_data)
    
    def update_user(self, user_id, user_data):
        """
        Actualiza un usuario existente
        """
        return self.put(f'/users/{user_id}/', data=user_data)
    
    def delete_user(self, user_id):
        """
        Elimina un usuario
        """
        return self.delete(f'/users/{user_id}/')
    
    def authenticate(self, credentials):
        """
        Autentica un usuario
        """
        return self.post('/auth/token/', data=credentials)