from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

# serializers
from apps.users.api.serializers.user_charge import UserChargeSerializers, UserChargeSerializersUserProvinceSerializers


class UserChargeViewSet(GenericViewSet):

    serializer_class = UserChargeSerializers

    def get_queryset(self, pk=None, fk_user=None, fk_province=None):
        if pk:
            return self.get_serializer().Meta.model.objects.filter(state=True, id=pk).first()
        elif fk_user and fk_province:
            return self.get_serializer().Meta.model.objects.filter(state=True, charge=fk_user, province__in=fk_province).all()
        elif fk_user:
            return self.get_serializer().Meta.model.objects.filter(state=True, charge=fk_user).all()
        elif fk_province:
            return self.get_serializer().Meta.model.objects.filter(state=True, province__in=fk_province).all()
        else:
            return self.get_serializer().Meta.model.objects.filter(state=True).all()
    

    def list(self, request):
        try:
            fk_user = request.GET.get('cargo')
            fk_province = request.GET.get('estado')

            if fk_user and fk_province:
                answer = {'error': 'Usuario a cargo no encontrado', 'message': 'No se encontraro el usuario a cargo en el estado especificado.'}
                message = 'Usuario a cargo encontrado en el estado especificado.'
            if fk_user:
                answer = {'error': 'Estados no encontrados para el usuario a cargo', 'message': 'No se encontraron estados asignados al usuario a cargo. Es posible que el usuario no tenga ningún estado asignado en este momento.'}
                message = 'Estados asignados encontrados para el usuario a cargo.'
            elif fk_province:
                answer = {'error': 'Usuarios a cargo no encontrados', 'message': 'No se encontraron usuarios a cargo en el estado especificado.'}
                message = 'Usuarios a cargo encontrados en el estado especificado.'
            else:
                answer = {'error': 'Usuarios a cargo no encontrados', 'message': 'No se encontraron usuarios a cargo en la base de datos.'}
                message = 'Usuarios a cargo encontrados.'
            
            queryset = self.get_queryset(fk_user=fk_user, fk_province=fk_province)
            if queryset:
                serializer = UserChargeSerializersUserProvinceSerializers(queryset, many=True)
                return Response({'items': serializer.data, 'message': message}, status=status.HTTP_200_OK)
            return Response(answer, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({
                'error': 'Error interno del servidor',
                'message': str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'items': serializer.data,
                    'message': 'Se ha asignado los estados al usuario a cargo correctamente.'
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'No se pudo asignar los estados al usuario a cargo',
                'message': 'Falta uno o más datos requeridos para realizar la asignación a los estados al usuario a cargo. Por favor, proporcione la información necesaria e intente nuevamente.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({
                'error': 'Error interno del servidor',
                'message': str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        try:
            queryset = self.get_queryset(pk=pk)
            if queryset:
                serializer = self.get_serializer(queryset, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'items': serializer.data,
                        'message': 'Se ha actualizado el estado al usuario a cargo correctamente.'
                    }, status=status.HTTP_200_OK)
                return Response({
                    'error': 'No se pudo actualizar el usuario a cargo.',
                    'message': 'Falta uno o más datos requeridos para realizar la actualización de estado al usuario a cargo. Por favor, proporcione la información necesaria e intente nuevamente.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'No se pudo encontrar el usuario a cargo para su actualización.',
                    'message': 'El usuario a cargo que intenta actualizar no se encuentra en la base de datos o está desactivado. Verifique la información proporcionada e intente nuevamente.',
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({
                'error': 'Error interno del servidor',
                'message': str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'El usuario a cargo ha sido eliminado correctamente de manera lógica.'}, status=status.HTTP_200_OK)
        return Response({
            'error': 'No se pudo eliminar lógicamente el usuario a cargo.',
            'message': 'El usuario a cargo ya ha sido eliminado anteriormente.'
        }, status=status.HTTP_404_NOT_FOUND)
