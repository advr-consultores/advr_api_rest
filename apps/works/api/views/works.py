from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.projects.models import Concept
from apps.properties.models import Property
from apps.works.models import Status
from apps.users.models import User

# serializers
from apps.works.api.serializers.works import *


class WorkViewSet(GenericViewSet):
    serializer_class = WorkSerializer

    class Request:
        def __init__(self, work):
            self.data = work

    def get_queryset(self, pk=None, pk_property_office=None, pk_concept=None):
        if pk_property_office is not None and pk_concept is not None:
            return self.get_serializer().Meta.model.objects.filter(
                property_office=pk_property_office,
                concept=pk_concept,
                state=True
            ).first()
        elif pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = ListWorksSerializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No hay trabajos.'}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = WorkRetrieveSerializer(queryset)
            return Response({'items': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'No existe el trabajo.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def proyecto(self, request, pk=None):
        queryset = self.get_serializer().Meta.model.objects.filter(proyect=pk, state=True)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No tiene trabajos asignados a este proyecto.', 'error': 'None'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def concepto(self, request, pk=None):
        queryset = self.get_serializer().Meta.model.objects.filter(concept=pk, state=True)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No tiene trabajos asignados a este concepto.', 'error': 'None'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def verificar_asignacion(self, request):
        assignments = request.data['assignments']
        items = []
        for assignment in assignments:
            works = []
            for work in assignment['works']:
                queryset = self.get_queryset(pk_concept=work['concept'], pk_property_office=assignment['property_office'])
                if queryset:
                    work['message']='A este inmueble ya se le asignó este trabajo.'
                else:
                    work['message']='Listo para la asignación.'
                serialize = self.serializer_class(data={
                    'concept': work['concept'],
                    'status': work['status'],
                    'assigned_user': work['assigned_user'],
                    'property_office': assignment['property_office'],
                    'area_user': assignment['area_user']
                })
                concept = Concept.objects.filter(id=work['concept']).first()
                status_work = Status.objects.filter(id = work['status']).first()
                property = Property.objects.filter(id=assignment['property_office']).first()
                assigned_user = User.objects.filter(id=work['assigned_user']).first()
                area_user = User.objects.filter(id=assignment['area_user']).first()

                work['concept'] = { 'id': concept.id, 'name': concept.name, 'project':concept.project.name }
                work['status']={ 'id': status_work.id, 'name': status_work.name }
                property_office={ 'id': property.id, 'name': property.name, 'key': property.property_key }
                work['assigned_user']={ 'id': assigned_user.id, 'name': assigned_user.name }
                areauser={ 'id': area_user.id, 'name': area_user.name }

                if serialize.is_valid():
                    work['confirmation'] = True
                    work['status_code'] = status.HTTP_200_OK
                else:
                    work['confirmation'] = False
                    work['status_code'] = status.HTTP_400_BAD_REQUEST
                    work['error'] = serialize.errors
                works.append(work)
            items.append({'works': works, 'property_office': property_office, 'area_user': areauser})
        return Response({'items': items, 'message': 'Asignaciones verificadas.'}, status=status.HTTP_207_MULTI_STATUS)

    @action(detail=False, methods=['post'])
    def confirmar_asignacion(self, request):
        assignments = request.data['assignments']
        items = []
        for assignment in assignments:
            works = []
            for work in assignment['works']:
                if work['confirmation']:
                    data = self.Request({
                        'concept': work['concept'],
                        'status': work['status'],
                        'property_office': assignment['property_office'],
                        'assigned_user': work['assigned_user'],
                        'area_user': assignment['area_user']
                    })
                    serialize = self.create(request=data)
                    if serialize.status_code != 400:
                        work['status_code'] = serialize.status_code
                    else:
                        work['error'] = serialize.data['error']
                        work['status_code'] = serialize.status_code
                    works.append(work)
                else:
                    works.append(work)
                    work['status_code'] = None
            items.append({'works': works, 'property_office': assignment['property_office'], 'area_user': assignment['area_user'],})
        return Response({'items': items, 'message': 'Trabajos asignados.'}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({ 'items': serializer.data }, status=status.HTTP_202_ACCEPTED)
            return Response({ 'error': serializer.errors }, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'error': 'El trabajo dejo de existir' }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Trabajo eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'El trabajo ya fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)
