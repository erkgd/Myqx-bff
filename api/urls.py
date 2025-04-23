from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthCheckView, UserView, UsersView, AuthView, AuthTestView, SpotifyAuthView, FollowingNetworkView, UserProfileView, UserFollowingView
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
    path('users/<str:user_id>/', UserView.as_view(), name='user-detail'),
    path('users/<str:user_id>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<str:user_id>/profile', UserProfileView.as_view(), name='user-profile-no-slash'),
    path('users/following/<str:follower_id>/<str:followed_id>/', UserFollowingView.as_view(), name='user-following'),
    path('users/following/<str:follower_id>/<str:followed_id>', UserFollowingView.as_view(), name='user-following-no-slash'),
    path('auth/test/', AuthTestView.as_view(), name='auth-test'),
    path('auth/spotify', SpotifyAuthView.as_view(), name='spotify-auth'),
    path('users/<str:user_id>/following_network/', FollowingNetworkView.as_view(), name='following-network'),
    path('users/<str:user_id>/following_network', FollowingNetworkView.as_view(), name='following-network-no-slash'),
    
    # Ruta directa para acceder sin 'users/' en la URL
    path('<str:user_id>/following_network/', FollowingNetworkView.as_view(), name='direct-following-network'),
    
    # Rutas de autenticación JWT estándar
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Rutas personalizadas para verificación de tokens sin CSRF
    path('auth/verify/', CustomTokenVerifyView.as_view(), name='custom_token_verify'),
    path('auth/verify', CustomTokenVerifyView.as_view(), name='custom_token_verify_no_slash'),
]