from typing import Dict, Any, List, Optional
from rest_framework import status
from rest_framework.request import Request
from ..repositories.user_repository import UserRepository
from ..exceptions.api_exceptions import ResourceNotFoundException, ValidationException
from ..utils.response_utils import create_response
import logging
import sys
import datetime

logger = logging.getLogger(__name__)

class ProfileController:
    """
    Controlador para manejar operaciones relacionadas con perfiles de usuarios.
    Proporciona métodos para obtener y actualizar perfiles.
    """
    
    def __init__(self):
        """
        Constructor del controlador de perfiles.
        """
        from ..services.implementations.profile_service_impl import ProfileServiceImpl
        self.profile_service = ProfileServiceImpl()
        self.user_repository = UserRepository()  # Para verificar existencia de usuarios
    
    def get_profile(self, user_id: str):
        """
        Obtiene el perfil de un usuario.
        
        Args:
            user_id: ID del usuario cuyo perfil se desea obtener
            
        Returns:
            Response: Respuesta HTTP con los datos del perfil o error
        """
        try:
            print(f"[PROFILE_CONTROLLER] Obteniendo perfil para usuario {user_id}", file=sys.stderr)
            
            # Primero verificamos que el usuario existe
            user = self.user_repository.find_by_id(user_id)
            if not user:
                print(f"[PROFILE_CONTROLLER] Usuario con ID {user_id} no encontrado", file=sys.stderr)
                raise ResourceNotFoundException("Usuario", user_id)
            
            # Obtener el perfil usando el servicio
            profile_data = self.profile_service.get_profile(user_id)
            
            # Si hay un error en el servicio
            if "error" in profile_data:
                print(f"[PROFILE_CONTROLLER] Error desde el servicio: {profile_data['error']}", file=sys.stderr)
                return create_response(
                    data=None,
                    message=profile_data['error'],
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error=profile_data['error']
                )
              # Si todo está bien, devolver los datos
            print(f"[PROFILE_CONTROLLER] Perfil obtenido con éxito para usuario {user_id}", file=sys.stderr)
            
            # Creamos la respuesta
            response = create_response(
                data=profile_data,
                message="Perfil de usuario obtenido con éxito",
                status_code=status.HTTP_200_OK
            )
            
            # Registrar detalles de la respuesta para depuración
            import json
            response_data = json.dumps(response.data, indent=2) if hasattr(response, 'data') else "No hay datos disponibles"
            log_message = f"""
[PROFILE_CONTROLLER] ===== RESPUESTA =====
[PROFILE_CONTROLLER] Status: {response.status_code}
[PROFILE_CONTROLLER] Timestamp: {datetime.datetime.now().isoformat()}
[PROFILE_CONTROLLER] Payload:
{response_data}
[PROFILE_CONTROLLER] =======================
            """
            print(log_message, file=sys.stderr)
            logger.info(log_message)
            
            return response
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            # Log del error y devolver respuesta genérica
            error_msg = f"Error al obtener perfil de usuario {user_id}: {str(e)}"
            logger.exception(error_msg)
            print(f"[PROFILE_CONTROLLER] Error: {error_msg}", file=sys.stderr)
            return create_response(
                data=None,
                message="Error al obtener perfil de usuario",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )
    
    def update_profile(self, user_id: str, update_data: Dict[str, Any]):
        """
        Actualiza el perfil de un usuario.
        
        Args:
            user_id: ID del usuario cuyo perfil se va a actualizar
            update_data: Datos a actualizar en el perfil
            
        Returns:
            Response: Respuesta HTTP con los datos actualizados del perfil o error
        """
        try:
            print(f"[PROFILE_CONTROLLER] Actualizando perfil para usuario {user_id}", file=sys.stderr)
            print(f"[PROFILE_CONTROLLER] Datos a actualizar: {update_data}", file=sys.stderr)
            
            # Primero verificamos que el usuario existe
            user = self.user_repository.find_by_id(user_id)
            if not user:
                print(f"[PROFILE_CONTROLLER] Usuario con ID {user_id} no encontrado", file=sys.stderr)
                raise ResourceNotFoundException("Usuario", user_id)
            
            # Actualizar el perfil usando el servicio
            updated_profile = self.profile_service.update_profile(user_id, update_data)
            
            # Si hay un error en el servicio
            if "error" in updated_profile:
                print(f"[PROFILE_CONTROLLER] Error desde el servicio: {updated_profile['error']}", file=sys.stderr)
                return create_response(
                    data=None,
                    message=updated_profile['error'],
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error=updated_profile['error']
                )
            
            # Si todo está bien, devolver los datos actualizados
            print(f"[PROFILE_CONTROLLER] Perfil actualizado con éxito para usuario {user_id}", file=sys.stderr)
            return create_response(
                data=updated_profile,
                message="Perfil de usuario actualizado con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except ValidationException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            # Log del error y devolver respuesta genérica
            error_msg = f"Error al actualizar perfil de usuario {user_id}: {str(e)}"
            logger.exception(error_msg)
            print(f"[PROFILE_CONTROLLER] Error: {error_msg}", file=sys.stderr)
            return create_response(
                data=None,
                message="Error al actualizar perfil de usuario",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )
