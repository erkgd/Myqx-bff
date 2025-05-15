from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..controllers.users_controller import UsersController
import logging
import sys
import datetime

logger = logging.getLogger(__name__)

class UserFollowingStatusView(APIView):
    """
    Endpoint para verificar el estado de seguimiento de un usuario específico.
    Permite verificar si el usuario autenticado sigue a otro usuario.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = UsersController()
    def get(self, request, follower_id, followed_id, format=None):
        """
        Verifica si un usuario sigue a otro.
        
        Args:
            request: Objeto HttpRequest
            follower_id: ID del usuario que podría estar siguiendo
            followed_id: ID del usuario que podría estar siendo seguido
            
        Returns:
            Response: Respuesta con el estado de seguimiento
        """
        try:
            print(f"[USER_FOLLOWING_STATUS_VIEW] Verificando estado de seguimiento entre {follower_id} y {followed_id}", file=sys.stderr)
            
            # Aquí recibimos ambos IDs directamente en la URL
            # Pero también podemos permitir sobreescribirlos desde los parámetros para compatibilidad
            follower_id_param = request.query_params.get('currentUserId', follower_id)
            
            if not follower_id:
                print("[USER_FOLLOWING_STATUS_VIEW] No se proporcionó currentUserId", file=sys.stderr)
                # Si no hay follower_id, asumimos que queremos verificar si alguien sigue al usuario
                return Response(
                    {
                        "error": "Se requiere parámetro currentUserId para verificar estado de seguimiento",
                        "message": "Parámetro requerido no proporcionado",
                        "status": "error",
                        "timestamp": datetime.datetime.now().isoformat()
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(f"[USER_FOLLOWING_STATUS_VIEW] Usando follower_id: {follower_id} y followed_id: {followed_id}", file=sys.stderr)
            
            # Llamar al controlador para verificar estado de seguimiento
            return self.controller.check_following(follower_id, followed_id)
            
        except Exception as e:
            error_msg = f"Error al procesar solicitud de estado de seguimiento: {str(e)}"
            logger.exception(error_msg)
            print(f"[USER_FOLLOWING_STATUS_VIEW] Error: {error_msg}", file=sys.stderr)
            return Response(
                {
                    "error": "Error al procesar la solicitud",
                    "message": str(e),
                    "status": "error",
                    "timestamp": datetime.datetime.now().isoformat()
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
