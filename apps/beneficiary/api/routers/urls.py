from rest_framework.routers import DefaultRouter

# views
from apps.beneficiary.api.views.beneficiary import BeneficiaryViewSet


router = DefaultRouter()

router.register(r'beneficiario', BeneficiaryViewSet, basename='beneficiario')

urlpatterns = router.urls
