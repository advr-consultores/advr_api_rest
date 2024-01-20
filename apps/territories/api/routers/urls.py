from rest_framework.routers import DefaultRouter
from apps.territories.api.views.locality import LocalityViewSet
from apps.territories.api.views.municipality import MunicipalityViewSet
from apps.territories.api.views.province import ProvinceViewSet
from apps.territories.api.views.property import PropertyTerritoriesViewSet
from apps.territories.api.views.user_charge import UserChargeTerritoriesViewSet

router = DefaultRouter()

router.register(r'estados', ProvinceViewSet, basename='estados')
router.register(r'municipios', MunicipalityViewSet, basename='municipios')
router.register(r'localidades', LocalityViewSet, basename='localidades')
router.register(r'inmuebles', PropertyTerritoriesViewSet, basename='territorios-inmuebles')
router.register(r'cargo', UserChargeTerritoriesViewSet, basename='usuario-cargo')

urlpatterns = router.urls
