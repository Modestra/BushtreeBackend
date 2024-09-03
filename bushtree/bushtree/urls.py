"""
URL configuration for bushtree project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from bushtree.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"seccions", SeccionApiViewSet)

get_user = SeccionApiViewSet.as_view({"get", "list"})
set_user = SeccionApiViewSet.as_view({"post": "crate_seccion"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seccions/get', get_user),
    path('seccions/create', set_user),
    path('api/v1/', include(router.urls))
]
