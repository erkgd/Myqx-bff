from django.http import HttpResponseRedirect
from django.urls import resolve, Resolver404
import re

class ApiRedirectMiddleware:
    """
    Middleware que redirige las solicitudes que no coinciden con ninguna URL definida
    a su equivalente en /api/ si existe.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Excluir solicitudes que ya están en /api/
        if request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Excluir rutas administrativas y estáticas
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Excluir rutas que ya tienen una redirección definida
        known_redirects = ['/feed', '/feed/', '/ratings/submit', '/ratings/submit/']
        if request.path in known_redirects:
            return self.get_response(request)
        
        try:
            # Intentar resolver la URL original
            resolve(request.path)
            # Si no lanza una excepción, significa que la URL existe
            return self.get_response(request)
        except Resolver404:
            # La URL no existe, intentar redirigir a /api/
            api_path = '/api' + request.path
            try:
                # Verificar si la URL con /api/ existe
                resolve(api_path)
                # Si existe, redirigir
                return HttpResponseRedirect(api_path)
            except Resolver404:
                # Ni la URL original ni la URL con /api/ existen
                pass
            
        # Si llegamos aquí, continuar con la solicitud normal
        return self.get_response(request)
