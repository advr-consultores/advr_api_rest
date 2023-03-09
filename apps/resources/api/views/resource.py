from datetime import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.db.utils import IntegrityError
import json

# serializers
from apps.resources.api.serializers.resource import ResourceSerializers, ResourceRetriveSerializers, ResourcePartialSerializer, ResourceValidationPartialSerializer
from apps.resources.api.serializers.work import ResourceWorkSerializers

from apps.resources.api.views.petition import PetitionViewSet

from apps.resources.models import Petition, Resource

# Create your views here.


class ResourceViewSet(GenericViewSet):

    serializer_class = ResourceSerializers

    def get_queryset(self, pk=None, list_pk=[], request=None, validate = None, type_pay=None):
        if pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        if request:
            return self.get_serializer().Meta.model.objects.filter(state=True, id__in=list(list_pk), request=request)
        if type_pay and list_pk:
            return self.get_serializer().Meta.model.objects.filter(state=True, id__in=list(list_pk), request=True, type_pay=type_pay)
        if type_pay:
            return self.get_serializer().Meta.model.objects.filter(state=True, request=True, validate=validate, type_pay=type_pay)
        if list_pk:
            return self.get_serializer().Meta.model.objects.filter(id__in=list(list_pk), state=True)
        return self.get_serializer().Meta.model.objects.filter(state=True)
    

    def create(self, request):
        data = PetitionViewSet.confirmar_peticiones(self, request=request)
        if(400 <= data.status_code <= 404):
            return data
        petitions = [petition.work.id for petition in data.data['items']]
        list_of_tuple_petitions =  Petition.objects.filter(work__in = petitions, state=True).values_list('id')
        list_petition = [int(tuple[0]) for tuple in list_of_tuple_petitions]
        request_resource = {
            'petitions': list_petition,
            'type_pay': request.data['type_pay'],
            'concept': request.data['concept'],
        }
        serializer = self.serializer_class(data=request_resource)
        if serializer.is_valid():
            serializer.save()
            return Response({'items': serializer.data, 'message': 'La solicitud ha tenido éxito.'}, status=status.HTTP_201_CREATED)
        Petition.objects.filter(id__in =list_petition).delete()
        return Response({'error': serializer.errors, 'message': 'Solicitud de recurso no creada.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def mutiple_create(self, request):
        try:
            data = PetitionViewSet.confirmar_peticiones(self, request=request)
            if(400 <= data.status_code <= 404):
                return data
            list_request_resource = []
            for petition in data.data['items']:
                request_resource = Resource.objects.create(
                    bank_data=request.data['bank_data'],
                    type_pay=request.data['type_pay'],
                    bank=request.data['bank'],
                    concept=request.data['concept'],
                    method_pay=request.data['method_pay'],
                    beneficiary=request.data['beneficiary']
                )
                request_resource.petitions.add(petition)
                list_request_resource.append(request_resource)
            return Response( {'message': 'Solicitudes de recursos creada.'}, status=status.HTTP_200_OK)
        except ValueError as error:
            petitions = [petition.id for petition in data.data['items']]
            Petition.objects.filter(id__in =petitions).delete()
            return Response({"error": str(error) }, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as error:
            petitions = [petition.id for petition in data.data['items']]
            Petition.objects.filter(id__in =petitions).delete()
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as error:
            petitions = [petition.id for petition in data.data['items']]
            Petition.objects.filter(id__in =petitions).delete()
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        requestBool = request.GET.get('request')
        typePay = request.GET.get('type_pay')
        validateBool = request.GET.get('validate')
        queryset = self.get_queryset(request=requestBool, type_pay=typePay, validate=validateBool)

        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'items': serializer.data, 'message': 'La solicitud ha tenido éxito.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No tienes solicitudes de recursos pendientes.'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = ResourceRetriveSerializers(queryset)
            return Response({'items': serializer.data, 'message': 'La solicitud ha tenido éxito.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def trabajo(self, request):
        try:
            request_data = dict(request.GET)
            if 'tipo_pago' in request_data:
                type_pay=request_data['tipo_pago'][0]
            else:
                type_pay=None
            if 'request' in request_data:
                request =request_data['request'][0]
            else:
                request=None
            if 'solicitado' in request_data:
                assigned_user = request_data['solicitado'][0]
                queryset_work= ResourceWorkSerializers.Meta.model.objects.filter(assigned_user=assigned_user).exclude(petition=None)
            else:
                area_user = request_data['gestor'][0]
                queryset_work= ResourceWorkSerializers.Meta.model.objects.filter(area_user=area_user).exclude(petition=None)
            if queryset_work:
                serilalizer_work = ResourceWorkSerializers(queryset_work, many=True)
                queryset = self.get_queryset(list_pk=serilalizer_work.data, request=request, type_pay=type_pay)
                if queryset:
                    serilalizerr = self.get_serializer(queryset, many=True)
                    return Response({'items': serilalizerr.data})
                return Response({'message': 'No se encontraron solicitudes de recursos relacionados con este usuario.'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'No se encontraron trabajos relacionados con este usuario.'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({
                "message": {"solicitado o gestor": "Estos campo son requerido.", },
                "error": '"No se puede hace la solicitud debido a que no se encontro en el parámetro los argumentos: "solicitado" o "gestor"'
            }, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data, 'message': 'La actualización ha tenido éxito.'}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors, 'message': 'La actualización no ha tenido éxito.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.request:
                serializer=ResourceValidationPartialSerializer(queryset, data=request.data)
            else:
                # if request.data['validate'] or request.data['validate'] is False:
                #     return Response({'messagae': 'No se puede validar o rechazar este recurso, hasta que  haya aceptado por la parte coordinadora'}, status=status.HTTP_400_BAD_REQUEST)
                serializer = ResourcePartialSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'items': serializer.data, 'message': 'La actualización ha tenido éxito.'}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors, 'message': 'La actualización no ha tenido éxito.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            Petition.objects.filter(id__in =self.get_serializer(queryset).data['petitions']).delete()
            queryset.delete()
            return Response({'message': 'Solicitud de recursos eliminada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)
