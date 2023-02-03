from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.groups.api.serializers.groups import GroupsSerializer, GroupSerializer


class GroupsViewSet(GenericViewSet):
    serializer_class = GroupsSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            if serializer:
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': 'Error en el seializer'}, status=status.HTTP_409_CONFLICT)
        return Response({'message': 'Consulta no satisfactoria'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = GroupSerializer(queryset)
            if serializer:
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Consulta no satisfactoria'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data, 'message': 'Grupo actualizado'}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_409_CONFLICT)
        return Response({'message': 'Consulta no satisfactoria'}, status=status.HTTP_409_CONFLICT)
