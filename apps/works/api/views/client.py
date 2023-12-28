from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.works.api.serializers.serializers import WorksPropertySerializer
from apps.properties.models import Property

class WorkClientViewSet(GenericViewSet):

    serializer_class = WorksPropertySerializer

    def get_queryset(self, list_fk_property=[]):
        return self.get_serializer().Meta.model.objects.filter(property_office__in=list_fk_property, state=True).all()

    def get_queryset_property(self, fk_client=None, fk_province=None):
        if fk_province:
            return Property.objects.values_list('id', flat=True).filter(client=fk_client, province=fk_province, state=True).exclude(works=None).all()
        return Property.objects.values_list('id', flat=True).filter(client=fk_client, state=True).exclude(works=None).all()

    def retrieve(self, request, pk=None):
        fk_province = request.GET.get('estado')
        list_property = self.get_queryset_property(fk_client=pk, fk_province=fk_province)
        if len(list_property):
            queryset = self.get_queryset(list_fk_property=list_property)
            serializer = self.serializer_class(queryset, many=True)
            return Response({'items': serializer.data, 'meesage': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontraron trabajos relacionados al cliente.'}, status=status.HTTP_404_NOT_FOUND)
