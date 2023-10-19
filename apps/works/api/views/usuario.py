from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

# models
from apps.users.models import Charge
from apps.properties.models import Property

#serializers
# from apps.works.api.serializers.users import WorksUserListSerializer
from apps.properties.api.serializers.works import PropertiesWorkSerializer
from apps.users.api.serializers.user_charge import UserChargeProvinceIdSerializers
# from apps.authentication.authtoken import TokenAuthentication
# from apps.permissions.auth import IsAuthenticated


class WorksUsuarioViewSet(GenericViewSet):

    serializer_class = PropertiesWorkSerializer

    def get_queryset(self, fk_province=[]):
        return self.get_serializer().Meta.model.objects.filter(province__in=fk_province, state=True).all().exclude(works=None)

    def get_queryset_user(self, username=None):
        return Charge.objects.filter(charge=username).first()

    def list(self, request):
        area_user = request.GET.get('usuario_cargo', None)
        assigned_user = request.GET.get('usuario_campo', None)
        if assigned_user or area_user:
            username = assigned_user if assigned_user is not None else area_user
            user = self.get_queryset_user(username)
            if user:
                serializer = UserChargeProvinceIdSerializers(user)
                list_province = serializer.data['province']
                queryset = self.get_queryset(fk_province=list_province)
                if queryset:
                    serializer = self.get_serializer(queryset, many= True)
                    return Response({'items': serializer.data, 'message': 'Tienes '+ str(len(queryset)) + ' trabajos asignados.'}, status=status.HTTP_200_OK)
                return Response({
                    'error': 'No se han creado trabajos por el momento.',
                    'message': 'Por favor, diríjase a su lista de inmuebles para empezar a asignar trabajos.'}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'error': 'No se han asignado trabajos por el momento porque no te han asignado un estado a cargo.',
                'message': 'Por favor, pídele alguien encado para que te asignen un estado para poder crear trabajos.'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se definió ninguno de los dos parámetros.', 'error': 'La solicitud fue incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

