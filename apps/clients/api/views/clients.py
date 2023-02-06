
from rest_framework import status, viewsets
from rest_framework.response import Response

# serializers
from apps.clients.api.serializers.clients import ClientsSerializer


class ClientViewSet(viewsets.GenericViewSet):
    serializer_class = ClientsSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializers = self.get_serializer(queryset, many=True)
            return Response({'items': serializers.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data, 'message': 'Cliente creado.'}, status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                'error': 'Consulta no satisfactoria o se elimino con anterioridad.'
            }, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Cliente eliminado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Cliente eliminado con anterioridad.'}, status=status.HTTP_404_NOT_FOUND)
