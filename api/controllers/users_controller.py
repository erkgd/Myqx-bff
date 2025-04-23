from typing import Dict, List, Any, Optional
from rest_framework import status
from rest_framework.request import Request
from ..repositories.user_repository import UserRepository
from ..dtos.user_dto import UserDTO
from ..exceptions.api_exceptions import ResourceNotFoundException, ValidationException, AuthenticationException
from ..utils import create_response


class UsersController:
    """
    Controlador para manejar operaciones relacionadas con usuarios.
    Utiliza el patrón repositorio para acceso a datos.
    Optimizado para responder a aplicaciones Flutter.
    """
    
    def __init__(self):
        """
        Constructor del controlador de usuarios.
        """
        self.repository = UserRepository()
    
    def get_user(self, user_id: str):
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario a obtener
            
        Returns:
            Response: Respuesta HTTP con los datos del usuario o error
        """
        try:
            user = self.repository.find_by_id(user_id)
            if not user:
                raise ResourceNotFoundException("Usuario", user_id)
                
            return create_response(
                data=user.to_dict(),
                message="Usuario encontrado con éxito",
                status_code=status.HTTP_200_OK
            )
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
    
    def get_users(self, request: Request):
        """
        Obtiene una lista de usuarios con filtros opcionales.
        
        Args:
            request: Objeto request que puede contener filtros
            
        Returns:
            Response: Respuesta HTTP con la lista de usuarios
        """
        try:
            # Extraemos parámetros del request
            params = request.query_params.dict()
            
            # Configuramos paginación
            page = int(params.pop('page', 1))
            page_size = int(params.pop('page_size', 20))
            
            # Obtenemos usuarios
            users = self.repository.find_all(**params)
            
            # Convertimos los DTOs a diccionarios para la respuesta
            users_dict = [user.to_dict() for user in users]
            
            # Información de paginación para el cliente Flutter
            meta = {
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": len(users_dict),
                    "total_pages": (len(users_dict) + page_size - 1) // page_size
                }
            }
            
            return create_response(
                data=users_dict,
                message="Usuarios obtenidos con éxito",
                status_code=status.HTTP_200_OK,
                meta=meta
            )
        except Exception as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
    
    def create_user(self, data: Dict[str, Any]):
        """
        Crea un nuevo usuario.
        
        Args:
            data: Datos del usuario a crear
            
        Returns:
            Response: Respuesta HTTP con los datos del usuario creado
        """
        try:
            # Validar datos requeridos
            required_fields = ['username', 'email']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                raise ValidationException(
                    f"Campos requeridos: {', '.join(missing_fields)}",
                    errors={field: "Este campo es requerido" for field in missing_fields}
                )
            
            # Crear DTO y validar
            user_dto = UserDTO.from_dict(data)
            
            # Guardar usuario
            created_user = self.repository.create(user_dto)
            
            return create_response(
                data=created_user.to_dict(),
                message="Usuario creado con éxito",
                status_code=status.HTTP_201_CREATED
            )
        except ValidationException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except ValueError as e:
            # Convertimos ValueError en una ValidationException para mantener consistencia
            raise ValidationException(str(e))
        except Exception as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
    
    def update_user(self, user_id: str, data: Dict[str, Any]):
        """
        Actualiza un usuario existente.
        
        Args:
            user_id: ID del usuario a actualizar
            data: Nuevos datos del usuario
            
        Returns:
            Response: Respuesta HTTP con los datos del usuario actualizado
        """
        try:
            # Verificar que el usuario existe
            existing_user = self.repository.find_by_id(user_id)
            if not existing_user:
                raise ResourceNotFoundException("Usuario", user_id)
            
            # Actualizar solo los campos proporcionados
            for key, value in data.items():
                if hasattr(existing_user, key) and key != 'id':
                    setattr(existing_user, key, value)
            
            # Guardar usuario actualizado
            updated_user = self.repository.update(user_id, existing_user)
            
            return create_response(
                data=updated_user.to_dict(),
                message="Usuario actualizado con éxito",
                status_code=status.HTTP_200_OK
            )
        except (ResourceNotFoundException, ValidationException) as e:
            # El manejador de excepciones personalizado se encargará de formatear estas respuestas
            raise
        except ValueError as e:
            # Convertimos ValueError en una ValidationException para mantener consistencia
            raise ValidationException(str(e))
        except Exception as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
    
    def delete_user(self, user_id: str):
        """
        Elimina un usuario.
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        try:
            # Verificar que el usuario existe
            existing_user = self.repository.find_by_id(user_id)
            if not existing_user:
                raise ResourceNotFoundException("Usuario", user_id)
            
            success = self.repository.delete(user_id)
            if success:
                return create_response(
                    message="Usuario eliminado con éxito",
                    status_code=status.HTTP_200_OK
                )
            else:
                raise Exception("Error al eliminar usuario")
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
    
    def authenticate(self, credentials: Dict[str, str]):
        """
        Autentica un usuario.
        
        Args:
            credentials: Credenciales del usuario
            
        Returns:
            Response: Respuesta HTTP con token y datos del usuario o error
        """
        try:
            username = credentials.get('username')
            password = credentials.get('password')
            
            # Validar datos requeridos
            if not username or not password:
                raise ValidationException(
                    "Nombre de usuario y contraseña son requeridos",
                    errors={
                        "username": "Este campo es requerido" if not username else None,
                        "password": "Este campo es requerido" if not password else None
                    }
                )
            
            result = self.repository.authenticate(username, password)
            if result:
                # Para Flutter, aseguramos que la respuesta tiene un formato consistente
                # Formateamos los datos de autenticación para la aplicación móvil
                auth_data = {
                    "token": result.get('token', ''),
                    "user": result.get('user', {})
                }
                
                return create_response(
                    data=auth_data,
                    message="Autenticación exitosa",
                    status_code=status.HTTP_200_OK
                )
            else:
                raise AuthenticationException("Credenciales inválidas")
        except (ValidationException, AuthenticationException) as e:
            # El manejador de excepciones personalizado se encargará de formatear estas respuestas
            raise
        except Exception as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
    
    def get_following_network(self, user_id: str):
        """
        Obtiene la red de seguidos de un usuario específico.
        
        Args:
            user_id: ID del usuario cuya red se quiere obtener
            
        Returns:
            Lista de usuarios seguidos o lista vacía si no hay ninguno
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            from ..services.implementations.users_service_impl import UsersServiceImpl
            
            # Log del user_id recibido
            logger.info(f"Recibido user_id: {user_id}")
            
            # Crear una instancia del servicio
            users_service = UsersServiceImpl()
            
            # Obtener la red de seguidos usando el método que implementamos
            following_network = users_service.get_following_network(user_id)
            
            # Log de la respuesta obtenida del servicio
            logger.info(f"Respuesta obtenida del servicio para user_id {user_id}: {following_network}")
            
            return following_network
            
        except Exception as e:
            # Loggear el error
            logger.error(f"Error al obtener red de seguidos para usuario {user_id}: {str(e)}")
            
            # En caso de error devolvemos una lista vacía
            return []
    
    def get_user_profile(self, user_id: str):
        """
        Obtiene el perfil detallado de un usuario, incluyendo información adicional
        como estadísticas, preferencias y datos extendidos.
        
        Args:
            user_id: ID del usuario cuyo perfil se quiere obtener
            
        Returns:
            Response: Respuesta HTTP con los datos del perfil del usuario o error
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Obtener los datos básicos del usuario
            user = self.repository.find_by_id(user_id)
            if not user:
                raise ResourceNotFoundException("Usuario", user_id)
            
            # Obtenemos información adicional del perfil del usuario
            from ..services.implementations.users_service_impl import UsersServiceImpl
            users_service = UsersServiceImpl()
            
            try:
                # Intentamos obtener información adicional del perfil
                following_network = self.get_following_network(user_id)
                
                # Creamos un objeto de perfil más completo
                profile_data = {
                    **user.to_dict(),  # Datos básicos del usuario
                    "following_count": len(following_network) if following_network else 0,
                    "following": following_network[:5] if following_network and len(following_network) > 0 else [],  # Primeros 5 seguidos
                    "is_complete": user.email is not None and user.username is not None,
                    "last_login": user.last_login if hasattr(user, 'last_login') else None,
                }
                
                return create_response(
                    data=profile_data,
                    message="Perfil de usuario obtenido con éxito",
                    status_code=status.HTTP_200_OK
                )
            
            except Exception as e:
                logger.error(f"Error al obtener datos adicionales del perfil: {str(e)}")
                # Si hay error en los datos adicionales, devolvemos al menos los datos básicos
                return create_response(
                    data=user.to_dict(),
                    message="Datos básicos de perfil obtenidos con éxito",
                    status_code=status.HTTP_200_OK
                )
                
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error no esperado al obtener perfil de usuario {user_id}")
            # Propagar excepción para que sea manejada por el manejador global
            raise
    
    def follow_user(self, follower_id: str, followed_id: str):
        """
        Establece una relación de seguimiento donde un usuario sigue a otro.
        
        Args:
            follower_id: ID del usuario que hace el seguimiento
            followed_id: ID del usuario que es seguido
            
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Verificar que ambos usuarios existan
            follower = self.repository.find_by_id(follower_id)
            if not follower:
                raise ResourceNotFoundException("Usuario seguidor", follower_id)
                
            followed = self.repository.find_by_id(followed_id)
            if not followed:
                raise ResourceNotFoundException("Usuario seguido", followed_id)
            
            # Usamos el servicio de usuarios para establecer la relación de seguimiento
            from ..services.implementations.users_service_impl import UsersServiceImpl
            users_service = UsersServiceImpl()
            
            # Llamar al servicio para crear la relación de seguimiento
            result = users_service.follow_user(follower_id, followed_id)
            
            # Crear respuesta basada en el resultado
            return create_response(
                data={
                    "follower": follower.to_dict(),
                    "followed": followed.to_dict(),
                    "status": "following"
                },
                message="Relación de seguimiento establecida con éxito",
                status_code=status.HTTP_201_CREATED
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al establecer relación de seguimiento: {str(e)}")
            # Propagar excepción para que sea manejada por el manejador global
            raise
    
    def unfollow_user(self, follower_id: str, followed_id: str):
        """
        Elimina una relación de seguimiento existente entre usuarios.
        
        Args:
            follower_id: ID del usuario que hace el seguimiento
            followed_id: ID del usuario que es seguido
            
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Verificar que ambos usuarios existan
            follower = self.repository.find_by_id(follower_id)
            if not follower:
                raise ResourceNotFoundException("Usuario seguidor", follower_id)
                
            followed = self.repository.find_by_id(followed_id)
            if not followed:
                raise ResourceNotFoundException("Usuario seguido", followed_id)
            
            # Usamos el servicio de usuarios para eliminar la relación de seguimiento
            from ..services.implementations.users_service_impl import UsersServiceImpl
            users_service = UsersServiceImpl()
            
            # Llamar al servicio para eliminar la relación de seguimiento
            result = users_service.unfollow_user(follower_id, followed_id)
            
            # Crear respuesta basada en el resultado
            return create_response(
                data={
                    "follower": follower.to_dict(),
                    "followed": followed.to_dict(),
                    "status": "unfollowed"
                },
                message="Relación de seguimiento eliminada con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al eliminar relación de seguimiento: {str(e)}")
            # Propagar excepción para que sea manejada por el manejador global
            raise
    
    def check_follow_status(self, follower_id: str, followed_id: str):
        """
        Verifica si un usuario sigue a otro.
        
        Args:
            follower_id: ID del usuario que podría estar siguiendo
            followed_id: ID del usuario que podría estar siendo seguido
            
        Returns:
            Response: Respuesta HTTP con el estado de la relación
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Verificar que ambos usuarios existan
            follower = self.repository.find_by_id(follower_id)
            if not follower:
                raise ResourceNotFoundException("Usuario seguidor", follower_id)
                
            followed = self.repository.find_by_id(followed_id)
            if not followed:
                raise ResourceNotFoundException("Usuario seguido", followed_id)
            
            # Usamos el servicio de usuarios para verificar la relación
            from ..services.implementations.users_service_impl import UsersServiceImpl
            users_service = UsersServiceImpl()
            
            # Verificar si existe la relación de seguimiento
            is_following = users_service.is_following(follower_id, followed_id)
            
            # Crear respuesta basada en el resultado
            return create_response(
                data={
                    "follower_id": follower_id,
                    "followed_id": followed_id,
                    "is_following": is_following
                },
                message="Estado de seguimiento verificado con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            logger.exception(f"Error al verificar estado de seguimiento: {str(e)}")
            # Propagar excepción para que sea manejada por el manejador global
            raise