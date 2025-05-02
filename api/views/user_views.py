from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..controllers.users_controller import UsersController
import datetime
import logging
import sys

class UsersView(APIView):
    """
    Endpoint para listar y crear usuarios.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = UsersController()
    
    def get(self, request, format=None):
        """
        Lista usuarios con filtros opcionales.
        """
        return self.controller.get_users(request)
    
    def post(self, request, format=None):
        """
        Crea un nuevo usuario.
        """
        return self.controller.create_user(request.data)


class UserView(APIView):
    """
    Endpoint para operaciones sobre un usuario específico.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene un usuario por su ID.
        """
        return self.controller.get_user(user_id)
    
    def put(self, request, user_id, format=None):
        """
        Actualiza un usuario por completo.
        """
        return self.controller.update_user(user_id, request.data)
    
    def patch(self, request, user_id, format=None):
        """
        Actualiza parcialmente un usuario.
        """
        return self.controller.partial_update_user(user_id, request.data)
    
    def delete(self, request, user_id, format=None):
        """
        Elimina un usuario.
        """
        return self.controller.delete_user(user_id)


class FollowingNetworkView(APIView):
    """
    Endpoint para obtener la red de seguidos de un usuario.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    users_controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene la red de seguidos para un usuario específico.
        """
        try:
            # Usando el método que implementamos en el controlador
            following_network = self.users_controller.get_following_network(user_id)
            
            # Crear una respuesta estructurada
            data = {
                'user_id': user_id,
                'following_network': following_network,
                'count': len(following_network) if following_network else 0,
                'timestamp': datetime.datetime.now().isoformat(),
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # Manejar errores de manera adecuada
            error_data = {
                'error': str(e),
                'user_id': user_id,
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    """
    Endpoint para obtener el perfil detallado de un usuario específico.
    Proporciona información adicional como estadísticas, actividad reciente y preferencias.
    """
    users_controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene el perfil completo de un usuario por su ID
        """
        return self.users_controller.get_user_profile(user_id)


class UserFollowingView(APIView):
    """
    Endpoint para gestionar relaciones de seguimiento entre usuarios.
    Permite verificar, crear y eliminar relaciones donde un usuario sigue a otro.
    """
    users_controller = UsersController()
    
    def get(self, request, follower_id, followed_id, format=None):
        """
        Verifica si un usuario sigue a otro.
        """
        return self.users_controller.check_following(follower_id, followed_id)
    
    def post(self, request, follower_id, followed_id, format=None):
        """
        Hace que un usuario siga a otro.
        """
        return self.users_controller.follow_user(follower_id, followed_id)
    
    def delete(self, request, follower_id, followed_id, format=None):
        """
        Hace que un usuario deje de seguir a otro.
        """
        return self.users_controller.unfollow_user(follower_id, followed_id)
