from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.projects.models import Concept
from apps.properties.models import Property

# serializers
from apps.works.api.serializers.works import *


class WorkViewSet(GenericViewSet):

    serializer_class = WorkSerializer

    def get_queryset(self, pk=None, fk_property_office=None, fk_concept=None, is_state=True):
        if fk_property_office and fk_concept: # Esta condición es solo para la función: verificar_asignacion
            return self.get_serializer().Meta.model.objects.filter(property_office=fk_property_office, concept=fk_concept, state=is_state).first()
        elif fk_property_office:
            return self.get_serializer().Meta.model.objects.filter(property_office=fk_property_office, state=is_state).all()
        elif pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=is_state).first()
        else:
            return self.get_serializer().Meta.model.objects.filter(state=is_state).all()

    def list(self, request):
        fk_property_office = request.GET['inmueble'] if 'inmueble' in request.GET.keys() else None
        is_state = request.GET['state'] if 'state' in request.GET.keys() else True
        queryset = self.get_queryset(fk_property_office=fk_property_office, is_state=is_state)
        if queryset:
            serializer = ListWorksSerializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No hay trabajos.'}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            assignments = request.data['assignments']
            items = []
            for assignment in assignments:
                works = []
                assignment['property_office'] = Property.objects.filter(id=assignment['property_office']).values('id', 'name', 'property_key').first()
                for work in assignment['works']:
                    queryset = self.get_queryset(fk_concept=work['concept'], fk_property_office=assignment['property_office']['id'])
                    if queryset:
                        work['message']='A este inmueble ya se le asignó este trabajo.'
                    else:
                        work['message']='Listo para la asignación.'
                    serialize = self.serializer_class(data={
                        'concept': work['concept'],
                        'status': work['status'],
                        'property_office': assignment['property_office']['id'],
                    })
                    work['concept'] = Concept.objects.filter(id=work['concept']).values('id', 'name', 'project__name').first()
                    work['status'] = 'nuevo'

                    if serialize.is_valid():
                        work['confirmation'] = True
                        work['status_code'] = status.HTTP_200_OK
                    else:
                        work['confirmation'] = False
                        work['status_code'] = status.HTTP_400_BAD_REQUEST
                        work['error'] = serialize.errors
                    works.append(work)
                items.append({'works': works, 'property_office': assignment['property_office']})
            return Response({'items': items, 'message': 'Asignaciones verificadas.'}, status=status.HTTP_207_MULTI_STATUS)     
        except ValueError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def confirmar_asignacion(self, request):
        try:
            assignments = request.data['assignments']
            works_assignments = []
            for assignment in assignments:
                property_office = Property.objects.filter(id=assignment['property_office']).first()
                for work in assignment['works']:
                    if work['confirmation']:
                        work_assignment = self.serializer_class.Meta.model(
                            concept= Concept.objects.filter(id=work['concept']).first(),
                            status= 'nuevo',
                            property_office= property_office
                        )
                        works_assignments.append(work_assignment)
            serializer_bulk = self.serializer_class.Meta.model.objects.bulk_create(works_assignments)
            serializer = ListWorksAssignmentsSerializer(serializer_bulk, many=True)
            return Response({'items': serializer.data, 'message': 'Trabajos asignados.'}, status=status.HTTP_200_OK)
        except ValueError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

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
