from django.contrib.auth.hashers import check_password

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

    def get_queryset(self, pk=None, group=None):
        if pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()
        if group:
            return self.get_serializer().Meta.model.objects.filter(groups=group).all()
        return self.get_serializer().Meta.model.objects.all()

    def list(self, request):
        group = request.GET['grupo'] if request.GET.keys() else None
        queryset = self.get_queryset(group=group)
        if queryset:
            serializer = UsersSerializers(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Se encontraron ' + str(len(queryset)) + ' usuarios.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontraron usuarios que cumplan con los criterios de búsqueda especificados. Por favor, verifique los parámetros de búsqueda o intente con diferentes criterios.', 'error': 'Usuarios no encontrados'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                absurl = "http://"
                data_send_email = SendVerificationEmail.sendEmial({
                    'subject': '¡Activa tu cuenta ahora!',
                    'message': "¡Hola!\n¡Te acaban de registrar para obtener una cuenta en ADVR sistem(Antasoft)!\nPara comenzar, solo necesitas acceder a la siguiente página utilizando tu dirección de correo electrónico de la empresa y la nueva contraseña que te hemos asignado:\n"+absurl,
                    'from_email': '',
                    'recipient_list': [serializer.data['email']]
                })
                print(data_send_email.data)
                return Response({
                    'items': serializer.data, 'message': 'Usuario ' + serializer.data["username"] +' creado correctamente.'
                }, status=status.HTTP_201_CREATED)
            return Response({
                'error': 'Usuario no creado',
                'message': 'La solicitud de creación de usuario no puede ser procesada debido a la falta de datos necesarios o porque el usuario ya existe. Por favor, verifique los datos proporcionados y asegúrese de que no exista un usuario con la misma información.',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = UserSerializers(queryset)
            return Response({
                'items': serializer.data, 'message': 'Consulta exitosa.'
            }, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el usuario.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.get_serializer(queryset, data=request.data)
            if serializer.is_valid():
                if check_password(request.data['password'], queryset.password):
                    serializer.save()
                    return Response({
                        'items': serializer.data, 'message': 'La solicitud ha tenido éxito.'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'message': 'La contraseña es incorrecta.',
                    'error': 'Usuario no actualizado.'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'message': 'Solicitud incorrecta.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se encontro el usuario.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def permisos(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serialize = UserPermissionsSerializers(queryset, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response({
                    'items': serialize.data,
                    'message': 'Se actualizaron los permisos del usuario ' + queryset.username + '.'
                }, status=status.HTTP_200_OK)
            return Response({
                'error': serialize.errors,
                'message': 'No se actualizaron los permisos del usuario ' + queryset.username + '.'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Consulta no satisfactoria.', 'message': 'No se encontro el usuario.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'])
    def grupos(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.is_staff:
                serialize = UserGroupsSerializers(queryset, data=request.data)
                if serialize.is_valid():
                    serialize.save()
                    return Response({
                        'items': serialize.data,
                        'message': 'Se actualizaron los privilegios del usuario ' + queryset.username + '.'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'Asignación de privilegios no válida',
                    'errors': serialize.errors,
                    'message': 'No se actualizaron los privilegios del usuario ' + queryset.username + '.'
                },status=status.HTTP_403_FORBIDDEN)
            return Response({
                'error': 'No se pueden asignar privilegios al usuario',
                'message': 'El usuario no tiene el permiso de staff necesario para recibir estos privilegios. Por favor, contacte a un administrador o al personal autorizado para solicitar cambios en los privilegios.'
                }, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'Usuario no encontrado', 'message': 'El usuario solicitado no se encuentra en la base de datos o no existe.'}, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['patch']) imagen
    def partial_update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.image.delete()
            serialize = UserImagenPartialSerializers(queryset, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response({'items': serialize.data, 'message': 'La solicitud ha tenido éxito.'}, status=status.HTTP_200_OK)
            return Response({'error': serialize.errors, 'message': 'Solicitud incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Consulta no satisfactoria.', 'message': 'No se encontro el usuario.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.is_superuser is False:
                if queryset.is_active:
                    queryset.is_active = False
                    queryset.is_staff = False
                    queryset.groups.set([])
                    queryset.save()
                    return Response({'message': 'Usuario desactivado correctamente.'}, status=status.HTTP_200_OK)
                return Response({
                    'error': 'No se puede desactivar el usuario',
                    'message': 'El usuario que intenta desactivar ya se encuentra en estado desactivado. No es necesario realizar esta acción nuevamente.'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'error': 'No se puede desactivar el administrador',
                'message': 'El usuario que intenta desactivar es un administrador con permisos especiales. Estos usuarios no pueden ser desactivados debido a su rol y nivel de acceso. Si necesita realizar cambios en la cuenta del super usuario, por favor, contacte al administrador del sistema o al soporte técnico para obtener asistencia.'
            }, status=status.HTTP_403_FORBIDDEN)
        return Response({
            'error': 'Usuario no encontrado.',
            'message': 'El usuario que intenta desactivar no existe. Por favor, verifique que ha proporcionado el nombre de usuario o el identificador correcto e intente de nuevo'
            }, status=status.HTTP_404_NOT_FOUND)
