from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

# models
from apps.users.models import User

#serializers
from apps.works.api.serializers.users import WorksUserListSerializer
from apps.authentication.authtoken import TokenAuthentication
from apps.permissions.auth import IsAuthenticated


class WorksUsuarioViewSet(IsAuthenticated, TokenAuthentication, GenericViewSet):

    serializer_class = WorksUserListSerializer

    def get_queryset(self, pk_user=None, area_user=None, assigned_user=None):
        if area_user is not None:
            return self.get_serializer().Meta.model.objects.filter(area_user=pk_user, state=True).all()
        if assigned_user is not None:
            return self.get_serializer().Meta.model.objects.filter(assigned_user=pk_user).all()

    def get_queryset_user(self, username=None):
        return User.objects.filter(username=username).first()

    def list(self, request):
        area_user = request.GET.get('usuario_area', None)
        assigned_user = request.GET.get('usuario_asignado', None)
        if assigned_user or area_user:
            username = assigned_user if assigned_user is not None else area_user
            user = self.get_queryset_user(username)
            if user:
                queryset = self.get_queryset(pk_user=user.id, area_user=area_user, assigned_user=assigned_user)
                if queryset:
                    serializer = self.serializer_class(queryset, many= True)
                    return Response({'items': serializer.data, 'message': 'Tienes '+ str(len(queryset)) + ' trabajos asignados.'}, status=status.HTTP_200_OK)
                return Response({'message': 'No tiene trabajos asignados por el momento'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'No se encontro el usuario con ese nombre de usuario.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No se definió ninguno de los dos parámetros.', 'error': 'La solicitud fue incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

