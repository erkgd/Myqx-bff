from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..controllers.users_controller import UsersController
import logging
import sys

logger = logging.getLogger(__name__)

class UserCompleteProfileView(APIView):
    """
    Endpoint para obtener el perfil completo de un usuario con información adicional
    como estado de seguimiento, álbumes mejor valorados y actividad reciente.
    """
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = UsersController()
    
    def get(self, request, user_id, format=None):
        """
        Obtiene el perfil completo de un usuario con información adicional opcional.
        
        Parámetros de consulta:
        - currentUserId: ID del usuario que está realizando la consulta (para determinar relación de seguimiento)
        - includeFollowingStatus: True para incluir si currentUserId sigue al usuario
        - includeTopRatedAlbum: True para incluir el álbum mejor valorado por el usuario
        - includeRecentActivity: True para incluir actividad reciente del usuario
        - activityLimit: Límite de elementos de actividad reciente (defecto: 5)
        """
        try:
            print(f"[USER_COMPLETE_PROFILE] Solicitando perfil completo para usuario ID: {user_id}", file=sys.stderr)
            print(f"[USER_COMPLETE_PROFILE] Parámetros recibidos: {dict(request.query_params)}", file=sys.stderr)
            
            # Extraer parámetros de la solicitud
            current_user_id = request.query_params.get('currentUserId')
            include_following_status = request.query_params.get('includeFollowingStatus', 'false').lower() == 'true'
            include_top_rated_album = request.query_params.get('includeTopRatedAlbum', 'false').lower() == 'true'
            include_recent_activity = request.query_params.get('includeRecentActivity', 'false').lower() == 'true'
            activity_limit = int(request.query_params.get('activityLimit', 5))
            
            print(f"[USER_COMPLETE_PROFILE] Parámetros procesados:", file=sys.stderr)
            print(f"[USER_COMPLETE_PROFILE] - current_user_id: {current_user_id}", file=sys.stderr)
            print(f"[USER_COMPLETE_PROFILE] - include_following_status: {include_following_status}", file=sys.stderr)
            print(f"[USER_COMPLETE_PROFILE] - include_top_rated_album: {include_top_rated_album}", file=sys.stderr)
            print(f"[USER_COMPLETE_PROFILE] - include_recent_activity: {include_recent_activity}", file=sys.stderr)
            print(f"[USER_COMPLETE_PROFILE] - activity_limit: {activity_limit}", file=sys.stderr)
            
            # Enviar la solicitud al controlador
            return self.controller.get_complete_profile(
                user_id=user_id,
                current_user_id=current_user_id,
                include_following_status=include_following_status,
                include_top_rated_album=include_top_rated_album,
                include_recent_activity=include_recent_activity,
                activity_limit=activity_limit
            )
            
        except ValueError as e:
            print(f"[USER_COMPLETE_PROFILE] Error de valor en parámetros: {str(e)}", file=sys.stderr)
            return Response(
                {"error": f"Error en parámetros: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"[USER_COMPLETE_PROFILE] Error al procesar solicitud: {str(e)}", file=sys.stderr)
            logger.exception(f"Error obteniendo perfil completo para usuario {user_id}: {str(e)}")
            return Response(
                {"error": "Error al procesar la solicitud"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )