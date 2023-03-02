from rest_framework.routers import DefaultRouter

# views
from apps.projects.api.views.project import ProjectViewSet
from apps.projects.api.views.concept import ConceptViewSet


router = DefaultRouter()

router.register(r'proyecto', ProjectViewSet, basename='pryecto')
router.register(r'conceptos', ConceptViewSet, basename='conceptos')

urlpatterns = router.urls
