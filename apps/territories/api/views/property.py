from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


# models
from apps.properties.models import Property

# 
from apps.territories.api.serializers.territories import ProvinceSerializer, MunicipalitySerializer


class PropertyTerritoriesViewSet(GenericViewSet):

    serializer_class_province = ProvinceSerializer
    serializer_class_municipality = MunicipalitySerializer

    def get_queryset_property(self, fk_client=None, fk_province=None):
        if fk_province:
            if fk_client:
                return Property.objects.values('municipality').filter(state=True, client=fk_client, province=fk_province).annotate(Count('municipality'))
            return Property.objects.values('municipality').filter(state=True, province=fk_province).annotate(Count('municipality'))
        if fk_client:
            return Property.objects.values_list('province', flat=True).filter(state=True, client=fk_client,).annotate(Count('province'))
        return Property.objects.values_list('province', flat=True).filter(state=True).annotate(Count('province'))

    def get_queryset(self, list_province=[], list_municipality=[]):
        if len(list_province):
            return self.serializer_class_province.Meta.model.objects.filter(id__in=list_province).all()
        return self.serializer_class_municipality().Meta.model.objects.filter(id__in=list_municipality).all()
    
    @action(detail=False, methods=['get'])
    def estados(self, request):
        fk_client = request.GET.get('cliente', None)
        queryset = self.get_queryset_property(fk_client=fk_client)
        exclude = request.GET.get('excluir_trabajos', 'false')
        queryset = queryset.exclude(works=None) if exclude == 'true' else queryset

        if queryset:
            queryset = self.get_queryset(list_province=list(queryset))
            serializer = self.serializer_class_province(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Se listaron los estados con inmuebles exitosamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'La búsqueda no arrojó resultados', 'message': 'No se encontraron estados con inmuebles.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def municipios(self, request):
        if 'estado' in request.GET:
            municipalities = []
            queryset = self.get_queryset_property(fk_client=request.GET.get('cliente', None), fk_province=request.GET.get('estado'))
            if queryset:
                for municipality in queryset:
                    municipalities.append(municipality.get('municipality'))
                queryset = self.get_queryset(list_municipality=municipalities)
                serializer = self.serializer_class_municipality(queryset, many=True)
                data_provinces = { 'municipalities': serializer.data }
                return Response({'items': data_provinces, 'message': 'Se listaron los municipios con inmuebles exitosamente.'}, status=status.HTTP_200_OK)
            return Response({'error': 'La búsqueda no arrojó resultados', 'message': 'No se encontraron municipios con inmuebles.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Error en la solicitud', 'message': 'El campo "estado" es requerido. Por favor, proporcione el valor para "estado" e inténtelo nuevamente.'}, status=status.HTTP_400_BAD_REQUEST)
