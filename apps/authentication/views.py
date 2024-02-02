from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

import datetime

# serializers
from apps.authentication.serializers import UserLoginSerializer, LoginCredentialSerializer
from apps.users.api.serializers.users import UserGetUsernameSerializer

#views
from apps.authentication.authtoken import TokenAuthentication


class Login(ObtainAuthToken):

    def get_queryset_username(self, email):
        return UserGetUsernameSerializer().Meta.model.objects.filter(email=email).first()

    def post(self, request, *args, **kwargs):
        serializer_credential = LoginCredentialSerializer(data=request.data)
        if serializer_credential.is_valid():
            queryset_username = self.get_queryset_username(request.data['email'])
            if queryset_username:
                serializer_user = UserGetUsernameSerializer(queryset_username)
                if serializer_user.data['is_active']:
                    serializer = self.serializer_class(
                        data={'username': serializer_user.data['username'], 'password': request.data['password']},
                        context={'request': request}
                    )
                    if serializer.is_valid():
                        user = serializer.validated_data['user']
                        user.last_login = datetime.datetime.now()
                        token, created = Token.objects.get_or_create(user=user)
                        serializer = UserLoginSerializer(user)
                        class_token = TokenAuthentication()
                        if not created:
                            if class_token.is_token_expired(token):
                                token.delete()
                                token = Token.objects.create(user=user)
                        return Response({
                            'token': token.key,
                            'user': serializer.data,
                            'message': 'Inicio de sesion exitoso.'
                        }, status=status.HTTP_201_CREATED)
                    return Response({
                        'message': 'La contraseña que has introducido es incorrecta.',
                        'errors': { 'password': ['No puede iniciar sesión con la contraseña proporcionadas.']},
                        }, status=status.HTTP_401_UNAUTHORIZED)
                return Response({
                    'message': 'No tienes permitido iniciar sesión.',
                    'errors': {
                        'is_active': ['No cuentas con el permiso necesario']
                    }
                },status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'message': 'No se ha podido encontrar tu correo con la información proporcionada.',
                'errors': {'email': ['No hemos podido encontrar la cuenta solicitada.'] }
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'errors': serializer_credential.errors,
            'message': 'Asegúrate de proporcionar la información requerida antes de proceder.'},
        status=status.HTTP_400_BAD_REQUEST)
