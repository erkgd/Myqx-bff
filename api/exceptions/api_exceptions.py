class ApiException(Exception):
    """
    Excepción base para todas las excepciones de la API.
    """
    def __init__(self, message="Error en la API", code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ResourceNotFoundException(ApiException):
    """
    Excepción para cuando un recurso no se encuentra.
    """
    def __init__(self, resource="Recurso", resource_id=None):
        message = f"{resource} no encontrado"
        if resource_id:
            message = f"{resource} con id {resource_id} no encontrado"
        super().__init__(message=message, code=404)


class ValidationException(ApiException):
    """
    Excepción para errores de validación.
    """
    def __init__(self, message="Error de validación", errors=None):
        self.errors = errors or {}
        super().__init__(message=message, code=400)


class AuthenticationException(ApiException):
    """
    Excepción para errores de autenticación.
    """
    def __init__(self, message="Error de autenticación"):
        super().__init__(message=message, code=401)


class ServiceUnavailableException(ApiException):
    """
    Excepción para cuando un servicio externo no está disponible.
    """
    def __init__(self, service="Servicio externo"):
        message = f"{service} no disponible"
        super().__init__(message=message, code=503)