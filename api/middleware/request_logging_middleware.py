import time
import json
import sys
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware para registrar información detallada de todas las peticiones HTTP.
    Incluye tiempos de respuesta, detalles de la petición y formato JSON para depuración.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Generar un ID único para esta petición
        request_id = str(uuid.uuid4())[:8]
        request.request_id = request_id
        
        # Registrar inicio de la petición
        start_time = time.time()
        timestamp = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        
        # Obtener información de la petición
        path = request.path
        method = request.method
        
        # Construir el log inicial
        request_log = {
            "timestamp": timestamp,
            "request_id": request_id,
            "method": method,
            "path": path,
            "query_params": dict(request.GET),
            "remote_addr": request.META.get('REMOTE_ADDR', 'unknown'),
            "user_agent": request.META.get('HTTP_USER_AGENT', 'unknown'),
            "content_type": request.content_type,
            "content_length": request.META.get('CONTENT_LENGTH', '0'),
        }
        
        # Log en formato similar al de Django pero con información extra
        print(f"[REQUEST:{request_id}] INICIO - {timestamp} \"{method} {path} HTTP/{request.META.get('SERVER_PROTOCOL', '1.1').split('/')[-1]}\"", file=sys.stderr)
        
        # Procesar la petición
        response = self.get_response(request)
        
        # Registrar fin de la petición
        processing_time = time.time() - start_time
        end_timestamp = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
        
        # Construir el log de respuesta
        response_log = {
            "timestamp": end_timestamp,
            "request_id": request_id,
            "status_code": response.status_code,
            "processing_time_ms": round(processing_time * 1000, 2),
            "content_type": response.get('Content-Type', 'unknown'),
            "content_length": response.get('Content-Length', 'unknown'),
        }
        
        # Log en formato similar al de Django pero con información extra
        print(f"[REQUEST:{request_id}] FIN - {end_timestamp} \"{method} {path} HTTP/{request.META.get('SERVER_PROTOCOL', '1.1').split('/')[-1]}\" {response.status_code} - {round(processing_time * 1000, 2)}ms", file=sys.stderr)
        
        # Log detallado para depuración
        log_entry = {
            "request": request_log,
            "response": response_log,
        }
        
        # Guardar en logs solo si es necesario (depuración)
        if response.status_code >= 400:  # Solo para respuestas de error
            logger.warning(f"Request failed: {json.dumps(log_entry)}")
        
        return response
