from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.territories.api.serializers.territories import ProvinceMunicipalitiesSerializer, ProvincesSerializer


class ProvinceViewSet(GenericViewSet):
    serializer_class = ProvinceMunicipalitiesSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return ProvincesSerializer().Meta.model.objects.filter(active=1).order_by('id', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=1).first()


    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = ProvincesSerializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontraron estados.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)
    

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se encontró el estado.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)
