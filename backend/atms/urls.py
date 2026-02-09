from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from traffic_app import views

router = DefaultRouter()
router.register(r'violations', views.ViolationViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'fines', views.FineViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]
