from rest_framework.routers import DefaultRouter
from apps.territories.api.views.locality import LocalityViewSet
from apps.territories.api.views.municipality import MunicipalityViewSet
from apps.territories.api.views.province import ProvinceViewSet

router = DefaultRouter()

router.register(r'estados', ProvinceViewSet, basename='estados')
router.register(r'municipios', MunicipalityViewSet, basename='municipios')
router.register(r'localidades', LocalityViewSet, basename='localidades')

urlpatterns = router.urls
