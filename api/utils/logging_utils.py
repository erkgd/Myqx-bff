import logging
import sys
import datetime

def log_http_request(request, level='info', logger=None):
    """
    Registra una solicitud HTTP con información detallada para depuración.
    
    Args:
        request: Objeto HttpRequest de Django
        level: Nivel de log ('debug', 'info', 'warning', 'error', 'critical')
        logger: Instancia de logger a usar (si es None, se imprime a stderr)
    """
    try:
        # Información detallada de la solicitud para depuración
        client_ip = request.META.get('REMOTE_ADDR', 'unknown')
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
        request_method = request.method
        request_path = request.path
        query_params = dict(request.query_params) if hasattr(request, 'query_params') else dict(request.GET)
        
        log_message = f"""
[HTTP_REQUEST] ===========================================
[HTTP_REQUEST] {request_method} {request_path} HTTP/1.1
[HTTP_REQUEST] Timestamp: {datetime.datetime.now().isoformat()}
[HTTP_REQUEST] Cliente: {client_ip}
[HTTP_REQUEST] User-Agent: {user_agent}
[HTTP_REQUEST] Parámetros de consulta: {query_params}
[HTTP_REQUEST] ===========================================
        """
        
        # Imprimir a stderr para depuración inmediata
        print(log_message, file=sys.stderr)
        
        # Registrar usando el logger si se proporcionó
        if logger:
            if level == 'debug':
                logger.debug(log_message)
            elif level == 'info':
                logger.info(log_message)
            elif level == 'warning':
                logger.warning(log_message)
            elif level == 'error':
                logger.error(log_message)
            elif level == 'critical':
                logger.critical(log_message)
    
    except Exception as e:
        print(f"[ERROR_LOGGING] Error al registrar solicitud: {str(e)}", file=sys.stderr)
