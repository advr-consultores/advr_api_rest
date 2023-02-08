from rest_framework.routers import DefaultRouter

# views
from apps.properties.api.views.property import PropertyViewSet
from apps.properties.api.views.property_province import PropertyProvinceViewSet


router = DefaultRouter()

router.register(r'inmueble', PropertyProvinceViewSet, basename='inmuebles-filtro')
router.register(r'inmueble', PropertyViewSet, basename='inmuebles')


urlpatterns = router.urls
