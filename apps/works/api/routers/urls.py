
from rest_framework.routers import DefaultRouter

# views
from apps.works.api.views.works_status import WorkStatusViewSet
from apps.works.api.views.works import WorkViewSet
from apps.works.api.views.comment import CommentViewSet
from apps.works.api.views.files import FileViewSet
from apps.works.api.views.works_filter import WorksPropertyViewSet
from apps.works.api.views.usuario import WorksUsuarioViewSet
from apps.works.api.views.properties import PropertiesViewSet

router = DefaultRouter()

router.register(r'status', WorkStatusViewSet, basename='status_trabajos')
router.register(r'trabajo', WorkViewSet, basename='trabajos')
router.register(r'archivo', FileViewSet, basename='archivos')
router.register(r'pendiente', WorksPropertyViewSet, basename='pendientes')
router.register(r'usuario', WorksUsuarioViewSet, basename='trabajos_usuario')
router.register(r'comentario', CommentViewSet, basename='comentarios')
router.register(r'cliente', PropertiesViewSet, basename='cliente')

urlpatterns = router.urls
