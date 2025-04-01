import requests
from django.conf import settings
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .exceptions.api_exceptions import ApiException

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado para devolver respuestas de error
    en un formato consistente y amigable para aplicaciones Flutter.
    
    Args:
        exc: Excepción capturada
        context: Contexto de la excepción
        
    Returns:
        Response: Respuesta HTTP con formato estandarizado
    """
    # Primero, intentamos manejar la excepción con el manejador estándar de DRF
    response = exception_handler(exc, context)
    
    # Si ya tenemos una respuesta, la formateamos para Flutter
    if response is not None:
        error_data = {
            "success": False,
            "error": {
                "code": response.status_code,
                "message": "Error en la solicitud",
                "details": response.data
            }
        }
        response.data = error_data
        return response
    
    # Para nuestras excepciones personalizadas
    if isinstance(exc, ApiException):
        error_data = {
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": getattr(exc, 'errors', {})
            }
        }
        return Response(error_data, status=exc.code)
    
    # Para otras excepciones no manejadas
    error_message = str(exc)
    logger.error(f"Error no manejado: {error_message}")
    error_data = {
        "success": False,
        "error": {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Error interno del servidor",
            "details": error_message if settings.DEBUG else "Contacte al administrador del sistema"
        }
    }
    return Response(
        error_data, 
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


# Función auxiliar para respuestas exitosas con formato estándar
def create_response(data=None, message="Operación exitosa", status_code=status.HTTP_200_OK, meta=None):
    """
    Crea una respuesta HTTP con formato estándar para la aplicación Flutter.
    
    Args:
        data: Datos a devolver (opcional)
        message: Mensaje de éxito (opcional)
        status_code: Código de estado HTTP (opcional)
        meta: Metadatos adicionales como paginación (opcional)
        
    Returns:
        Response: Respuesta HTTP con formato estandarizado
    """
    response_data = {
        "success": True,
        "message": message,
        "data": data or {}
    }
    
    if meta:
        response_data["meta"] = meta
        
    return Response(response_data, status=status_code)


class ServiceClient:
    """
    Cliente base para realizar peticiones HTTP a servicios externos.
    Útil para el patrón BFF donde necesitamos comunicarnos con múltiples
    microservicios backend.
    """
    
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        
    def _make_request(self, method, endpoint, data=None, params=None, headers=None):
        """
        Realiza una petición HTTP al servicio externo.
        
        Args:
            method: Método HTTP (get, post, put, delete)
            endpoint: Endpoint a llamar (sin incluir base_url)
            data: Datos para enviar en el body (opcional)
            params: Parámetros de query (opcional)
            headers: Headers HTTP adicionales (opcional)
            
        Returns:
            Response: Objeto de respuesta de la librería requests
        """
        url = f"{self.base_url}{endpoint}"
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if headers:
            default_headers.update(headers)
            
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=default_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al comunicarse con el servicio externo: {e}")
            raise
            
    def get(self, endpoint, params=None, headers=None):
        """Realiza una petición GET"""
        return self._make_request('get', endpoint, params=params, headers=headers)
        
    def post(self, endpoint, data=None, params=None, headers=None):
        """Realiza una petición POST"""
        return self._make_request('post', endpoint, data=data, params=params, headers=headers)
        
    def put(self, endpoint, data=None, headers=None):
        """Realiza una petición PUT"""
        return self._make_request('put', endpoint, data=data, headers=headers)
        
    def delete(self, endpoint, headers=None):
        """Realiza una petición DELETE"""
        return self._make_request('delete', endpoint, headers=headers)


# Ejemplo de implementación de un cliente específico:
# 
# class UsersServiceClient(ServiceClient):
#     """Cliente para el servicio de usuarios"""
#     
#     def __init__(self):
#         super().__init__(base_url=settings.USERS_SERVICE_URL)
#         
#     def get_user(self, user_id):
#         """Obtiene un usuario por su ID"""
#         return self.get(f'/users/{user_id}').json()
#         
#     def get_all_users(self):
#         """Obtiene todos los usuarios"""
#         return self.get('/users').json()