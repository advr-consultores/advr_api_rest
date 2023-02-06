from rest_framework.routers import DefaultRouter
from apps.clients.api.views.clients import ClientViewSet

router = DefaultRouter()

router.register(r'cliente', ClientViewSet, basename='clientes')

urlpatterns = router.urls
