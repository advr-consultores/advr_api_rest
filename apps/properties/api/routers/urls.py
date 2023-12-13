from rest_framework.routers import DefaultRouter

# views
from apps.properties.api.views.property import PropertyViewSet
from apps.properties.api.views.user_charge import PropertyUserChargeViewSet


router = DefaultRouter()

router.register(r'inmueble', PropertyViewSet, basename='inmuebles')
router.register(r'cargo', PropertyUserChargeViewSet, basename='property-user-charge')


urlpatterns = router.urls
