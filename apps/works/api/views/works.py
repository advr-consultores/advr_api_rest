from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.projects.models import Concept
from apps.properties.models import Property

# serializers
from apps.works.api.serializers.works import *
from apps.properties.api.serializers.property import PropertyReferenceSerializer
from apps.projects.api.serializers.concepts import ConceptSerializer


class WorkViewSet(GenericViewSet):

    serializer_class = WorkSerializer
    serializer_property = PropertyReferenceSerializer
    serializer_concept = ConceptSerializer

    def get_queryset(self, pk=None, fk_property_office=None, fk_concept=None, is_state=True):
        if fk_property_office and fk_concept: # Esta condición es solo para la función: verificar_asignacion
            return self.get_serializer().Meta.model.objects.filter(property_office=fk_property_office, concept=fk_concept, state=is_state).first()
        elif fk_property_office:
            return self.get_serializer().Meta.model.objects.filter(property_office=fk_property_office, state=is_state).all()
        elif pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=is_state).first()
        else:
            return self.get_serializer().Meta.model.objects.filter(state=is_state).all()
    
    def get_queryset_property(self, pk=None, is_state=True):
        return self.serializer_property().Meta.model.objects.filter(id=pk, state=is_state).first()
    
    def get_queryset_concept(self, pk=None, is_state=True):
        return self.serializer_concept().Meta.model.objects.filter(id=pk, state=is_state).first()

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
            works_to_verify = request.data['trabajos']
            if works_to_verify:
                items = []
                for work_to_verify in works_to_verify:
                    queryset_property_office = self.get_queryset_property(pk=work_to_verify['property_office'])
                    concepts = work_to_verify['concepts']
                    if concepts:
                        queryset_work = self.get_queryset(fk_property_office=work_to_verify['property_office'])
                        array_works = queryset_work.values_list('concept', flat=True)
                        verified_works = self.verify_and_serializar_work(array_concepts=concepts, array_works=array_works, fk_property_office=queryset_property_office.id)
                        items.append({
                            'concepts': verified_works,
                            'property_office': self.serializer_property(queryset_property_office).data
                        })
                    else:
                        items.append({
                            'concepts': [],
                            'property_office': self.serializer_property(queryset_property_office).data,
                            'error': 'Imposible verificar conceptos: solicitud vacía.',
                            'message': 'No es posible verificar los conceptos ya que la solicitud del inmueble está vacía.'
                        })
                return Response({'items': items, 'message': 'Verificación exitosa. No se encontraron problemas.'}, status=status.HTTP_200_OK)
            return Response({
                'error': 'Solicitud no válida. Verifique los parámetros enviados.',
                'message': 'No es posible verificar los trabajos ya que la solicitud de trabajo está vacía.'
            }, status=status.HTTP_400_BAD_REQUEST)   
        except ValueError as error:
            return Response({
                'error': str(error),
                'message': 'Error interno del servidor. Inténtelo de nuevo más tarde.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def verify_and_serializar_work(self, array_concepts=[], array_works=[], fk_property_office=None):
        verified_works = []
        for concept in array_concepts:
            queryset_concept = self.get_queryset_concept(pk=concept)
            message = 'A este inmueble ya se le asignó este trabajo.' if concept in array_works else 'Listo para la asignación.'
            serialize = self.serializer_class(data={
                'concept': concept,
                'property_office': fk_property_office,
            })

            verified_work = {
                'concept': self.serializer_concept(queryset_concept).data,
                'message': message,
                'confirmation': serialize.is_valid()
            }

            if not verified_work['confirmation']:
                verified_work['error'] = serialize.errors
            verified_works.append(verified_work.copy())
        return verified_works

    @action(detail=False, methods=['post'])
    def confirmar_asignacion(self, request):
        try:
            assignments = request.data['trabajos']
            works_assignments = []
            for assignment in assignments:
                property_office = Property.objects.filter(id=assignment['property_office']).first()
                for concept in assignment['concepts']:
                    work_assignment = self.serializer_class.Meta.model(
                        concept= Concept.objects.filter(id=concept).first(),
                        status= 'nuevo',
                        property_office= property_office
                    )
                    works_assignments.append(work_assignment)
            serializer_bulk = self.serializer_class.Meta.model.objects.bulk_create(works_assignments)
            serializer = ListWorksAssignmentsSerializer(serializer_bulk, many=True)
            # serializer = ListWorksAssignmentsSerializer(works_assignments, many=True)
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
