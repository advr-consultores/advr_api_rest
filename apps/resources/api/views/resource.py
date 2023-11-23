import json

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.db.utils import IntegrityError

# serializers
from apps.resources.api.serializers.resource import *
from apps.resources.api.serializers.work import ResourceWorkSerializers
from apps.resources.api.serializers.petition import PetitionConfirmSerializer, PetitionSerializers
from apps.users.api.serializers.user_charge import UserChargeProvinceIdSerializers
from apps.users.api.serializers.contact import ContactMunicipalitiesSerializers
from apps.properties.api.serializers.property import PropertyWorksSerializer

# view
from apps.resources.api.views.petition import PetitionViewSet

# Create your views here.


class ResourceViewSet(GenericViewSet):

    serializer_class = ResourceSerializers
    serializer_paid_class = ResourcePaidSerializer
    serializer_invoiced_class = ResourceInvoicedSerializer
    serializer_detail_state_class = ResourceDetailStateSerializer
    serializer_petition_class = PetitionSerializers

    def get_queryset(self, pk=None, list_pk=[], validate=False, payment_mode=''):
        if pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        if not payment_mode:
            return self.get_serializer().Meta.model.objects.filter(id__in=list(list_pk), state=True, validate=validate)
        if len(list_pk):
            return self.get_serializer().Meta.model.objects.filter(id__in=list(list_pk), state=True, validate=validate, payment_mode=payment_mode)
        return self.get_serializer().Meta.model.objects.filter(state=True, validate=validate, payment_mode=payment_mode)
    
    def get_queryset_paid(self, validate=False, paid=False, payment_mode=''):
        return self.get_serializer().Meta.model.objects.filter(state=True, validate=validate, paid=paid, payment_mode=payment_mode).all()
    
    def get_queryset_charge(self, fk_user_charge=None):
       return UserChargeProvinceIdSerializers().Meta.model.objects.filter(charge=fk_user_charge).first()
    
    def get_queryset_contact(self, pk=None):
        return ContactMunicipalitiesSerializers().Meta.model.objects.filter(id=pk).first()
    
    def get_queryset_property(self, list_fk_provinces=[], list_fk_municipalities=[]):
        try:
            if len(list_fk_provinces):
                queryset_property = PropertyWorksSerializer().Meta.model.objects.filter(province__in=list_fk_provinces).all().exclude(works=None)
            if len(list_fk_municipalities):
                queryset_property = PropertyWorksSerializer().Meta.model.objects.filter(municipality__in=list_fk_municipalities).all().exclude(works=None)
            if queryset_property.exists():
                list_property_works = PropertyWorksSerializer(queryset_property, many=True)
                trabajos = []
                for list_property in list_property_works.data:
                    trabajos.extend(list_property['works'])
                return trabajos
            return []
        except UnboundLocalError:
            return []

    def create(self, request):
        resource_create = self.create_resource(resource=request.data)
        if resource_create['success']:
            return Response({'items': resource_create['items'], 'message': resource_create['message']}, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': resource_create['error'], 'message': resource_create['message'], 'errors': resource_create['errors']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            resource_update = self.create_resource(queryset, resource=request.data)
            if resource_update['success']:
                return Response({'items': resource_update['items'], 'message': resource_update['message']}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': resource_update['error'], 'message': resource_update['message'], 'errors': resource_update['errors']
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['patch'])
    def paid(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.validate:
                serializer = self.serializer_paid_class(queryset, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Pago exitoso. La petición está marcada como pagada.', 'items': serializer.data}, status=status.HTTP_200_OK)
                return Response({
                    'error': 'Error en el pago',
                    'message': 'Lo sentimos, ha habido un problema con el procesamiento del pago. Inténtalo de nuevo.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Validación requerida', 'message': 'No se puede activar el atributo sin validar primero.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({
            'error': 'Petición de pago de derechos no encontrada',
            'message': 'Lo sentimos, no hemos encontrado ninguna petición con el ID proporcionado. Por favor, asegúrate de que el ID sea correcto e inténtalo nuevamente. Si el problema persiste, contacta con nuestro equipo de soporte para obtener asistencia.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['patch'])
    def invoiced(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            if queryset.validate and queryset.paid:
                serializer = self.serializer_invoiced_class(queryset, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Factura aprobada. La solicitud se ha registrado como facturada.', 'items': serializer.data}, status=status.HTTP_200_OK)
                return Response({
                    'error': 'Error en la factura',
                    'message': 'Lo sentimos, ha habido un problema con el procesamiento de la factura. Inténtalo de nuevo.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'No se puede marcar como facturado hasta validar y pagar',
                            'message': 'La marcación como facturado no es posible hasta que se valide y realice el pago correspondiente.'
                        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({
            'error': 'Petición de pago de derechos no encontrada',
            'message': 'Lo sentimos, no hemos encontrado ninguna petición con el ID proporcionado. Por favor, asegúrate de que el ID sea correcto e inténtalo nuevamente. Si el problema persiste, contacta con nuestro equipo de soporte para obtener asistencia.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['patch'])
    def state(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_detail_state_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'La petición ha sido actualizada con éxito a [Nuevo Estado]. ¡Listo para seguir adelante!', 'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({
                'error': 'Error al actualizar el estado de la petición.',
                'message': 'Lo sentimos, ha ocurrido un error al intentar actualizar el estado de la petición. Por favor, revisa la información proporcionada e inténtalo de nuevo. ',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'Petición de pago de derechos no encontrada',
            'message': 'Lo sentimos, no hemos encontrado ninguna petición con el ID proporcionado. Por favor, asegúrate de que el ID sea correcto e inténtalo nuevamente. Si el problema persiste, contacta con nuestro equipo de soporte para obtener asistencia.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def multiple(self, request):
        try:
            if 'solicitudes_recursos' in request.data:
                resources = []
                for resource in request.data['solicitudes_recursos']:
                    resources.append(self.create_resource(resource=resource))
                return Response({'items': resources, 'message': 'Todas las solicitudes se han procesado exitosamente.'}, status=status.HTTP_200_OK)
            return Response({
                'error': 'No se pueden verificar las peticiones sin datos válidos',
                'message': 'Por favor, proporcione una lista de trabajos con información válida para poder procesar su solicitud correctamente.'
            },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        

    def create_resource(self, queryset=None, resource={}):
        serializer_resource = ResourceCheckStructSerializer(data=resource)
        if serializer_resource.is_valid():
            response_petitions = self.confirmar_peticiones(serializer_resource.data['works'])
            if response_petitions['success']:
                obj_resource = {
                    'payment_mode': resource['modalidad_pago'],
                    'transfer_type': '' if resource['tipo_transferencia'] is None else resource['tipo_transferencia'],
                    'transfer_data': json.dumps(resource['datos_tipo_transferencia']) if len(resource['datos_tipo_transferencia']) else '{}' ,
                    'bank': resource['banco'],
                    'beneficiary': resource['beneficiario'],
                    'concept': resource['concept'],
                    'petitions': response_petitions['petitions'],
                    'validate': False if resource['validate'] is None else resource['validate'],
                    'detail_state': resource['detalle_status']
                }
                serializer = ResourcePOSTSerializer(queryset, data=obj_resource) if queryset else ResourcePOSTSerializer(data=obj_resource)
                if serializer.is_valid():
                    serializer.save()
                    return {
                        'success': True,
                        'message': 'La solicitud de recursos se ha creado exitosamente.',
                        'items': serializer.data
                    }
                return {
                    'success': False,
                    'message': 'Por favor, asegúrese de proporcionar todos los datos requeridos en el formato correcto para poder crear la solicitud de recurso.',
                    'error': 'No se pudo crear la solicitud de recurso',
                    'errors': serializer.errors
                }
            return {
                'success': False,
                'error': 'La solicitud de recursos no pudo ser creada debido a un error en las peticiones.',
                'message': 'Por favor, revise las peticiones enviadas y asegúrese de que estén correctamente formateadas y contengan datos válidos.',
                'errors': response_petitions['errors']
            }
        return {
            'success': False,
            'error': 'La solicitud de recursos no se pudo crear debido a la falta de datos.',
            'message': 'Por favor, proporcione los datos necesarios para crear los recursos y vuelva a intentarlo.',
            'errors': serializer_resource.errors
        }

    def confirmar_peticiones(self, request):
        try:
            petitions = []
            errors_petitions = []
            for obj_petition in request:
                serializer = PetitionConfirmSerializer(data=obj_petition)
                if serializer.is_valid():
                    petition = PetitionViewSet().verify_petition(obj_petition=obj_petition)
                    if petition['confirm']:
                        queryset_petition = self.serializer_petition_class.Meta.model.objects.filter(work=obj_petition['work']).first()
                        if queryset_petition:
                            serializer_update_petition = self.serializer_petition_class(queryset_petition, data=obj_petition)
                            if serializer_update_petition.is_valid():
                                serializer_update_petition.save()
                                petitions.append(serializer_update_petition.data['id'])
                            else:
                                errors_petitions.append(serializer_update_petition.errors)
                        else: # Crear la peticion
                            serializer_petition = self.serializer_petition_class(data=obj_petition)
                            if serializer_petition.is_valid():
                                serializer_petition.save()
                                petitions.append(serializer_petition.data['id'])
                            else:
                                errors_petitions.append(serializer_petition.errors)
                    else:
                        errors_petitions.append({'error': petition['error'], 'message': petition['message']})
                else:
                    errors_petitions.append(serializer.errors)
            if errors_petitions:
                return ({
                    'error': 'No se pudieron crear las peticiones debido a un error interno',
                    'message': 'Por favor, inténtelo de nuevo más tarde o póngase en contacto con el soporte técnico para obtener ayuda.',
                    'errors': errors_petitions, 'success': False
                })
            return({'petitions': petitions, 'success': True})
        except Exception as error:
            return {'message': str(error), 'error': type(error).__name__, 'errors': 'Fue interrumpida la creación de las peticiones', 'success': False}

    def list(self, request):
        type_pay = request.GET.get('modalidad_pago')
        is_validate = request.GET.get('validado')
        is_paid = request.GET.get('pagado')
        queryset = self.get_queryset_paid(payment_mode=type_pay, validate=is_validate, paid=is_paid)
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
            if 'payment_mode' in request_data:
                payment_mode = request_data['payment_mode'][0]
            else:
                payment_mode = ''
            if 'validate' in request_data:
                validate = request_data['validate'][0] if len(request_data['validate'][0]) else False
            else:
                validate = False
            if 'usuario_cargo' in request_data:
                queryset_province = self.get_queryset_charge(fk_user_charge=request_data['usuario_cargo'][0])
                if queryset_province:
                    serializer_province = UserChargeProvinceIdSerializers(queryset_province)
                    list_provinces = serializer_province.data
                    list_works = self.get_queryset_property(list_fk_provinces=list_provinces['provinces'])
                    if list_works:
                        queryset_work = ResourceWorkSerializers.Meta.model.objects.filter(id__in=list_works).exclude(petition=None)
                    else:
                        return Response({
                        'error': 'No se encontraron solicitudes de recursos porque no se han creado trabajos.',
                        'message': 'Por favor, cree trabajos para poder gestionar las solicitudes de recursos.'
                    }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'error': 'No se encontraron solicitudes de recursos debido a que no se han asignado estados.',
                        'message': 'Por favor, asigne estados a los recursos para poder crear y gestionar solicitudes de recursos.'
                    }, status=status.HTTP_404_NOT_FOUND)
            if 'contact' in request_data:
                queryset_municipalities = self.get_queryset_contact(pk=request_data['contact'][0])
                if queryset_municipalities:
                    serializers_municipalities = ContactMunicipalitiesSerializers(queryset_municipalities)
                    list_municipalities = serializers_municipalities.data
                    list_works = self.get_queryset_property(list_fk_municipalities=list_municipalities['municipalities'])
                    if list_works:
                        queryset_work = ResourceWorkSerializers.Meta.model.objects.filter(id__in=list_works).exclude(petition=None)
                    else:
                        return Response({
                        'error': 'No se encontraron solicitudes de recursos porque no se han creado trabajos.',
                        'message': 'Por favor, cree trabajos para poder gestionar las solicitudes de recursos.'
                    }, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        'error': 'No se encontraron solicitudes de recursos debido a que no se han asignado municipios.',
                        'message': 'Por favor, asigne municipios a los recursos para poder crear y gestionar solicitudes de recursos.'
                    }, status=status.HTTP_404_NOT_FOUND)
            if queryset_work:
                serializer_work = ResourceWorkSerializers(queryset_work, many=True)
                petitions = []
                for work in serializer_work.data:
                    if len(work['petition']['resource']):
                        petitions.append(work['petition']['resource'][0])
                queryset = self.get_queryset(list_pk=petitions, validate=validate, payment_mode=payment_mode)
                if queryset:
                    serializer = self.get_serializer(queryset, many=True)
                    return Response({'items': serializer.data})
                return Response({
                    'error': 'No se encontraron solicitudes de recursos relacionadas con los filtros proporcionados',
                    'message': 'No hay solicitudes de recursos que coincidan con los filtros de "payment_mode", "validate" o "usuario_cargo" proporcionados.'
                }, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'error': 'No se encontraron solicitudes de recursos',
                'message': 'No hay registros de solicitudes de recursos en la base de datos en este momento'
            }, status=status.HTTP_404_NOT_FOUND)
        except UnboundLocalError:
            return Response({
                "message": {"usuario_cargo": "Estos campo son requerido.", },
                "error": 'No se puede hace la solicitud debido a que no se encontro en el parámetro los argumentos: "solicitado" o "gestor"'
            }, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk=None):
    #     queryset = self.get_queryset(pk)
    #     if queryset:
    #         if queryset.request:
    #             serializer=ResourceValidationPartialSerializer(queryset, data=request.data)
    #         else:
    #             # if request.data['validate'] or request.data['validate'] is False:
    #             #     return Response({'messagae': 'No se puede validar o rechazar este recurso, hasta que  haya aceptado por la parte coordinadora'}, status=status.HTTP_400_BAD_REQUEST)
    #             serializer = ResourcePartialSerializer(queryset, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'items': serializer.data, 'message': 'La actualización ha tenido éxito.'}, status=status.HTTP_200_OK)
    #         return Response({'error': serializer.errors, 'message': 'La actualización no ha tenido éxito.'}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.delete()
            return Response({'message': 'Solicitud de recursos eliminada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el recurso.'}, status=status.HTTP_404_NOT_FOUND)
