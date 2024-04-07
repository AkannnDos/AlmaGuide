from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title='Alma Guide API',
        default_version='v1',
        description='',
        contact=openapi.Contact(email=''),
        license=openapi.License(name=''),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/attractions/', include('attractions.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/stories/', include('stories.urls')),
    path('api/tours/', include('tours.urls')),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
