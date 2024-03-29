from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status


class TokenAuthentication(object):

    # expired = False

    # def token_expire_handler(self, token):
    #     return self.is_token_expired(token)
    #     if is_expire:
    #         print('TOKEN EXPIRADO')
    #         self.expired = True
    #         user = token.user
    #         token.delete()
    #         token = self.get_model().objects.create(user=user)
    #     return is_expire, token

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    def authenticate_credentials(self, token= ''):
        return Token.objects.filter(key= token).first()

    def dispatch(self, request, *args, **kwargs):
        try:
            authorization_token = get_authorization_header(request).split()
            queryset = self.authenticate_credentials(token=authorization_token[1].decode())
            if queryset:
                if queryset.user.is_active:
                    is_expire = self.is_token_expired(queryset)
                    if not is_expire:
                        return super().dispatch(request, *args, **kwargs)
                    response = Response({
                        'error':'Token expirado.',
                        'message': 'El token de autenticación que proporcionó ha expirado. Por favor, inicie sesión nuevamente para obtener un nuevo token.'
                        },status=status.HTTP_401_UNAUTHORIZED)
                else: 
                    response = Response({
                        'error': 'Token no válido debido a la inactividad de la cuenta',
                        'message':'Su cuenta de usuario no está activa en este momento. Por favor, póngase en contacto con el soporte o el administrador del sistema para obtener más información.'},status=status.HTTP_403_FORBIDDEN)
            else:
                response = Response({
                    'error':'Token inválido.',
                    'message': 'El token de autenticación proporcionado no coincide con ningún registro válido. Verifique que ha proporcionado el token correcto o inicie sesión nuevamente para obtener un token válido.'},status=status.HTTP_401_UNAUTHORIZED)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            return response
        except IndexError:
            response = Response({
                    'error':'Token inválido.',
                    'message': 'El token de autenticación proporcionado no coincide con ningún registro válido. Verifique que ha proporcionado el token correcto o inicie sesión nuevamente para obtener un token válido.'},status=status.HTTP_401_UNAUTHORIZED)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            return response
