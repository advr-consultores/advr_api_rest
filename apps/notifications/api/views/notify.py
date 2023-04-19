from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


# serializers
from apps.works.api.serializers.work_history import WorkHistorySerializer

class NotificationsView(GenericViewSet):

    serializer_class = WorkHistorySerializer

    def get_queryset(self, user_fk=None):
        works_assigned_user = self.get_serializer().Meta.model.objects.filter(assigned_user=user_fk).exclude(history_user=user_fk)
        list_history_id = [work.history_id for work in works_assigned_user]
        print(list_history_id)
        works_area_user = self.get_serializer().Meta.model.objects.filter(area_user=user_fk).exclude(
            history_id__in=list_history_id, history_user=user_fk
        )
        return works_area_user | works_assigned_user

    @action(detail=False, methods=['get'])
    def trabajos(self, request):
        user_fk = request.GET['usuario'] if 'usuario' in request.GET.keys() else 0
        print(user_fk)
        queryset = self.get_queryset(user_fk=user_fk)
        if queryset:
            serializer = self.get_serializer(queryset, many = True)
            return Response({'items': serializer.data, 'message': 'of'}, status=status.HTTP_200_OK)
        return Response({'message': 'No '} , status=status.HTTP_404_NOT_FOUND)
