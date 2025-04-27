# Este archivo permite que Python trate el directorio como un paquete
"""
Controladores para el BFF de MyQx.
Los controladores actúan como intermediarios entre las rutas y los servicios,
implementando la lógica de negocio específica de la API.
"""

# Exportar los controladores para que sean fácilmente accesibles
from .users_controller import UsersController
from .albums_controller import AlbumsController
from .auth_controller import AuthController