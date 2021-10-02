from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # OAuth
    path('api/oauth/', include('rest_framework_social_oauth2.urls')),

    # JWT token
    path('api/auth/', include('djoser.urls')),
    path('api/auth-token/', include('djoser.urls.jwt')),

    # Modules
    path('', include('bn_app.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
