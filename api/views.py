from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .controllers.users_controller import UsersController
import datetime


class HealthCheckView(APIView):
    """
    Endpoint para verificar el estado del servicio BFF.
    """
    permission_classes = [AllowAny]  # Sin requisitos de autenticación para health check

    def get(self, request, format=None):
        """
        Retorna el estado actual del servicio BFF.
        """
        data = {
            'status': 'ok',
            'message': 'MyQx BFF service is running',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0',
        }
        return Response(data, status=status.HTTP_200_OK)


class UserView(APIView):
    """
    Endpoint para operaciones en un usuario específico.
    """
    # Creamos una única instancia del controlador para la vista
    users_controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene un usuario por su ID
        """
        return self.users_controller.get_user(user_id)
    
    def put(self, request, user_id, format=None):
        """
        Actualiza un usuario existente
        """
        return self.users_controller.update_user(user_id, request.data)
    
    def delete(self, request, user_id, format=None):
        """
        Elimina un usuario
        """
        return self.users_controller.delete_user(user_id)


class UsersView(APIView):
    """
    Endpoint para operaciones en la colección de usuarios.
    """
    users_controller = UsersController()
    
    def get(self, request, format=None):
        """
        Obtiene la lista de usuarios, opcionalmente filtrada
        """
        return self.users_controller.get_users(request)
    
    def post(self, request, format=None):
        """
        Crea un nuevo usuario
        """
        return self.users_controller.create_user(request.data)


class AuthView(APIView):
    """
    Endpoint para autenticación de usuarios.
    """
    permission_classes = [AllowAny]  # La autenticación no requiere estar autenticado
    users_controller = UsersController()
    
    def post(self, request, format=None):
        """
        Autentica un usuario con sus credenciales
        """
        return self.users_controller.authenticate(request.data)
