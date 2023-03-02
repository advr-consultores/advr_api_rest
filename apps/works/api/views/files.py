
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


# serializers
from apps.works.api.serializers.serializers import FileSerializer


class FileViewSet(GenericViewSet):
    serializer_class = FileSerializer

    def get_queryset(self, pk):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response('El trabajo dejo de existir', status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.delete()
            return Response({'message': 'Archivo eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'El archivo ya fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)

