# Utilidades para crear respuestas estandarizadas
import datetime
from rest_framework.response import Response
from rest_framework import status

def create_response(data=None, message=None, status_code=status.HTTP_200_OK, error=None, meta=None):
    """
    Función auxiliar para crear respuestas HTTP con formato estandarizado para el frontend.
    
    Args:
        data: Datos a devolver en la respuesta
        message: Mensaje descriptivo de la respuesta
        status_code: Código de estado HTTP
        error: Mensaje de error (si aplica)
        meta: Metadatos adicionales (paginación, conteo, etc.)
        
    Returns:
        Response: Objeto Response con formato estandarizado
    """
    response_data = {
        'status': 'success' if error is None else 'error',
        'timestamp': datetime.datetime.now().isoformat(),
        'message': message or ('Operación completada con éxito' if error is None else 'Error en la operación')
    }
    
    if data is not None:
        response_data['data'] = data
        
    if error:
        response_data['error'] = error
        
    if meta is not None:
        response_data['meta'] = meta
        
    return Response(response_data, status=status_code)
