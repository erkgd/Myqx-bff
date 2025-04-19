from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthCheckView, UserView, UsersView, AuthView, AuthTestView, SpotifyAuthView, FollowingNetworkView

router = DefaultRouter()
# Aquí se pueden registrar los ViewSets cuando sean necesarios
# router.register('recursos', RecursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check-slash'),
    path('health', HealthCheckView.as_view(), name='health-check'),
    path('users/', UsersView.as_view(), name='users-list'),
    path('users/<str:user_id>/', UserView.as_view(), name='user-detail'),
    path('auth/token/', AuthView.as_view(), name='auth'),
    path('auth/test/', AuthTestView.as_view(), name='auth-test'),
    path('auth/spotify', SpotifyAuthView.as_view(), name='spotify-auth'),
    path('users/<str:user_id>/following_network/', FollowingNetworkView.as_view(), name='following-network'),
    
    # Ruta directa para acceder sin 'users/' en la URL
    path('<str:user_id>/following_network/', FollowingNetworkView.as_view(), name='direct-following-network')
]