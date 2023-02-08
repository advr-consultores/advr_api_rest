
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import Count

from apps.territories.api.serializers.territories import MunicipalitySerializer

from apps.properties.models import Property
from apps.territories.models import Municipality

from apps.territories.api.serializers.territories import MunicipalitySerializer, MunicipalityLocalitySerializer


class MunicipalityViewSet(GenericViewSet):
    serializer_class = MunicipalitySerializer

    def get_queryset(self, pk=None, pk_province=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(province=pk_province, active=1).order_by('name', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=1).first()

    def list(self, request):
        province = request.GET.get('province')
        if province:
            queryset = self.get_queryset(pk_province=province)
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

    @action(detail=False, methods=['get'])
    def sucursales(self, request):
        province = request.GET.get('province')
        clients = request.GET.get('clients')
        if province:
            municipios = []
            if clients:
                queryset = Property.objects.filter(client__in=clients.split(','), province=province, state=True).values(
                    'municipality').annotate(Count('municipality'))
            else:
                queryset = Property.objects.filter(province=province, state=True).values(
                    'municipality').annotate(Count('municipality'))
            if queryset:
                for municipality in queryset:
                    pk = municipality['municipality']
                    # municipality__count = municipality['municipality__count']
                    queryset = Municipality.objects.filter(id=pk).first()
                    serializer = MunicipalitySerializer(queryset)
                    municipios.append(serializer.data)
                return Response({'items': municipios}, status=status.HTTP_200_OK)
            return Response({'message': 'No se encontraron inmuebles en ese estado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No se puede hace la solicitud debido a que no se encontró en el parámetro el argumento: "province".'}, status=status.HTTP_400_BAD_REQUEST)
