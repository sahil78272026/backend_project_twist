from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth_app.urls')),
]


# Serve media files during development
print(MEDIA_URL)
print(MEDIA_ROOT)
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)