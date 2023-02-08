
from django.db.models import Count

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.properties.models import Property

from apps.territories.api.serializers.territories import LocalitySerializer


class LocalityViewSet(GenericViewSet):

    serializer_class = LocalitySerializer

    def get_queryset(self, pk=None, pk_municipality=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(municipality=pk_municipality, active=1).order_by('name', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=1).first()

    def list(self, request):
        municipality = request.GET.get('municipality')
        if municipality:
            queryset = self.get_queryset(pk_municipality=municipality)
            if queryset:
                serializer = self.get_serializer(queryset, many=True)
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'No se encontraron localidades.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No se puede hace la solicitud debido a que no se encontró en el parámetro el argumento: "municipality".'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontró la localidad.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def sucursales(self, request):

        clients = request.GET.get('clients')
        province = request.GET.get('province')
        municipality = request.GET.get('municipality')
        localidades = []

        if province and municipality:
            if clients:
                queryset = Property.objects.filter(
                    client__in=clients.split(','), province=province, municipality=municipality, state=True).values(
                    'locality').annotate(Count('locality')).exclude(locality=None)
            else:
                queryset = Property.objects.filter(
                    province=province, municipality=municipality, state=True).values(
                    'locality').annotate(Count('locality')).exclude(locality=None)
            if queryset:
                for locality in queryset:
                    pk = locality['locality']
                    # # municipality__count = municipality['municipality__count']
                    queryset = self.get_queryset(pk)
                    serializer = self.get_serializer(queryset)
                    localidades.append(serializer.data)
                return Response({'items':  localidades}, status=status.HTTP_200_OK)
            return Response({'message': 'No se encontraron inmuebles en esa localidad.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No se puede hace la solicitud debido a que no se encontró en el parámetro uno de los argumentos: "province" o "municipality".'}, status=status.HTTP_400_BAD_REQUEST)
