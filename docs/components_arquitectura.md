# Components de la Solució Myqx-BFF

## 1. Processament de Peticions (Middleware)

### Descripció Funcional
Actua com a capa d'entrada per a totes les peticions HTTP dirigides al sistema. Els components principals són:

- **ApiRedirectMiddleware**: Redirigeix automàticament les peticions sense el prefix `/api/` al seu equivalent.
- **RequestLoggingMiddleware**: Registra informació detallada sobre les peticions i les respostes.

### Tecnologies Utilitzades
S'ha implementat utilitzant el sistema de middleware de Django, en comptes d'altres alternatives, pels següents motius:
- Integració nativa amb el framework Django.
- Capacitat per a executar-se en una seqüència determinada.
- Accés complet a les peticions HTTP i les seves respostes.

### Problemes i Solucions
**Problema**: Algunes rutes especials generaven redireccionaments incorrectes.
**Solució**: Implementació d'una llista d'exclusions per a les rutes que no s'han de redirigir.

```python
class ApiRedirectMiddleware:
    """
    Middleware que redirigeix les solicituds que no coincideixen amb ninguna URL definida
    a su equivalent en /api/ si existeix.
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
            
        # Intentar redirigir a la versió amb /api/ prefix
        api_path = f"/api{request.path}"
        try:
            resolve(api_path)
            return HttpResponseRedirect(api_path)
        except Resolver404:
            return self.get_response(request)
```

## 2. Vistes API

### Descripció Funcional
Les vistes defineixen els endpoints REST exposats per l'aplicació. Gestionen:
- Serialització i deserialització de dades
- Validació d'entrada i gestió d'errors
- Enrutament a controladors adequats

### Tecnologies Utilitzades
S'ha implementat utilitzant Django REST Framework (DRF) per:
- Sistema potent de serialització i validació
- Integració amb l'autenticació de Django
- Documentació automàtica (OpenAPI/Swagger)

### Problemes i Solucions
**Problema**: Manca d'endpoints per a verificar l'estat de seguiment entre usuaris.
**Solució**: Creació d'una vista específica (`UserFollowingStatusView`) que accepta dos IDs d'usuari.

```python
class FeedView(APIView):
    """
    Endpoint para obtener el feed de un usuario.
    Proporciona la actividad reciente y relevante para el usuario.
    """
    permission_classes = [AllowAny]  # Puedes cambiar a IsAuthenticated según tus requisitos
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from .repositories.feed_repository import FeedRepository
        self.repository = FeedRepository()
    
    def __init__(self):
        self.controller = UsersController()
        
    def get(self, request, user_id):
        try:
            return self.controller.get_complete_profile(user_id)
        except Exception as e:
            return Response({
                "error": f"Error obtenint perfil complet: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

## 3. Controladors

### Descripció Funcional
Els controladors implementen la lògica de negoci del sistema. Són responsables de:
- Orquestrar operacions complexes entre serveis i repositoris
- Aplicar regles de negoci
- Transformar les dades entre vistes i serveis
- Gestionar errors i excepcions

### Tecnologies Utilitzades
S'han implementat com a classes Python estàndard, seguint el patró controlador, per:
- Facilitar els tests mitjançant injecció de dependències
- Separar la lògica de negoci de la presentació (vistes)
- Permetre la reutilització del codi

### Problemes i Solucions
**Problema**: Dificultat per gestionar les excepcions provinents de serveis externs.
**Solució**: Implementació d'un sistema d'excepcions personalitzades i un gestor central d'errors.

## 4. Interfícies de Servei

### Descripció Funcional
Les interfícies defineixen contractes que han de complir les implementacions dels serveis:
- Proporcionen abstracció i desacoblament
- Permeten múltiples implementacions (per exemple, per tests)

### Tecnologies Utilitzades
S'utilitzen classes abstractes de Python amb mètodes abstractes en comptes de protocols per:
- Compatibilitat amb diverses versions de Python
- Claredat en la documentació i codi

### Problemes i Solucions
**Problema**: Garantir que totes les implementacions compleixin amb la interfície.
**Solució**: Ús de mètodes abstractes (`@abstractmethod`) i test unitaris per verificar conformitat.

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class UserServiceInterface(ABC):
    """
    Interfaz para definir los métodos que debe implementar cualquier servicio de usuarios.
    Siguiendo el principio de inversión de dependencias, los controladores dependerán
    de esta interfaz en lugar de una implementación concreta.
    """
    
    @abstractmethod
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene un usuario por su ID desde el backend.
        
        Args:
            user_id: ID del usuario a obtener
            
        Returns:
            Dict que representa los datos del usuario
        """
        pass
    
    @abstractmethod
    def get_users(self, **params) -> List[Dict[str, Any]]:
        """
        Obtiene una lista de usuarios con filtros opcionales.
        """
        pass
```

## 5. Implementacions de Serveis

### Descripció Funcional
Els serveis implementen les operacions definides en les interfícies. S'encarreguen de:
- Comunicar-se amb APIs externes
- Transformar dades entre el format BFF i el format d'API externa
- Gestionar credencials i autenticació amb serveis externs

### Tecnologies Utilitzades
S'han implementat utilitzant:
- La biblioteca `requests` per a comunicacions HTTP
- Una classe base (`BaseService`) per a funcionalitat comuna
- Gestió de configuracions centralitzada

S'ha escollit aquesta aproximació en comptes de biblioteques asíncrones per:
- Compatibilitat amb l'arquitectura síncrona de Django
- Simplicitat en la implementació
- Facilitat de manteniment

