"""
URL configuration for myqx_bff project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.decorators.http import require_GET
from api.views import FeedView  # Importamos la vista directamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Incluir las URLs de la aplicación API
    
    # URLs directas sin redirección
    path('feed', FeedView.as_view(), name='feed-direct'),
    path('feed/', FeedView.as_view(), name='feed-direct-slash'),
    path('ratings/submit', RedirectView.as_view(url='/api/ratings/submit', query_string=True)),
    path('ratings/submit/', RedirectView.as_view(url='/api/ratings/submit/', query_string=True)),
]
