# MyQx BFF (Backend For Frontend)

Este proyecto implementa un patrón BFF (Backend For Frontend) utilizando Django y Django REST Framework. El propósito de un BFF es proporcionar una capa de API específica para un frontend determinado, optimizando las llamadas a microservicios backend y mejorando la experiencia de desarrollo.

## Características

- API REST con Django REST Framework
- Configuración de CORS para comunicación con frontend
- Cliente HTTP reutilizable para comunicación con servicios backend
- Estructura modular para agregar nuevos endpoints
- Configuración basada en variables de entorno

## Estructura del proyecto

```
myqx-bff/
  ├── api/                    # Aplicación principal de API
  │   ├── services/           # Clientes para servicios backend
  │   │   ├── base_service.py # Clase base para servicios HTTP
  │   │   └── users_service.py # Ejemplo de servicio de usuarios
  │   ├── models.py           # Modelos de datos (si son necesarios)
  │   ├── serializers.py      # Serializadores para la API
  │   ├── urls.py             # Rutas de la API
  │   ├── utils.py            # Utilidades generales
  │   └── views.py            # Vistas de la API
  ├── myqx_bff/               # Configuración principal del proyecto
  │   ├── settings.py         # Configuración de Django
  │   ├── urls.py             # URLs principales
  │   └── wsgi.py             # Configuración WSGI
  ├── .env                    # Variables de entorno (no comitear en producción)
  ├── manage.py               # Script de administración de Django
  └── README.md               # Este archivo
```

## Requisitos

- Python 3.8+
- Django 5.1+
- Django REST Framework

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Copiar `.env.example` a `.env` y configurar variables de entorno
6. Ejecutar migraciones: `python manage.py migrate`
7. Iniciar el servidor: `python manage.py runserver`

## Uso

El BFF expone endpoints REST en `/api/` que el frontend puede consumir. Estos endpoints se comunican con los servicios backend y optimizan las respuestas para el frontend específico.

### Ejemplo de endpoints

- `GET /api/health/` - Verificar estado del servicio

## Desarrollo

Para añadir un nuevo servicio backend:

1. Crear un nuevo archivo en `api/services/` extendiendo `BaseService`
2. Implementar métodos específicos para comunicarse con el servicio
3. Crear vistas en `api/views.py` que utilicen el servicio
4. Registrar las rutas en `api/urls.py`

## Configuración

Las variables de configuración se cargan desde el archivo `.env`. Algunas variables importantes son:

- `DEBUG`: Modo de depuración (True/False)
- `SECRET_KEY`: Clave secreta de Django
- `ALLOWED_HOSTS`: Hosts permitidos
- `CORS_ALLOWED_ORIGINS`: Orígenes permitidos para CORS