from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# serializers
from apps.authentication.serializers import UserLoginSerializer, LoginCredentialSerializer
from apps.users.api.serializers.users import UserGetUsernameSerializer

#views
from apps.authentication.authtoken import TokenAuthentication


class Credential():

    def __init__(self, credentials):
        self.data = {
            'username': '',
            'password': credentials['password'],
        }
        self.find_username(account=credentials['account'])

    def find_username(self, account=''):
        queryset = UserGetUsernameSerializer().Meta.model.objects.filter(username=account).first()
        if not queryset:
            queryset = UserGetUsernameSerializer().Meta.model.objects.filter(email=account).first()
        if queryset:
            self.set_data_username(username=queryset.username)

    def set_data_username(self, username=''):
        self.data['username'] = username

    def get_data(self):
        return self.data


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = LoginCredentialSerializer(data=request.data)
        if serializer.is_valid():
            credential = Credential(request.data)
            serializer = self.serializer_class(
                data=credential.get_data(),
                context={'request': request}
            )
            if serializer.is_valid():
                user = serializer.validated_data['user']
                if user.is_active:
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
                else:
                    return Response({
                        'error': 'No tienes permitido iniciar sesión.',
                        'message': 'Asegúrate de que estás utilizando las credenciales correctas y que cuentas con los permisos necesarios.'
                    },status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'error': 'El usuario o contraseña son incorrectos.',
                'message': 'Verifica tu nombre de usuario y contraseña e intenta iniciar sesión nuevamente',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'Por favor, completa la información necesaria.',
            'errors': serializer.errors,
            'message': 'Asegúrate de proporcionar la información requerida antes de proceder.'},
        status=status.HTTP_400_BAD_REQUEST)
