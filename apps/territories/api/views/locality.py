from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

# serializers
from apps.territories.api.serializers.territories import LocalitySerializer


class LocalityViewSet(GenericViewSet):

    serializer_class = LocalitySerializer

    def get_queryset(self, pk=None, pk_municipality=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(municipality=pk_municipality, active=1).order_by('name', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=1).first()

    def list(self, request):
        if 'municipality' in request.GET:
            queryset = self.get_queryset(pk_municipality=request.GET.get('municipality'))
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
