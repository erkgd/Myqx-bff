from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import directly from the views modules to avoid circular imports
from .views.basic_views import HealthCheckView
from .views.user_views import UserView, UsersView, FollowingNetworkView, UserProfileView, UserFollowingView
from .views.auth_views import AuthView, AuthTestView, SpotifyAuthView
from .views.albums_views import AlbumView, AlbumsRatingView, AlbumRatingsView, AlbumUserRatingView
from .views.ratings_views import RatingsView
from .views.feed_views import FeedView
from .views.profile_view import ProfileView
from .views.user_following_status_view import UserFollowingStatusView
# Import UserCompleteProfileView 
from .views.user_complete_profile_view import UserCompleteProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.views.generic import RedirectView
from .auth_views import CustomTokenVerifyView

router = DefaultRouter()
# Aquí se pueden registrar los ViewSets cuando sean necesarios
# router.register('recursos', RecursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check-slash'),
    path('health', HealthCheckView.as_view(), name='health-check'),
    path('users/', UsersView.as_view(), name='users-list'),
    path('users/<str:user_id>/', UserView.as_view(), name='user-detail'),    path('users/<str:user_id>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<str:user_id>/profile', UserProfileView.as_view(), name='user-profile-no-slash'),
    path('users/<str:user_id>/complete-profile/', UserCompleteProfileView.as_view(), name='user-complete-profile'),
    path('users/<str:user_id>/complete-profile', UserCompleteProfileView.as_view(), name='user-complete-profile-no-slash'),    path('users/following/<str:follower_id>/<str:followed_id>/', UserFollowingView.as_view(), name='user-following'),
    path('users/following/<str:follower_id>/<str:followed_id>', UserFollowingView.as_view(), name='user-following-no-slash'),
    path('users/following/status/<str:follower_id>/<str:followed_id>/', UserFollowingStatusView.as_view(), name='user-following-status'),
    path('users/following/status/<str:follower_id>/<str:followed_id>', UserFollowingStatusView.as_view(), name='user-following-status-no-slash'),
    path('auth/test/', AuthTestView.as_view(), name='auth-test'),
    path('auth/spotify', SpotifyAuthView.as_view(), name='spotify-auth'),
    path('users/<str:user_id>/following_network/', FollowingNetworkView.as_view(), name='following-network'),
    path('users/<str:user_id>/following_network', FollowingNetworkView.as_view(), name='following-network-no-slash'),
    
    # Rutas para el nuevo endpoint de perfil
    path('profile/<str:user_id>/', ProfileView.as_view(), name='profile-detail'),
    path('profile/<str:user_id>', ProfileView.as_view(), name='profile-detail-no-slash'),
    path('profile/', ProfileView.as_view(), name='own-profile'),
    
    # Ruta directa para acceder sin 'users/' en la URL
    path('<str:user_id>/following_network/', FollowingNetworkView.as_view(), name='direct-following-network'),
    
    # Rutas de autenticación JWT estándar
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Rutas personalizadas para verificación de tokens sin CSRF
    path('auth/verify/', CustomTokenVerifyView.as_view(), name='custom_token_verify'),
    path('auth/verify', CustomTokenVerifyView.as_view(), name='custom_token_verify_no_slash'),    # Rutas para álbumes
    path('albums/', AlbumView.as_view(), name='albums-list'),
    path('albums/<str:album_id>/', AlbumView.as_view(), name='album-detail'),
    path('albums/<str:album_id>/ratings/', AlbumRatingsView.as_view(), name='album-ratings'),
    path('albums/<str:album_id>/ratings', AlbumRatingsView.as_view(), name='album-ratings-no-slash'),
    path('albums/<str:album_id>/rating/', AlbumUserRatingView.as_view(), name='album-user-rating'),
    path('albums/<str:album_id>/rating', AlbumUserRatingView.as_view(), name='album-user-rating-no-slash'),
    path('users/<str:user_id>/albums/ratings/', AlbumsRatingView.as_view(), name='user-album-ratings'),
    path('users/<str:user_id>/albums/ratings', AlbumsRatingView.as_view(), name='user-album-ratings-no-slash'),
    path('users/<str:user_id>/album/<str:album_id>/rating/', AlbumUserRatingView.as_view(), name='user-album-rating'),
    path('users/<str:user_id>/album/<str:album_id>/rating', AlbumUserRatingView.as_view(), name='user-album-rating-no-slash'),
    
    # Endpoint centralizado para calificaciones
    path('ratings/submit/', RatingsView.as_view(), name='submit-rating'),
    path('ratings/submit', RatingsView.as_view(), name='submit-rating-no-slash'),
    
    # Redirecciona de albums/rate a ratings/submit
    path('albums/rate/', RedirectView.as_view(url='/api/ratings/submit/', permanent=False), name='rate-album-redirect'),
    path('albums/rate', RedirectView.as_view(url='/api/ratings/submit/', permanent=False), name='rate-album-no-slash-redirect'),
      # Rutas para consultar calificaciones
    path('ratings/', RatingsView.as_view(), name='ratings-list'),
    path('ratings/<str:rating_id>/', RatingsView.as_view(), name='rating-detail'),
    
    # Rutas para el feed
    path('feed/', FeedView.as_view(), name='feed-list'),
    path('feed', FeedView.as_view(), name='feed-list-no-slash'),
    path('feed/<str:item_id>/', FeedView.as_view(), name='feed-item'),
    path('ratings/submit', RedirectView.as_view(url='/api/ratings/submit', query_string=True)),
    path('ratings/submit/', RedirectView.as_view(url='/api/ratings/submit/', query_string=True)),
]