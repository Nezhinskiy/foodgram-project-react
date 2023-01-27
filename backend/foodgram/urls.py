from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from foodgram import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('recipes.urls', namespace='recipes'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
