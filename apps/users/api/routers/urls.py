from rest_framework.routers import DefaultRouter

from apps.users.api.views.user import UserViewSet
from apps.users.api.views.user_charge import UserChargeViewSet

# views

router = DefaultRouter()

router.register(r'usuario', UserViewSet, basename='user_api')
router.register(r'cargo', UserChargeViewSet, basename='usuario a cargo')

urlpatterns = router.urls
