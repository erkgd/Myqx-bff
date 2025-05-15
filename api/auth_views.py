from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import create_response
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenVerifyView(APIView):
    """
    Vista personalizada para verificar tokens JWT sin requerir CSRF.
    Esta vista permite verificar tokens desde clientes como aplicaciones móviles
    que podrían tener problemas con la verificación CSRF.
    """
    
    def post(self, request, *args, **kwargs):
        try:

            if request.data is None:
                request.data = {}
                
            # Aquí es verifica si el token esta inclos en el cos de la petició
            token = None
            if isinstance(request.data, dict):
                token = request.data.get('token')
            if not token and hasattr(request, 'POST'):
                token = request.POST.get('token')
            if not token and 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2 and auth[0].lower() == 'token':
                    token = auth[1]
                elif len(auth) == 2 and auth[0].lower() == 'bearer':
                    token = auth[1]
                    
            # Comprobar si se proporcionó un token
            if not token:
                return create_response(
                    data=None,
                    message="Token no proporcionado",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    errors={"token": "Este campo es requerido"}
                )
            
            # Intentar decodificar el token
            AccessToken(token)
            return create_response(
                data={"valid": True},
                message="Token válido",
                status_code=status.HTTP_200_OK
            )
        except (TokenError, InvalidToken):
            return create_response(
                data={"valid": False},
                message="Token inválido o expirado",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.exception("Error inesperado en CustomTokenVerifyView.post")
            return create_response(
                data=None,
                message="Error interno al verificar token",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors={"detail": str(e)}
            )
    
    def get(self, request, *args, **kwargs):
        """
        Manejar solicitudes GET redirigiendo a POST con el mismo token.
        Esto es útil para clientes que envían tokens en la URL.
        """
        token = request.GET.get('token')
        if not token:
            return create_response(
                data=None,
                message="Token no proporcionado",
                status_code=status.HTTP_400_BAD_REQUEST,
                errors={"token": "Este campo es requerido"}
            )
        
        # Crear una solicitud POST simulada
        request.data = {'token': token}
        return self.post(request, *args, **kwargs)
