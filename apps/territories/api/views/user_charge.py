from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


# serializer
from apps.users.api.serializers.user_charge import UserChargeProvincesSerializers

class UserChargeTerritoriesViewSet(GenericViewSet):

    serializer_class = UserChargeProvincesSerializers

    def get_queryset_user_charge(self, state=True, fk_user_charge=None):
        if fk_user_charge:
            return self.get_serializer().Meta.model.objects.filter(state=state, charge=fk_user_charge).first()
        return None
    
    @action(detail=True, methods=['get'])
    def estados(self, request, pk=None):
        queryset = self.get_queryset_user_charge(fk_user_charge=pk)
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response({
                'items': serializer.data,
                'message': 'Se detallaron los estados con el usuario a cargo (coordinado).'
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'La búsqueda no arrojó resultados',
            'message': 'No se identificaron estados con el usuario a cargo (coordinado).'
        }, status=status.HTTP_404_NOT_FOUND)
