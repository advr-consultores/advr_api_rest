"""advr_api_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from apps.authentication.views import Login

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('usuarios/', include('apps.users.api.routers.urls')),
    path('grupos/', include('apps.groups.api.routers.urls')),
    path('clientes/', include('apps.clients.api.routers.urls')),
    path('territorios/', include('apps.territories.api.routers.urls')),
    path('inmuebles/', include('apps.properties.api.routers.urls')),
    path('proyectos/', include('apps.projects.api.routers.urls')),
    path('trabajos/', include('apps.works.api.routers.urls')),
    path('peticiones/', include('apps.resources.api.routers.urls')),
    path('notificaciones/', include('apps.notifications.api.routers.urls')),
    path('correos/', include('apps.email.api.routers.urls')),
    path('beneficiarios/', include('apps.beneficiary.api.routers.urls')),
    path('admin/', admin.site.urls),
]
