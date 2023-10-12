from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import get_authorization_header


class IsAuthenticated(object):

    def dispatch(self, request, *args, **kwargs):
        is_provided_auth_credentials = get_authorization_header(request)
        if is_provided_auth_credentials:
            return super().dispatch(request, *args, **kwargs)
        response = Response({
                'error': 'Credenciales de autenticación no proporcionadas.',
                'message':'Las credenciales de autenticación no fueron incluidas en la solicitud. Por favor, proporcione las credenciales adecuadas (por ejemplo, un token de autenticación) para acceder a este recurso.'
            },status=status.HTTP_401_UNAUTHORIZED
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
