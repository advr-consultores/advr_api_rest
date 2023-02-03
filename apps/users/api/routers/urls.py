from rest_framework.routers import DefaultRouter

from apps.users.api.views.user import UserViewSet

# views

router = DefaultRouter()

router.register(r'usuario', UserViewSet, basename='user_api')

urlpatterns = router.urls
