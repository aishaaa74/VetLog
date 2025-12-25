from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),           # главная страница
    path('pets/', include('pets.urls')),      # питомцы
    path('health/', include('health.urls')),  # ← ВСЁ ЗДОРОВЬЕ ЗДЕСЬ
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)