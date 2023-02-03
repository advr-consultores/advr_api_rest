from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.groups.api.serializers.groups import PermissionsSerializer


class PermissionViewSet(GenericViewSet):
    serializer_class = PermissionsSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Consulta no satisfactoria'}, status=status.HTTP_404_NOT_FOUND)
