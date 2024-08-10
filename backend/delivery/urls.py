from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, LocationViewSet, DeliveryViewSet,UserInfoView , update_vehicle_location , LoginView,RegisterView ,convert_to_coordinates_view, convert_to_3words_view , assign_delivery_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Smart Delivery API",
      default_version='v1',
      description="API documentation for the Smart Delivery and Logistics Services",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'deliveries', DeliveryViewSet , basename='delivery')

urlpatterns = [
    path('', include(router.urls)),
    path('update-location/', update_vehicle_location, name='update-vehicle-location'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('convert-to-coordinates/', convert_to_coordinates_view, name='convert-to-coordinates'),
    path('convert-to-3words/', convert_to_3words_view, name='convert-to-3words'),
    path('assign-delivery/', assign_delivery_view, name='assign-delivery'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),



]+ router.urls