### Problemes i Solucions
**Problema**: Timeouts i errors transitoris en les comunicacions amb APIs externes.
**Solució**: Implementació d'un sistema de retries amb backoff exponencial.

## 6. Repositoris

### Descripció Funcional
Els repositoris proporcionen una capa d'abstracció sobre l'accés a dades:
- Ofereixen mètodes CRUD per a les entitats del sistema
- Transformen DTOs en models i viceversa
- Permeten estratègies de caching

### Tecnologies Utilitzades
S'han implementat seguint el patró repositori estàndard, en comptes d'accés directe als models o serveis, per:
- Facilitar la testabilitat mitjançant mocks
- Permetre canvis en la font de dades sense afectar els consumidors
- Implementar estratègies de cache

### Problemes i Solucions
**Problema**: Complexitat en la transformació de dades entre diferents formats (API externa → DTO → Model).
**Solució**: Creació de mètodes auxiliars de transformació dins dels repositoris.

```python
class UserRepository:
    def __init__(self, users_service=None):
        self.users_service = users_service or UsersServiceImpl()
        
    def get_user(self, user_id):
        try:
            user_data = self.users_service.get_user(user_id)
            return self._transform_to_user_dto(user_data)
        except Exception as e:
            raise RepositoryException(f"Error obtenint usuari {user_id}: {str(e)}")
```

## 7. DTOs (Data Transfer Objects)

### Descripció Funcional
Els DTOs són objectes que faciliten el transport de dades entre capes del sistema:
- Proporcionen una estructura immutable i ben definida
- Oculten detalls d'implementació interna
- Faciliten la serialització i deserialització

### Tecnologies Utilitzades
S'han implementat utilitzant:
- Dataclasses de Python (Python 3.7+) per automatitzar mètodes comuns
- Type hints per a documentació i seguretat de tipus
- Immutabilitat (`frozen=True`) per garantir la integritat de dades

### Problemes i Solucions
**Problema**: Necessitat de serialització personalitzada per a entitats complexes.
**Solució**: Implementació de mètodes de conversió (`to_dict()`, `from_dict()`) en els DTOs.

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
@dataclass
class AlbumDTO:
    """
    Data Transfer Object para representar un álbum.
    """
    id: str
    name: str
    artist: str
    release_date: Optional[datetime] = None
    spotify_id: Optional[str] = None
    cover_image: Optional[str] = None
    tracks_count: Optional[int] = None
    popularity: Optional[int] = None
    genres: Optional[List[str]] = None
    average_rating: Optional[float] = None
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AlbumDTO':
        """
        Crea un DTO a partir de un diccionario.
        """
        pass
```

## 8. Utils i Excepcions

### Descripció Funcional
Aquest component proporciona funcionalitat transversal utilitzada per diversos components:
- Utilitats de resposta i formatació
- Sistema de gestió d'excepcions personalitzades
- Funcions de logging i monitoratge

### Tecnologies Utilitzades
S'han implementat utilitzant:
- Classes d'excepció personalitzades
- Funcions d'utilitat estàtiques
- Decoradors per aspectes transversals

### Problemes i Solucions
**Problema**: Manca d'estandardització en les respostes d'error de l'API.
**Solució**: Creació d'una funció centralitzada `create_response()` i gestor d'excepcions personalitzat.

```python
def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado para devolver respuestas de error
    en un formato consistente y amigable para aplicaciones Flutter.
    
    Args:
        exc: Excepción capturada
        context: Contexto de la excepción
        
    Returns:
        Response: Respuesta HTTP con formato estandarizado
    """
    # Primero, intentamos manejar la excepción con el manejador estándar de DRF
    response = exception_handler(exc, context)
    
    # Si ya tenemos una respuesta, la formateamos para Flutter
    if response is not None:
        error_data = {
            "success": False,
            "error": {                "message": str(exc),
                "details": response.data if hasattr(response, 'data') else None,
                "status_code": response.status_code
            }
        }
        return Response(error_data, status=response.status_code)
```

## 9. Configuració i Inicialització

### Descripció Funcional
La configuració defineix com s'inicia i configura el sistema:
- Configuració de Django (`settings.py`)
- Definició de rutes API (`urls.py`)
- Inicialització de components i middleware

### Tecnologies Utilitzades
S'ha implementat utilitzant el sistema de configuració de Django amb:
- Variables d'entorn per a configuracions sensibles
- Fitxers de configuració separats per entorn (desenvolupament, testing, producció)

### Problemes i Solucions
**Problema**: Dificultat per mantenir configuracions consistents entre entorns.
**Solució**: Implementació d'un sistema basat en variables d'entorn i valors per defecte.

## Resum de l'Arquitectura

L'arquitectura Myqx-BFF segueix un patró en capes amb separació clara de responsabilitats:

1. **Middleware** - Processament inicial de peticions
2. **Vistes API** - Exposició d'endpoints i serialització
3. **Controladors** - Lògica de negoci i orquestració
4. **Interfícies** - Contractes d'abstracció
5. **Serveis** - Comunicació amb sistemes externs
6. **Repositoris** - Abstracció d'accés a dades
7. **DTOs** - Transferència de dades entre capes
8. **Models** - Representació de les entitats de domini
9. **Utils** - Funcionalitat compartida

L'arquitectura facilita el manteniment, testing i escalabilitat del sistema, permetent que diferents equips treballin en paral·lel en diferents capes sense interferències. Les decisions tecnològiques s'han pres prioritzant la robustesa, mantenibilitat i simplicitat del codi.

La diagramació de l'arquitectura en components separats ha permès una millor visualització i comprensió del sistema, facilitant la seva evolució i documentació.
