    def get_complete_profile(self, user_id: str, current_user_id: str = None, 
                            include_following_status: bool = False, 
                            include_top_rated_album: bool = False,
                            include_recent_activity: bool = False,
                            activity_limit: int = 5):
        """
        Obtiene el perfil completo de un usuario con información adicional opcional.
        
        Args:
            user_id: ID del usuario principal
            current_user_id: ID del usuario que está visualizando el perfil (para determinar si lo sigue)
            include_following_status: Si se debe incluir información de seguimiento
            include_top_rated_album: Si se debe incluir el álbum mejor valorado
            include_recent_activity: Si se debe incluir actividad reciente
            activity_limit: Cantidad de elementos de actividad reciente a incluir
            
        Returns:
            Response: Respuesta HTTP con los datos del perfil completo o error
        """
        import sys
        
        try:
            print(f"[USERS_CONTROLLER] Obteniendo perfil completo para usuario {user_id}", file=sys.stderr)
            
            # 1. Obtener información básica del perfil
            basic_profile = self.repository.find_by_id(user_id)
            
            if not basic_profile:
                print(f"[USERS_CONTROLLER] Usuario con ID {user_id} no encontrado", file=sys.stderr)
                raise ResourceNotFoundException("Usuario", user_id)
            
            # Convertir el DTO a diccionario para poder añadir más información
            complete_profile = basic_profile.to_dict() if hasattr(basic_profile, 'to_dict') else basic_profile
            
            # 2. Añadir información de seguimiento si se solicita
            if include_following_status and current_user_id:
                print(f"[USERS_CONTROLLER] Verificando estado de seguimiento entre {current_user_id} y {user_id}", file=sys.stderr)
                is_following = self.repository.check_following_status(current_user_id, user_id)
                complete_profile['following_status'] = {
                    'is_following': is_following
                }
            
            # 3. Añadir álbum mejor valorado si se solicita
            if include_top_rated_album:
                print(f"[USERS_CONTROLLER] Obteniendo álbum mejor valorado para usuario {user_id}", file=sys.stderr)
                from ..repositories.album_repository import AlbumRepository
                album_repo = AlbumRepository()
                top_album = album_repo.get_user_top_rated_album(user_id)
                if top_album:
                    complete_profile['top_rated_album'] = top_album
            
            # 4. Añadir actividad reciente si se solicita
            if include_recent_activity:
                print(f"[USERS_CONTROLLER] Obteniendo actividad reciente para usuario {user_id} (límite: {activity_limit})", file=sys.stderr)
                from ..repositories.feed_repository import FeedRepository
                feed_repo = FeedRepository()
                recent_activity = feed_repo.get_user_activity(user_id, limit=activity_limit)
                if recent_activity:
                    complete_profile['recent_activity'] = [
                        item.to_dict() if hasattr(item, 'to_dict') else item 
                        for item in recent_activity
                    ]
            
            print(f"[USERS_CONTROLLER] Perfil completo generado con éxito para usuario {user_id}", file=sys.stderr)
            
            # Devolver el perfil completo
            return create_response(
                data=complete_profile,
                message="Perfil completo obtenido con éxito",
                status_code=status.HTTP_200_OK
            )
            
        except ResourceNotFoundException as e:
            # El manejador de excepciones personalizado se encargará de formatear esta respuesta
            raise
        except Exception as e:
            # Loguear el error y devolver una respuesta genérica
            import logging
            logging.exception(f"Error al obtener perfil completo de usuario {user_id}: {str(e)}")
            print(f"[USERS_CONTROLLER] Error obteniendo perfil completo: {str(e)}", file=sys.stderr)
            return create_response(
                data=None,
                message="Error al obtener perfil completo de usuario",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )
