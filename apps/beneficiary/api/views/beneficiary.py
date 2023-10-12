from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

# serializer
from apps.beneficiary.api.serializers.beneficiary import BeneficiarySerializer


class BeneficiaryViewSet(GenericViewSet):
    serializer_class = BeneficiarySerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True).order_by('name', )
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Se encontraron {} beneficiarios.'.format(len(queryset))}, status=status.HTTP_200_OK)
        return Response({
            'error': 'Beneficiarios no encontrados',
            'message': 'No se encontraron beneficiarios en la base de datos o no hay beneficiarios que cumplan con los criterios de búsqueda especificados.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'items': serializer.data,
                'message': 'El beneficiario con el nombre {} ha sido creado exitosamente.'.format(serializer.data['name'])
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'No se pudo crear el beneficiario',
            'errors': serializer.errors,
            'message': 'La solicitud para crear el beneficiario no puede ser procesada en este momento. Verifique los datos proporcionados y asegúrese de que estén en el formato correcto. Si el problema persiste, por favor, contacte al soporte técnico para obtener asistencia.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Actualización del beneficiario completada exitosamente.',
                    'items': serializer.data,
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Error en la actualización del beneficiario',
                'message': 'La actualización del beneficiario no pudo ser completada debido a un problema en los datos proporcionados. Por favor, verifique los datos e inténtelo nuevamente. Si el problema persiste, contacte al soporte técnico para obtener asistencia.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'error': 'Beneficiario no encontrado',
                'message': 'El beneficiario que intenta actualizar no se encuentra en la base de datos o no existe. Por favor, verifique el identificador del beneficiario o los datos proporcionados e intente nuevamente.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Beneficiario eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'El beneficiario ya fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)
