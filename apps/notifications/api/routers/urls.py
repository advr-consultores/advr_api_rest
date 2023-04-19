from rest_framework.routers import DefaultRouter

# views
from apps.notifications.api.views.notify import NotificationsView

router = DefaultRouter()

router.register(r'notificacion', NotificationsView, basename='notificaciones')

urlpatterns = router.urls
