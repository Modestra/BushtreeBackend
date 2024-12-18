from django.contrib import admin
from django.urls import path, include
from bushtree.views import *
from django.conf import settings
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r"flower", FlowerApiViewSet)
router.register(r"gardens", GardensApiViewSet)
router.register(r"flowerband", FlowerBandApiViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Bushtree API",
      default_version='v1',
      description="API для ссылок проекта",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
