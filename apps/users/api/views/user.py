from django.contrib.auth.hashers import check_password
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


# serializers
from apps.users.api.serializers.users import *

# views
from apps.email.api.views.sendVerificationEmail import SendVerificationEmail


# from apps.authentication.authtoken import TokenAuthentication
# from apps.permissions.auth import IsAuthenticated

class UserViewSet(GenericViewSet):

    serializer_class = UserPOSTPUTSerializers

    def get_queryset(self, pk=None, is_active=True, group=None):
        if pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()
        if group:
            return self.get_serializer().Meta.model.objects.filter(groups=group, is_active=is_active).all()
        return self.get_serializer().Meta.model.objects.filter(is_active=is_active).all()

    def list(self, request):
        group = request.GET.get('grupo', None)
        is_active = request.GET.get('activo', True)
        queryset = self.get_queryset(group=group, is_active=is_active)
        if queryset:
            serializer = UsersSerializers(queryset, many=True)
            user = serializer.data
            return Response({'users': user, 'message': 'Usuarios encontrados con éxito.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Usuarios no encontrados.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                absurl = settings.CORS_ALLOWED_ORIGINS[0]
                data_send_email = SendVerificationEmail.sendEmial({
                    'subject': '¡Activación exitosa!',
                    'message': "¡Te acaban de registrar para obtener una cuenta en Antasoft!\nPara comenzar, solo necesitas acceder a la siguiente página utilizando tu dirección de correo electrónico de la empresa y la nueva contraseña que te hemos asignado:\n"+absurl,
                    'from_email': '',
                    'recipient_list': [serializer.data['email']]
                })
                return Response({
                    'user': serializer.data, 'message': 'El usuario ha sido creado correctamente.',
                    'data_send': data_send_email.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Usuario no creado, debido a la falta de datos necesarios o porque el usuario ya existe.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = UserSerializers(queryset)
            return Response({
                'user': serializer.data, 'message': 'Consulta exitosa.'
            }, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el usuario.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = UserUpdateSerializers(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'user': serializer.data, 'message': 'La solicitud ha tenido éxito.'
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Solicitud incorrecta.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Usuario con ID {} no encontrado.'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['patch'])
    def password(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = UserPasswordSerializers(queryset, data=request.data)
            if serializer.is_valid():
                if check_password(request.data['old_password'], queryset.password):
                    serializer.save()
                    return Response({'message': 'Contraseña actualizada con éxito.'}, status=status.HTTP_200_OK)
                return Response({
                    'message': 'Contraseña vieja no coincide; actualización de contraseña fallida.',
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Solicitud incorrecta.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Usuario con ID {} no encontrado.'.format(pk)}, status=status.HTTP_404_NOT_FOUND) 


    @action(detail=True, methods=['patch'])
    def personal(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serialize = UserStaffSerializers(queryset, data=request.data)
            if serialize.is_valid():
                if not request.data['is_staff']:
                    queryset.groups.clear()
                serialize.save()
                return Response({
                    'user': serialize.data,
                    'message': 'Se actualizaron los permisos del usuario.'
                }, status=status.HTTP_200_OK)
            return Response({
                'errors': serialize.errors,
                'message': 'No se actualizaron los permisos del usuario.'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Usuario con ID {} no encontrado.'.format(pk)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def grupos(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.is_staff:
                serialize = UserGroupsSerializers(queryset, data=request.data)
                if serialize.is_valid():
                    serialize.save()
                    return Response({
                        'user': serialize.data,
                        'message': 'Privilegios de usuario asignados/actualizados con éxito.'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'errors': serialize.errors,
                    'message': 'Falló la asignación/actualización de privilegios del usuario.'
                },status=status.HTTP_403_FORBIDDEN)
            return Response({
                'message': 'El usuario no tiene el permiso de staff necesario para recibir estos privilegios.'
            }, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Usuario con ID {} no encontrado.'.format(pk)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def imagen(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.image.delete()
            serialize = UserImagenPartialSerializers(queryset, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response({'user': serialize.data, 'message': 'La solicitud ha tenido éxito.'}, status=status.HTTP_200_OK)
            return Response({'error': serialize.errors, 'message': 'Solicitud incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Consulta no satisfactoria.', 'message': 'No se encontro el usuario.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.is_superuser is False:
                if queryset.is_active:
                    queryset.is_active = False
                    queryset.is_staff = False
                    queryset.groups.clear()
                    queryset.save()
                    return Response({'message': 'Usuario desactivado correctamente.'}, status=status.HTTP_200_OK)
                return Response({
                    'message': 'El usuario que intenta desactivar ya se encuentra en estado desactivado.'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'message': 'Estos usuarios no pueden ser desactivados debido a su rol y nivel de acceso.'
            }, status=status.HTTP_403_FORBIDDEN)
        return Response({
            'message': 'Usuario con ID {} no encontrado.'.format(pk)
        }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def activar(self, reques, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if not queryset.is_active:
                queryset.is_active = True
                queryset.save()
                return Response({'message': 'Usuario con ID {} reactivado con éxito.'.format(pk)}, status=status.HTTP_200_OK)
            return Response({'message': 'Usuario ya activo; no es necesario reactivarlo '}, status=status.HTTP_409_CONFLICT)
        return Response({ 'message': 'Usuario con ID {} no encontrado.'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
