from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

# serializers
from apps.users.api.serializers.contact import ContactSerializers


class ContactViewSet(GenericViewSet):

    serializer_class = ContactSerializers

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True).all()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializers = self.get_serializer(queryset, many=True)
            return Response({'items': serializers.data, 'message': 'Se encontraron los contactos exitosamente'}, status=status.HTTP_200_OK)
        return Response({
            'error': 'No se encontraron contactos',
            'message': 'No hay registros de contactos en la base de datos en este momento.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        serializers = self.get_serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({
                'items': serializers.data,
                'message': 'El contacto se creó exitosamente.'
            },status=status.HTTP_200_OK)
        return Response({
            'error': 'No se puede crear el contacto',
            'message': 'Por favor, revise los datos proporcionados para el contacto y asegúrese de que sean válidos.',
            'errors': serializers.errors
        }, status=status.HTTP_400_BAD_REQUEST)