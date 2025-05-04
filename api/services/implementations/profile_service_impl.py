from typing import Dict, Any, List, Optional
from django.conf import settings
from ..base_service import BaseService
from ...interfaces.profile_service_interface import ProfileServiceInterface
import logging
import sys
import datetime
import json

logger = logging.getLogger(__name__)

class ProfileServiceImpl(BaseService, ProfileServiceInterface):
    """
    Implementación del servicio de perfiles que se comunica con el backend.
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la URL base y el timeout configurados.
        """
        base_url = getattr(settings, 'USERS_SERVICE_URL', None)  # Usar la misma URL que el servicio de usuarios
        timeout = getattr(settings, 'SERVICES_TIMEOUT', 30)
        super().__init__(base_url=base_url, timeout=timeout)
    
    def get_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene el perfil de un usuario específico.
        
        Args:
            user_id: ID del usuario del que se quiere obtener el perfil
            
        Returns:
            Dict: Datos del perfil del usuario
        """
        try:
            print(f"[PROFILE_SERVICE] Obteniendo perfil para usuario: {user_id}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Construir la URL para obtener el perfil
            endpoint_url = f"/profile/{user_id}"
            print(f"[PROFILE_SERVICE] Realizando solicitud GET a: {endpoint_url}", file=sys.stderr)
            
            response = self.get(endpoint_url, headers=headers)
              # Verificar y formatear la respuesta
            if isinstance(response, dict):
                print(f"[PROFILE_SERVICE] Perfil obtenido con éxito para usuario {user_id}", file=sys.stderr)
                
                # Log detallado de la respuesta para depuración
                log_message = f"""
[PROFILE_SERVICE] ===== DATOS RECIBIDOS DEL BACKEND =====
[PROFILE_SERVICE] Timestamp: {datetime.datetime.now().isoformat()}
[PROFILE_SERVICE] Usuario: {user_id}
[PROFILE_SERVICE] Datos:
{json.dumps(response, indent=2)}
[PROFILE_SERVICE] =======================================
                """
                print(log_message, file=sys.stderr)
                logger.info(log_message)
                
                return response
            else:
                print(f"[PROFILE_SERVICE] Formato de respuesta inesperado: {type(response)}", file=sys.stderr)
                return {"error": "Formato de respuesta no válido"}
                
        except Exception as e:
            logger.error(f"Error al obtener perfil del usuario {user_id}: {str(e)}")
            print(f"[PROFILE_SERVICE] Error: {str(e)}", file=sys.stderr)
            self._handle_error(f"Error al obtener perfil de usuario {user_id}", e)
            return {"error": f"Error al obtener perfil: {str(e)}"}
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza el perfil de un usuario.
        
        Args:
            user_id: ID del usuario cuyo perfil se va a actualizar
            profile_data: Datos nuevos para el perfil
            
        Returns:
            Dict: Datos actualizados del perfil
        """
        try:
            print(f"[PROFILE_SERVICE] Actualizando perfil para usuario: {user_id}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Construir la URL para actualizar el perfil
            endpoint_url = f"/profile/{user_id}"
            print(f"[PROFILE_SERVICE] Realizando solicitud PUT a: {endpoint_url}", file=sys.stderr)
            print(f"[PROFILE_SERVICE] Datos a enviar: {profile_data}", file=sys.stderr)
            
            response = self.put(endpoint_url, data=profile_data, headers=headers)
            
            # Verificar y formatear la respuesta
            if isinstance(response, dict):
                print(f"[PROFILE_SERVICE] Perfil actualizado con éxito para usuario {user_id}", file=sys.stderr)
                return response
            else:
                print(f"[PROFILE_SERVICE] Formato de respuesta inesperado: {type(response)}", file=sys.stderr)
                return {"error": "Formato de respuesta no válido"}
                
        except Exception as e:
            logger.error(f"Error al actualizar perfil del usuario {user_id}: {str(e)}")
            print(f"[PROFILE_SERVICE] Error: {str(e)}", file=sys.stderr)
            self._handle_error(f"Error al actualizar perfil de usuario {user_id}", e)
            return {"error": f"Error al actualizar perfil: {str(e)}"}
    
    def get_extended_profile(self, user_id: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Obtiene un perfil extendido con información adicional basada en las opciones.
        
        Args:
            user_id: ID del usuario del que se quiere obtener el perfil
            options: Opciones para personalizar la información que se incluye
            
        Returns:
            Dict: Datos extendidos del perfil
        """
        try:
            print(f"[PROFILE_SERVICE] Obteniendo perfil extendido para usuario: {user_id}", file=sys.stderr)
            if options:
                print(f"[PROFILE_SERVICE] Opciones: {options}", file=sys.stderr)
            
            # Preparar headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Construir la URL con parámetros opcionales
            endpoint_url = f"/profile/{user_id}/extended"
            print(f"[PROFILE_SERVICE] Realizando solicitud GET a: {endpoint_url}", file=sys.stderr)
            
            response = self.get(endpoint_url, params=options, headers=headers)
            
            # Verificar y formatear la respuesta
            if isinstance(response, dict):
                print(f"[PROFILE_SERVICE] Perfil extendido obtenido con éxito para usuario {user_id}", file=sys.stderr)
                return response
            else:
                print(f"[PROFILE_SERVICE] Formato de respuesta inesperado: {type(response)}", file=sys.stderr)
                return {"error": "Formato de respuesta no válido"}
                
        except Exception as e:
            logger.error(f"Error al obtener perfil extendido del usuario {user_id}: {str(e)}")
            print(f"[PROFILE_SERVICE] Error: {str(e)}", file=sys.stderr)
            self._handle_error(f"Error al obtener perfil extendido de usuario {user_id}", e)
            return {"error": f"Error al obtener perfil extendido: {str(e)}"}
    
    def _handle_error(self, message: str, exception: Exception = None):
        """
        Maneja los errores del servicio de perfiles de manera uniforme.
        
        Args:
            message: Mensaje descriptivo del error
            exception: Excepción que ocurrió (opcional)
        """
        error_msg = message
        if exception:
            error_msg = f"{message}: {str(exception)}"
        
        logger.error(error_msg)
        if exception:
            logger.debug(f"Detalle de la excepción: {exception}", exc_info=True)
        
        # Imprimir a stderr para depuración inmediata
        print(f"[PROFILE_SERVICE] ERROR: {error_msg}", file=sys.stderr)
        
        # Si es una excepción que debería propagarse, relanzarla
        if exception and isinstance(exception, (ValueError, TypeError)):
            raise exception
