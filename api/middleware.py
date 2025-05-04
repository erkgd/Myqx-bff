# Este archivo está obsoleto - importar los middlewares desde api.middleware
from .middleware import ApiRedirectMiddleware, RequestLoggingMiddleware

# Exportar los middlewares para mantener compatibilidad con código existente
__all__ = ['ApiRedirectMiddleware', 'RequestLoggingMiddleware']
