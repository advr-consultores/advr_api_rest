from rest_framework.viewsets import GenericViewSet
from rest_framework import status, response

# serializer
from apps.works.api.serializers.comments import CommentsSerializer
from apps.works.api.serializers.works import WorkRetrieveSerializer


class CommentViewSet(GenericViewSet):
    
    serializer_class = CommentsSerializer

    def get_queryset_work(self, pk=None):
        queryset = WorkRetrieveSerializer.Meta.model.objects.filter(id=pk).first()
        return WorkRetrieveSerializer(queryset)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                {'items': serializer.data, 'message': 'Comentario agregado.'},
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            {'items': serializer.errors, 'message': 'Comentario no agregado.'},
            status=status.HTTP_404_NOT_FOUND
        )
