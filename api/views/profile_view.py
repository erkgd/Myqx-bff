from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..controllers.profile_controller import ProfileController
from ..utils import log_http_request
import logging
import sys
import datetime
import time

logger = logging.getLogger(__name__)

class ProfileView(APIView):
    """
    Endpoint para operaciones relacionadas con el perfil de un usuario.
    Permite obtener y actualizar la información del perfil.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = ProfileController()
    
    def get(self, request, user_id=None, format=None):
        """
        Obtiene el perfil de un usuario específico.
        
        Si no se proporciona user_id, se intentará obtener del token de autenticación.
        """
        try:
            # Información detallada de la solicitud para depuración
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            request_method = request.method
            request_path = request.path
            query_params = dict(request.query_params)
            
            log_message = f"""
[PROFILE_VIEW] ===========================================
[PROFILE_VIEW] {request_method} {request_path} HTTP/1.1
[PROFILE_VIEW] Timestamp: {datetime.datetime.now().isoformat()}
[PROFILE_VIEW] Cliente: {client_ip}
[PROFILE_VIEW] User-Agent: {user_agent}
[PROFILE_VIEW] Parámetros de consulta: {query_params}
[PROFILE_VIEW] Usuario objetivo: {user_id}
[PROFILE_VIEW] ===========================================
            """
            print(log_message, file=sys.stderr)
            logger.info(log_message)
            
            # Si no se proporciona user_id, intentar obtenerlo del usuario autenticado
            if not user_id and request.user and hasattr(request.user, 'id'):
                user_id = request.user.id
                print(f"[PROFILE_VIEW] Usando ID de usuario autenticado: {user_id}", file=sys.stderr)
            
            if not user_id:
                print("[PROFILE_VIEW] No se proporcionó ID de usuario y no hay usuario autenticado", file=sys.stderr)
                return Response(
                    {"error": "Se requiere ID de usuario"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Llamar al controlador para obtener el perfil
            return self.controller.get_profile(user_id)
            
        except Exception as e:
            error_msg = f"Error al procesar solicitud de perfil: {str(e)}"
            logger.exception(error_msg)
            print(f"[PROFILE_VIEW] Error: {error_msg}", file=sys.stderr)
            return Response(
                {"error": "Error al procesar la solicitud"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request, user_id=None, format=None):
        """
        Actualiza el perfil completo de un usuario.
        
        Si no se proporciona user_id, se intentará obtener del token de autenticación.
        """
        request_start_time = datetime.datetime.now()
        request_id = f"profile-update-{request_start_time.strftime('%Y%m%d%H%M%S')}-{id(request)}"
        
        # Formato de log inicial
        log_prefix = f"[PROFILE_UPDATE:{request_id}]"
        
        # Log de inicio de petición
        request_log = {
            "timestamp": request_start_time.isoformat(),
            "method": request.method,
            "path": request.path,
            "user_id": user_id,
            "content_type": request.content_type,
            "data_size": len(json.dumps(request.data)) if not isinstance(request.data, QueryDict) else sum(len(v) for v in request.data.values()),
            "remote_addr": request.META.get('REMOTE_ADDR', ''),
            "request_id": request_id
        }
        
        print(f"{log_prefix} INICIO PETICIÓN: {json.dumps(request_log, indent=2)}", file=sys.stderr)
        logger.info(f"{log_prefix} Petición recibida: {request.method} {request.path}")
        
        try:
            # Si no se proporciona user_id, intentar obtenerlo del usuario autenticado
            if not user_id and request.user and hasattr(request.user, 'id'):
                user_id = request.user.id
                print(f"{log_prefix} Usando ID de usuario autenticado: {user_id}", file=sys.stderr)
            
            if not user_id:
                print(f"{log_prefix} No se proporcionó ID de usuario y no hay usuario autenticado", file=sys.stderr)
                
                response_data = {"error": "Se requiere ID de usuario"}
                response_log = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "response_data": response_data,
                    "processing_time_ms": (datetime.datetime.now() - request_start_time).total_seconds() * 1000
                }
                print(f"{log_prefix} FIN PETICIÓN (ERROR): {json.dumps(response_log, indent=2)}", file=sys.stderr)
                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar que se proporcionaron datos para actualizar
            if not request.data:
                print(f"{log_prefix} No se proporcionaron datos para actualizar el perfil", file=sys.stderr)
                
                response_data = {"error": "No se proporcionaron datos para actualizar"}
                response_log = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "response_data": response_data,
                    "processing_time_ms": (datetime.datetime.now() - request_start_time).total_seconds() * 1000
                }
                print(f"{log_prefix} FIN PETICIÓN (ERROR): {json.dumps(response_log, indent=2)}", file=sys.stderr)
                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"{log_prefix} Llamando al controlador para actualizar perfil de usuario ID: {user_id}", file=sys.stderr)
            
            # Llamar al controlador para actualizar el perfil
            controller_response = self.controller.update_profile(user_id, request.data)
            
            # Log de respuesta exitosa
            response_log = {
                "timestamp": datetime.datetime.now().isoformat(),
                "status_code": controller_response.status_code,
                "user_id": user_id,
                "processing_time_ms": (datetime.datetime.now() - request_start_time).total_seconds() * 1000
            }
            print(f"{log_prefix} FIN PETICIÓN (ÉXITO): {json.dumps(response_log, indent=2)}", file=sys.stderr)
            logger.info(f"{log_prefix} Petición procesada: {request.method} {request.path} - Status: {controller_response.status_code}")
            
            return controller_response
            
        except Exception as e:
            error_msg = f"Error al procesar actualización de perfil: {str(e)}"
            stack_trace = traceback.format_exc()
            
            # Log detallado del error
            error_log = {
                "timestamp": datetime.datetime.now().isoformat(),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "user_id": user_id,
                "error_msg": str(e),
                "error_type": type(e).__name__,
                "processing_time_ms": (datetime.datetime.now() - request_start_time).total_seconds() * 1000
            }
            
            print(f"{log_prefix} FIN PETICIÓN (ERROR): {json.dumps(error_log, indent=2)}", file=sys.stderr)
            print(f"{log_prefix} STACK TRACE: \n{stack_trace}", file=sys.stderr)
            
            logger.exception(f"{log_prefix} Error procesando petición: {request.method} {request.path}")
            
            return Response(
                {"error": "Error al procesar la solicitud"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request, user_id=None, format=None):
        """
        Actualiza parcialmente el perfil de un usuario.
        
        Utiliza el mismo método que put porque ambos actualizan,
        la diferencia conceptual es manejada por el cliente.
        """
        return self.put(request, user_id, format)
