from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.properties.api.serializers.property import PropertiesSerializer


class PropertyProvinceViewSet(GenericViewSet):
    serializer_class = PropertiesSerializer

    def get_queryset_province(self, province=None, municipality=None, locality=None):

        if province and municipality and locality:
            return self.get_serializer().Meta.model.objects.filter(
                province=province,
                municipality=municipality,
                locality=locality,
                state=True
            )
        if province and municipality:
            return self.get_serializer().Meta.model.objects.filter(
                province=province,
                municipality=municipality,
                state=True
            )
        return self.get_serializer().Meta.model.objects.filter(province=province, state=True)

    def get_queryset(self, clients=[], province=None, municipality=None, locality=None):

        if clients and province and municipality and locality:
            return self.get_serializer().Meta.model.objects.filter(
                client__in=clients,
                province=province,
                municipality=municipality,
                locality=locality,
                state=True
            )
        if clients and province and municipality:
            return self.get_serializer().Meta.model.objects.filter(
                client__in=clients,
                province=province,
                municipality=municipality,
                state=True
            )
        if clients and province:
            return self.get_serializer().Meta.model.objects.filter(client__in=clients, province=province, state=True)
        if clients:
            return self.get_serializer().Meta.model.objects.filter(client__in=clients, state=True)
        return self.get_serializer().Meta.model.objects.filter(state=True)
        # return self.get_serializer().Meta.model.objects.filter(
        #     client=client_pk
        # ).values('province').annotate(Count('province'))

    @action(detail=False, methods=['get'])
    def filtrado(self, request):
        try:
            clients = request.GET.get('clientes')
            province = request.GET.get('estado')
            municipality = request.GET.get('municipio')
            locality = request.GET.get('localidad')
            if clients:
                queryset = self.get_queryset(clients.split(','), province, municipality, locality)
            elif province or municipality or locality:
                queryset = self.get_queryset_province(province, municipality, locality)
            else:
                queryset = self.get_queryset()
            if queryset:
                serializer = self.get_serializer(queryset, many=True)
                return Response({'items': serializer.data, 'message': 'Inmuebles encontrados.'}, status=status.HTTP_200_OK)
            return Response({'error': 'No se encontraron inmuebles esta ubicación.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)