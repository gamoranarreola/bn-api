from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Modules
    path('', include('bn_app.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
