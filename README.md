# MyQx BFF (Backend For Frontend)

This project implements a BFF (Backend For Frontend) pattern using Django and Django REST Framework. The purpose of a BFF is to provide a specific API layer for a given frontend, optimizing calls to backend microservices and improving the development experience.

## Features

- REST API with Django REST Framework
- CORS configuration for frontend communication
- Reusable HTTP client for backend service communication
- Modular structure for adding new endpoints
- Environment variable-based configuration
- Comprehensive logging and error handling
- Authentication and authorization middleware
- Structured service layer with interfaces and implementations

## Project Structure

```
myqx-bff/
  ├── api/                          # Main API application
  │   ├── controllers/              # Business logic controllers
  │   ├── dtos/                     # Data Transfer Objects
  │   ├── exceptions/               # Custom exception classes
  │   ├── interfaces/               # Service interfaces definitions
  │   ├── middleware/               # Custom middleware components
  │   ├── models/                   # Data models
  │   ├── repositories/             # Data access layer
  │   ├── services/                 # Service implementations
  │   │   ├── implementations/      # Concrete service implementations
  │   │   └── interfaces/           # Service interface definitions
  │   ├── utils/                    # Utility functions
  │   ├── views/                    # API views and endpoints
  │   ├── serializers.py            # API serializers
  │   ├── urls.py                   # API routes
  │   └── auth_views.py             # Authentication views
  ├── myqx_bff/                     # Main project configuration
  │   ├── settings.py               # Django settings
  │   ├── urls.py                   # Main URL configuration
  │   └── wsgi.py                   # WSGI configuration
  ├── docs/                         # Project documentation
  ├── diagrames/                    # Architecture diagrams
  ├── logs/                         # Application logs
  ├── .env                          # Environment variables (not in production)
  ├── manage.py                     # Django management script
  └── README.md                     # This file
```

## Architecture Diagrams

The `diagrames/` folder contains comprehensive PlantUML architecture diagrams that illustrate the system's structure and data flow. These diagrams are available in both detailed and simplified versions:

### Simplified Diagrams (Recommended)

1. **estructura_general_simple.puml**: Overall architecture overview showing all layers of the Myqx-BFF system and their relationships.

2. **vistes_i_processament_simple.puml**: API views layer diagram showing request processing flow through controllers and services.

3. **controladors_i_vistes_simple.puml**: Relationship diagram between API views and business logic controllers, showing separation of concerns.

4. **serveis_i_interficies_simple.puml**: Service layer architecture showing services, their implementations, and interface contracts.

5. **repositoris_dtos_models_simple.puml**: Data access layer showing repositories, DTOs (Data Transfer Objects), and data models.

6. **utils_i_configuracio_simple.puml**: Utility components, exception handling, middleware, and configuration management.

7. **flux_peticions_simple.puml**: Sequence diagram showing the complete flow of a request through all system layers.

8. **index_simple.puml**: Index diagram providing an overview of all simplified diagrams.

### Detailed Diagrams

The same diagrams are available in detailed versions (without the `_simple` suffix) that include more granular information about each component.

### Diagram Styling

All diagrams use a consistent, clean style with:
- Rectangular package styling
- UML2 component styling
- Orthogonal line connections
- Explanatory notes instead of complex legends
- Clear component representations

### Viewing the Diagrams

You can visualize the diagrams using any PlantUML-compatible tool:

1. **VS Code Extensions**: Install the PlantUML extension to view diagrams directly in VS Code.
2. **Web Browser**: Use the [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/).
3. **Command Line**: Use the PlantUML executable to generate images.

```bash
java -jar plantuml.jar estructura_general_simple.puml
```

## Requirements

- Python 3.8+
- Django 5.1+
- Django REST Framework
- Requests library for HTTP communication
- Python-decouple for environment management

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure environment variables
6. Run migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`

## Usage

The BFF exposes REST endpoints at `/api/` that the frontend can consume. These endpoints communicate with backend services and optimize responses for the specific frontend.

### Available Endpoints

- `GET /api/health/` - Health check endpoint
- `POST /api/auth/login/` - User authentication
- `POST /api/auth/logout/` - User logout
- `GET /api/users/profile/` - User profile information
- `GET /api/users/{user_id}/following-status/` - Check if user is following another user
- `GET /api/albums/` - Album listings
- `GET /api/feed/` - User feed data

## Development

To add a new backend service:

1. Create a new interface in `api/interfaces/`
2. Create a new service implementation in `api/services/implementations/` extending the interface
3. Create a controller in `api/controllers/` to handle business logic
4. Create views in `api/views/` that use the controller
5. Register routes in `api/urls.py`
6. Add appropriate DTOs in `api/dtos/` if needed

### Error Handling

The application includes comprehensive error handling:
- Custom exception classes in `api/exceptions/`
- Structured error responses with appropriate HTTP status codes
- Detailed logging for debugging and monitoring
- Graceful fallbacks for external service failures

### Logging

Logs are written to the `logs/` directory and include:
- `access.log` - HTTP access logs
- `error.log` - Error and exception logs
- `myqx-bff.log` - General application logs
- `profile.log` - User profile and authentication logs

## Configuration

Configuration is loaded from the `.env` file. Important variables include:

- `DEBUG`: Debug mode (True/False)
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Allowed hosts
- `CORS_ALLOWED_ORIGINS`: Allowed origins for CORS
- `USERS_SERVICE_URL`: Backend users service URL
- `ALBUMS_SERVICE_URL`: Backend albums service URL
- `FEED_SERVICE_URL`: Backend feed service URL

## Testing

Run tests with:
```bash
python manage.py test
```

For detailed test coverage and logging verification, check the application logs during test execution to ensure proper error handling and service communication.

## Deployment

The project includes Docker configuration:
- `Dockerfile` for containerized deployment
- `docker-compose.yml` for local development with dependencies

Build and run with Docker:
```bash
docker-compose up --build
```

## Documentation

For detailed technical documentation including component descriptions and code examples, see:
- `docs/components_arquitectura.md` - Comprehensive component architecture documentation (in Catalan)
- `diagrames/README_SIMPLE.md` - PlantUML diagrams documentation (in Catalan)