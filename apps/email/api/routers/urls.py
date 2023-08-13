from rest_framework.routers import DefaultRouter

from apps.email.api.views.sendEmail import SendEmail

router = DefaultRouter()

router.register(r'enviar', SendEmail, basename='Emai')

urlpatterns = router.urls