from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# serializers
from apps.users.api.serializers.users import UserSerializers, UserPOSTPUTSerializers, UserPartialSerializers


class UserViewSet(GenericViewSet):

    serializer_class = UserPOSTPUTSerializers

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(is_active=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, is_active=True).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = UserSerializers(queryset, many=True)
            return Response(
                {'items': serializer.data, 'message': 'Consulta exitosa.'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'No se encontraron usuarios.',
                'error': 'Consulta no satisfactoria.'},
            status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'items': serializer.data, 'message': 'Usuario creado correctamente.'},
                status=status.HTTP_201_CREATED
            )
        return Response({'message': 'Solicitud no aceptada.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = UserSerializers(queryset)
            return Response(
                {'items': serializer.data, 'message': 'Consulta exitosa.'},
                status=status.HTTP_200_OK
            )
        return Response({'message': 'No se encontro el usuario.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.get_serializer(queryset, data=request.data)
            if serializer.is_valid():
                if check_password(request.data['password'], queryset.password):
                    serializer.save()
                    return Response(
                        {'items': serializer.data,
                            'message': 'La solicitud ha tenido éxito.'},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {'message': 'La contraseña es incorrecta.',
                        'error': 'Usuario no actualizado.'},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            return Response({'message': 'Solicitud incorrecta.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se encontro el usuario.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.image.delete()
            serialize = UserPartialSerializers(queryset, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response({'items': serialize.data, 'message': 'La solicitud ha tenido éxito.'}, status=status.HTTP_200_OK)
            return Response({'error': serialize.errors, 'message': 'Solicitud incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No se encontro el usuario', 'message': 'Consulta no satisfactoria'}, status=status.HTTP_404_NOT_FOUND)

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
