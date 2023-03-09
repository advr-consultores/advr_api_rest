from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.works.api.serializers.works import WorkStatusSerializer

class WorkStatusViewSet(GenericViewSet):
    serializer_class = WorkStatusSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items':serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No hay status de trabajo'}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'items': serializer.data, 'message': 'Se creó exitosamente el status del trabajo.'}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # def destroy(self, request, pk=None):
    #     queryset = self.get_queryset(pk)
    #     if queryset:
    #         queryset.state = False
    #         queryset.save()
    #         return Response({'message': 'Status de trabajo eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
    #     return Response({'error': 'El status de trabajo fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)
