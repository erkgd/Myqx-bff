# Custom exception handler for DRF
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import datetime

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
            "status": "error",
            "timestamp": datetime.datetime.now().isoformat(),
            "message": "Error al procesar la solicitud",
            "error": str(exc),
        }
        
        # Si la respuesta original tiene datos, los incluimos
        if hasattr(response, 'data') and response.data:
            if isinstance(response.data, dict) and 'detail' in response.data:
                error_data['error'] = response.data['detail']
            elif isinstance(response.data, dict):
                error_data['details'] = response.data
        
        return Response(error_data, status=response.status_code)
    
    # Si no hay respuesta, es una excepción no manejada por DRF
    logger.error(f"Excepción no manejada: {exc}", exc_info=True)
    error_data = {
        "status": "error",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "Error interno del servidor",
        "error": str(exc),
    }
    return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
