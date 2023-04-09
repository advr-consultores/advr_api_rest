from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.groups.api.serializers.groups import GroupsSerializer, GroupSerializer


class GroupsViewSet(GenericViewSet):
    serializer_class = GroupsSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Se encontraron ' + str(len(queryset)) + ' grupos.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontraron grupos, consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = GroupSerializer(queryset)
            if serializer:
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Consulta no satisfactoria'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        return Response({'message': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data, 'message': 'Grupo actualizado'}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_409_CONFLICT)
        return Response({'message': 'Consulta no satisfactoria'}, status=status.HTTP_409_CONFLICT)
