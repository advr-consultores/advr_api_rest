from rest_framework.routers import DefaultRouter

# views
from apps.resources.api.views.resource import ResourceViewSet
from apps.resources.api.views.fileReceipt import ProofPaymentViewSet
from apps.resources.api.views.comment import CommentViewSet
from apps.resources.api.views.petition import PetitionViewSet

router = DefaultRouter()

router.register(r'peticion', PetitionViewSet, basename='Petición')
router.register(r'recursos', ResourceViewSet, basename='Solicitud de recursos.')
router.register(r'comprobante', ProofPaymentViewSet, basename='Comprobante de pago.')
router.register(r'comentario', CommentViewSet, basename='Comentarios')

urlpatterns = router.urls