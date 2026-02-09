from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ViolationViewSet,
    FineViewSet,
    UserProfileViewSet,
    VehicleViewSet,
    TrafficPatternViewSet,
    IoTSensorViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'violations', ViolationViewSet, basename='violation')
router.register(r'fines', FineViewSet, basename='fine')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'patterns', TrafficPatternViewSet, basename='pattern')
router.register(r'sensors', IoTSensorViewSet, basename='sensor')

urlpatterns = [
    path('', include(router.urls)),
]
