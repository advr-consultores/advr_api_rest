from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# serializers
from apps.authentication.serializers import UserLoginSerializer
from apps.users.api.serializers.users import UserGetUsernameSerializer


class Credential():

    def __init__(self, credentials):
        self.data = {
            'email': credentials['email'],
            'username': credentials['username'],
            'password': credentials['password'],
        }
        self.find_username()

    def find_username(self):
        if self.data['username'] is None:
            queryset = UserGetUsernameSerializer().Meta.model.objects.filter(
                email=self.data['email']
            ).first()
            if queryset:
                self.set_data_username(queryset.username)
        return None

    def set_data_username(self, username):
        self.data['username'] = username

    def get_data(self):
        return self.data


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
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
                if created:
                    return Response({
                        'token': token.key,
                        'user': serializer.data,
                        'message': 'Inicio de sesion exitoso'
                    }, status=status.HTTP_201_CREATED)
                else:
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'user': serializer.data,
                        'message': 'Inicio de sesion exitoso'
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({'messgae': 'No tienes permitido iniciar sesi??n.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'El usuario o contrase??a son incorrectos'}, status=status.HTTP_400_BAD_REQUEST)