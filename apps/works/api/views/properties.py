from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.properties.api.serializers.works import PropertiesWorkSerializer

class PropertiesViewSet(GenericViewSet):

    serializer_class = PropertiesWorkSerializer

    def get_queryset(self, pk_client=None):
        return self.get_serializer().Meta.model.objects.filter(client = pk_client, state = True).exclude(works = None)

    def list(self, request):
        pk_client = request.GET.get('cliente')
        queryset = self.get_queryset(pk_client)
        if queryset:
            serializer_property = self.serializer_class(queryset, many=True)
            list_works = []
            for property in serializer_property.data:
                for work in property['works']:
                    if work['state']:
                        list_works.append(work)
            return Response({'items': list_works, 'meesage': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontraron trabajos relacionados al cliente.'}, status=status.HTTP_404_NOT_FOUND)
