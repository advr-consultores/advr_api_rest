
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.projects.api.serializers.concepts import ConceptSerializer, ConceptCreateSerializer


class ConceptViewSet(GenericViewSet):
    serializer_class = ConceptSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True).order_by('name', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def create(self, request):
        serializer = ConceptCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el concepto con esos datos.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Concepto eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'El concepto ya fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)
