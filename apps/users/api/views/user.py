from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


# serializers
from apps.users.api.serializers.users import *


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
        return Response({'message': 'No se encontraron usuarios.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'items': serializer.data, 'message': 'Usuario ' + serializer.data["username"] +' creado correctamente.'
            }, status=status.HTTP_201_CREATED)
        return Response({'message': 'Solicitud no aceptada.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
            if queryset.is_active and queryset.is_staff:
                serialize = UserGroupsSerializers(queryset, data=request.data)
                if serialize.is_valid():
                    serialize.save()
                    return Response({
                        'items': serialize.data,
                        'message': 'Se actualizaron los privilegios del usuario' + queryset.username + '.'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': serialize.errors,
                    'message': 'No se actualizaron los privilegios del usuario ' + queryset.username + '.'
                },status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Consulta no satisfactoria.', 'message': 'No se pueden asignar los privilegios por los permisos que tiene el usuario.'})
        return Response({'error': 'Consulta no satisfactoria.', 'message': 'No se encontro el usuario.'}, status=status.HTTP_404_NOT_FOUND)

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
            queryset.is_active = False
            queryset.save()
            return Response({'message': 'Usuario eliminado correctamente.'}, status=status.HTTP_200_OK)
        return Response(
            {'message': 'No se encontro el usuario.',
                'error': 'Consulta no satisfactoria.'},
            status=status.HTTP_404_NOT_FOUND
        )
