from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

# serializers
from apps.territories.api.serializers.territories import MunicipalitySerializer
from apps.territories.api.serializers.territories import MunicipalitySerializer, MunicipalityLocalitySerializer


class MunicipalityViewSet(GenericViewSet):
    serializer_class = MunicipalitySerializer

    def get_queryset(self, pk=None, pk_province=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(province=pk_province, active=1).order_by('name', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=1).first()

    def list(self, request):
        if 'province' in request.GET:
            queryset = self.get_queryset(pk_province=request.GET.get('province'))
            if queryset:
                serializer = MunicipalitySerializer(queryset, many=True)
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'No se encontraron municipios.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No se puede hace la solicitud debido a que no se encontró en el parámetro el argumento: "province".'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = MunicipalityLocalitySerializer(queryset)
            return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontró el municipio.'}, status=status.HTTP_404_NOT_FOUND)
