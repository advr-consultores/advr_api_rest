from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# from django.db.utils import IntegrityError
# serializers
from apps.resources.api.serializers.petition import PetitionSerializers, PetitionInResourceSerializer, PetitionsCheckStruct

# from apps.resources.models import Petition
from apps.works.models import Work


class PetitionViewSet(GenericViewSet):

    serializer_class = PetitionSerializers

    def get_queryset(self, pk=None, fk_work=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(work=fk_work).first()
        return self.get_serializer().Meta.model.objects.filter(state=True, id=pk).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data, 'message': 'La petición ha tenido éxito.'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors, 'message': 'Petición no creada.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verificar_peticiones(self, request):
        try:
            serializer_petitions = PetitionsCheckStruct(data=request.data)
            if serializer_petitions.is_valid():
                list_request = []
                for petition in serializer_petitions.data['works']:
                    list_request.append(self.verify_petition(obj_petition=petition))
                return Response({'items': list_request, 'message': 'Las peticiones fueron verificadas.'}, status=status.HTTP_207_MULTI_STATUS)
            return Response({
                'error': 'No se pueden verificar las peticiones sin datos válidos',
                'message': 'Por favor, proporcione una lista de trabajos con información válida para poder procesar su solicitud correctamente.',
                'errors': serializer_petitions.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error), 'error': type(error).__name__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def verify_petition(self, obj_petition={'work': 0}):
        queryset_work = Work.objects.filter(id=obj_petition['work']).first()
        is_petition_in_resource = False
        if queryset_work:
            queryset = PetitionInResourceSerializer().Meta.model.objects.filter(work=obj_petition['work']).first()
            if queryset:
                serializer_in_resource = PetitionInResourceSerializer(queryset)
                # print(serializer_in_resource.data['resource'])
                for resource in serializer_in_resource.data['resource']:
                    if resource['validate']:
                        is_petition_in_resource = True
                        break
                if is_petition_in_resource:
                    return {
                        'confirm': False,
                        'work': obj_petition['work'],
                        'error': 'Este trabajo ya ha sido enviado como solicitud de recursos',
                        'message': 'El trabajo que está intentando verificar no puede ser enviado dos veces como solicitud de recursos.'
                    }
                return {'confirm': True, 'work': obj_petition['work'], 'amount': serializer_in_resource.data['amount'] }
            return {'confirm': True, 'work': obj_petition['work'], 'amount': 0.0 }
        return {
            'confirm': False,
            'work': obj_petition['work'],
            'error': 'No se encontró el trabajo para verificar',
            'message': 'El trabajo que intenta verificar no se encuentra en la base de datos. Por favor, verifique el ID del trabajo proporcionado e intente nuevamente.'
        }

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data, 'message': 'La actualización ha tenido éxito.'}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors, 'message': 'La actualización no ha tenido éxito.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se encontro la petición.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.delete()
            return Response({'message': 'Solicitud de peticion eliminada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro la petición.'}, status=status.HTTP_404_NOT_FOUND)
