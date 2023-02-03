from rest_framework.routers import DefaultRouter
from apps.groups.api.views.groups import GroupsViewSet
from apps.groups.api.views.permissions import PermissionViewSet

router = DefaultRouter()

router.register(r'grupo', GroupsViewSet, basename='grupos')
router.register(r'permisos', PermissionViewSet, basename='permisos')

urlpatterns = router.urls
