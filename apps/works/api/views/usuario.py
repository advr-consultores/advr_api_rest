
from http import server
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User

from apps.works.api.serializers.users import WorksUserListSerializer


class WorksUsuarioViewSet(GenericViewSet):

    serializer_class = WorksUserListSerializer

    def get_queryset(self, pk_user):
        return self.get_serializer().Meta.model.objects.filter(assigned_user=pk_user)

    def get_queryset_user(self, username=None):
        return User.objects.filter(username=username).first()

    def list(self, request):
        username = request.GET.get('username')
        user = self.get_queryset_user(username)
        if user:
            queryset = self.get_queryset(user.id)
            if queryset:
                serializer = self.serializer_class(queryset, many= True)
                return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
            return Response({'message': 'No tiene trabajos asignados por el momento', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No se encontro el usuario con ese nombre de usuario.', 'error': 'Consulta no satisfactoria.'}, status=status.HTTP_404_NOT_FOUND)

