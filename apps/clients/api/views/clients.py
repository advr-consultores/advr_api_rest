
from rest_framework import status, viewsets
from rest_framework.response import Response

# serializers
from apps.clients.api.serializers.clients import ClientsSerializer
from apps.authentication.authtoken import TokenAuthentication
from apps.permissions.auth import IsAuthenticated


class ClientViewSet(IsAuthenticated, TokenAuthentication, viewsets.GenericViewSet):
    serializer_class = ClientsSerializer

    def get_queryset(self, pk=None, is_state=True):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=is_state)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def list(self, request):
        is_state = request.GET['estado'] if 'estado' in request.GET.keys() else True
        queryset = self.get_queryset(is_state=is_state)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'items': serializer.data, 'message': 'Se encontraron '+str(len(serializer.data))+' clientes registrados.'
            },status=status.HTTP_200_OK)
        return Response({'message': 'No se encontraron clientes registrados.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data, 'message': 'Cliente '+ serializer.data['name'] +' creado correctamente.'}, status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'items': serializer.data, 'message': 'Cliente '+ serializer.data['name'] +' modificado correctamente.'
                }, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'message': 'No se puede actualizar el cliente.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Cliente ' + queryset.name +' eliminado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Este cliente no se puede eliminar.'}, status=status.HTTP_404_NOT_FOUND)
