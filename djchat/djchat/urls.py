from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from server import views

router = DefaultRouter()
router.register(r'api/server/select', views.ServerListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]+router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)