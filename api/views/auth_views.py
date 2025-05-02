from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..controllers.auth_controller import AuthController
import datetime
import logging
import sys

class AuthView(APIView):
    """
    Base class for authentication related endpoints
    """
    permission_classes = [AllowAny]


class AuthTestView(APIView):
    """
    Endpoint para probar la autenticación.
    Requiere un token JWT para acceder.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """
        Retorna un mensaje de éxito indicando que el usuario está autenticado.
        """
        data = {
            'authenticated': True,
            'user': request.user.username if hasattr(request.user, 'username') else str(request.user),
            'timestamp': datetime.datetime.now().isoformat()
        }
        return Response(data, status=status.HTTP_200_OK)


class SpotifyAuthView(APIView):
    """
    Endpoint para autenticación con Spotify.
    Recibe el token de Spotify y devuelve un token JWT de la aplicación.
    """
    permission_classes = [AllowAny]
    
    def __init__(self):
        """
        Inicializa el controlador de autenticación
        """
        self.controller = AuthController()
        super().__init__()
    
    def post(self, request, format=None):
        """
        Autentica con token de Spotify y crea sesión
        """
        import sys
        
        # Banner para identificar claramente inicio de la petición
        print("\n" + "="*80, file=sys.stderr)
        print(f"[SPOTIFY_AUTH] INICIO PROCESO DE AUTENTICACIÓN SPOTIFY - {datetime.datetime.now().isoformat()}", file=sys.stderr)
        print("="*80, file=sys.stderr)
        
        # Registrar información de la petición
        print(f"[SPOTIFY_AUTH] IP cliente: {request.META.get('REMOTE_ADDR')}", file=sys.stderr)
        print(f"[SPOTIFY_AUTH] User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}", file=sys.stderr)
        
        # Registrar datos recibidos del frontend (con cuidado de la información sensible)
        print(f"[SPOTIFY_AUTH] Datos recibidos del frontend:", file=sys.stderr)
        print(f"[SPOTIFY_AUTH] - Claves en los datos: {list(request.data.keys())}", file=sys.stderr)
        
        # Mostrar información específica que nos interesa (sin revelar tokens)
        if 'spotifyToken' in request.data:
            print(f"[SPOTIFY_AUTH] - spotifyToken recibido (longitud): {len(str(request.data['spotifyToken']))}", file=sys.stderr)
        elif 'token' in request.data:
            print(f"[SPOTIFY_AUTH] - token recibido (longitud): {len(str(request.data['token']))}", file=sys.stderr)
        elif 'access_token' in request.data:
            print(f"[SPOTIFY_AUTH] - access_token recibido (longitud): {len(str(request.data['access_token']))}", file=sys.stderr)
            
        # Mostrar otros campos relevantes (datos no sensibles)
        safe_fields = ['username', 'email', 'profilePhoto', 'spotifyId']
        for field in safe_fields:
            if field in request.data:
                print(f"[SPOTIFY_AUTH] - {field}: {request.data[field]}", file=sys.stderr)
        
        # Para los logs estándar
        logger = logging.getLogger(__name__)
        logger.info(f"Recibida petición de autenticación Spotify desde: {request.META.get('REMOTE_ADDR')}")
        logger.info(f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        
        # Registrar headers para los logs
        safe_headers = {
            k: v for k, v in request.headers.items() 
            if k.lower() not in ['authorization', 'cookie']
        }
        logger.debug(f"Headers recibidos: {safe_headers}")
        print(f"[SPOTIFY_AUTH] Headers principales: Content-Type={request.headers.get('Content-Type')}, Accept={request.headers.get('Accept')}", file=sys.stderr)
        
        # Datos seguros para logs
        safe_data = {
            k: "***" if k in ['spotify_token', 'spotifyToken', 'token', 'access_token'] else v 
            for k, v in request.data.items()
        }
        logger.debug(f"Datos recibidos (sin tokens): {safe_data}")
        
        # Usar el controlador para procesar la autenticación
        response = self.controller.authenticate_with_spotify(request.data)
        
        # Normalizar campos de imagen en la respuesta para mantener consistencia con el frontend
        if hasattr(response, 'data') and 'user' in response.data:
            user_data = response.data['user']
            
            # Asegurar que tanto profilePhoto como profileImage estén presentes en la respuesta
            profile_image = user_data.get('profileImage')
            profile_photo = user_data.get('profilePhoto')
            
            # Si solo uno de los campos está presente, copiar su valor al otro
            if profile_image and not profile_photo:
                user_data['profilePhoto'] = profile_image
                print(f"[SPOTIFY_AUTH] Normalización: Añadido campo profilePhoto", file=sys.stderr)
            elif profile_photo and not profile_image:
                user_data['profileImage'] = profile_photo
                print(f"[SPOTIFY_AUTH] Normalización: Añadido campo profileImage", file=sys.stderr)
        
        # Registrar respuesta (sin información sensible)
        if hasattr(response, 'data'):
            response_data = dict(response.data)  # Crear una copia para no modificar la respuesta real
            if 'token' in response_data:
                response_data['token'] = "***" 
            print(f"[SPOTIFY_AUTH] Respuesta enviada al frontend (status {response.status_code}):", file=sys.stderr)
            import json
            print(f"[SPOTIFY_AUTH] {json.dumps(response_data, indent=2)}", file=sys.stderr)
        
        print("[SPOTIFY_AUTH] " + "="*70, file=sys.stderr)
        print(f"[SPOTIFY_AUTH] FIN PROCESO DE AUTENTICACIÓN SPOTIFY - {datetime.datetime.now().isoformat()}", file=sys.stderr) 
        print("="*80 + "\n", file=sys.stderr)
        
        return response
