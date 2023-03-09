from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

# serializers
from apps.resources.api.serializers.comment import CommentSerializers, CommentsSerializer


class CommentViewSet(GenericViewSet):
    serializer_class = CommentSerializers

    def get_queryset(self, pk=None, pk_resource=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(resource = pk_resource,state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data, 'message': 'Se actualizo el comentario.'}, status=status.HTTP_202_ACCEPTED)
            return Response({'error': serializer.errors, 'message': 'No se ha actualizado el comentario.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se pudo encontrar el contenido solicitado.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data, 'message': 'Se agregó el comentario.'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': serializer.errors, 'message': 'No se ha agregado el comentario.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        resource = request.GET.get('resource')
        queryset = self.get_queryset(pk_resource =resource)
        if queryset:
            serializer = CommentsSerializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Se obtuvieron los comentarios de recurso.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se obtuvieron los comentarios de recurso.'}, status=status.HTTP_404_NOT_FOUND)
            
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Comentario eliminado.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se pudo encontrar el contenido solicitado.'}, status=status.HTTP_404_NOT_FOUND)
