from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

# models
from apps.territories.models import Province, Municipality, Locality
from apps.properties.models import Property
from apps.clients.models import Client

# serializers
from apps.properties.api.serializers.property import PropertySerializer, PropertiesSerializer, PropertyReferenceSerializer
from apps.properties.api.serializers.serializers import PropertyRetriveSerializer
# from apps.authentication.authtoken import TokenAuthentication
# from apps.permissions.auth import IsAuthenticated


class PropertyViewSet(GenericViewSet):

    serializer_class = PropertySerializer

    class Request:
        def __init__(self, property):
            self.property = property

    def get_queryset(self, pk=None, state=True, fk_client=None,fk_province=None, fk_municipality=None):
        if pk:
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        if fk_client and fk_province and fk_municipality:
            return self.get_serializer().Meta.model.objects.filter(state=state, client=fk_client, province=fk_province, municipality=fk_municipality).all()
        if fk_province and fk_municipality:
            return self.get_serializer().Meta.model.objects.filter(state=state, province=fk_province, municipality=fk_municipality).all()
        if fk_client and fk_province:
            return self.get_serializer().Meta.model.objects.filter(state=state, client=fk_client, province=fk_province).all()
        if fk_client:
            return self.get_serializer().Meta.model.objects.filter(state=state, client=fk_client).all()
        if fk_province:
            return self.get_serializer().Meta.model.objects.filter(state=state, province=fk_province).all()
        return self.get_serializer().Meta.model.objects.filter(state=state).all()

    def get_property(self, property_key=''):
        return self.get_serializer().Meta.model.objects.filter(property_key=property_key, state=True).first()

    def get_queryset_province(self, province_name):
        provinces = Province.objects.filter(active=1).all().order_by('id',)
        for province in provinces:
            if self.normalize(province.name) in province_name:
                return province
        return None

    def get_queryset_municipality(self, municipality_name, province_pk):
        municipalities = Municipality.objects.filter(active=1, province=province_pk.id)
        for municipality in municipalities:
            if self.normalize(municipality.name) in municipality_name:
                return municipality
        return None

    def get_queryset_locality(self, locality_name, municipality_pk):
        localities = Locality.objects.filter(active=1, municipality=municipality_pk.id)
        for locality in localities:
            if self.normalize(locality.name) in locality_name:
                return locality
        return None

    def normalize(self, territory):
        territory_name = ''
        # method splits a string into a list.
        s = territory.split()
        for val in s:
            # t:he first character of the string to a capital (uppercase) letter
            territory_name += val.lower() + ' '

        s = territory_name[:-1]
        s = s.replace('cd.', 'ciudad')

        replacements = (
            ('á', 'a'),
            ('é', 'e'),
            ('í', 'i'),
            ('ó', 'o'),
            ('ú', 'u'),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        if s == 'estado de mexico':
            s = 'mexico'
        return s

    def get_territory(self, request):
        province_name = self.normalize(request['data']['province'])
        request['data']['province'] = self.get_queryset_province(province_name)

        if request['data']['province']:

            municipality_name = self.normalize(request['data']['municipality'])
            request['data']['municipality'] = self.get_queryset_municipality(
                municipality_name, request['data']['province'])
            if request['data']['municipality']:

                locality_name = self.normalize(request['data']['locality'])
                request['data']['locality'] = self.get_queryset_locality(
                    locality_name, request['data']['municipality'])

                if request['data']['locality']:
                    return {'property': request['data']}

                request['data']['locality'] = None

                return {'property': request['data']}

            request['data']['municipality'] = None
            request['data']['locality'] = None
            return {'property': request['data']}

        request['data']['province'] = None
        request['data']['municipality'] = None
        request['data']['locality'] = None
        return {'property': request['data']}

    @action(detail=False, methods=['post'])
    def verificacion(self, request):
        items = []
        try:
            properties = request.data['properties']
            if len(properties):
                for property in properties:
                    data = self.Request(property)
                    data = self.get_territory(request={'data': data.property})
                    property = Property(
                        name= data['property']['name'],
                        property_key= data['property']['property_key'],
                        sirh = data['property']['sirh'],
                        address= data['property']['address'],
                        province= data['property']['province'],
                        municipality= data['property']['municipality'],
                        locality= data['property']['locality'],
                        client= Client.objects.filter(id=data['property']['client'], state=True).first()
                    )
                    items.append(property)
                serializer = PropertyRetriveSerializer(items, many=True)
                return Response({'items': serializer.data, 'message': 'Inmuebles verificados.'}, status=status.HTTP_200_OK)
            return Response({'errors': 'No hay inmubles por revisar'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as error:
            return Response({
                'message': {'properties': str(error), },
                'error': 'No se puede hace la solicitud debido a que no se encontro en el parámetro el argumento: "properties"'
            }, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as error:
            return Response({
                'message': {
                    'properties': str(error),
                },
                'error': 'No se puede hace la solicitud debido a que no se encontro en el parámetro el argumento: "properties"'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def confirmacion(self, request):
        items = []
        properties = request.data['properties']

        if len(properties):
            for index, property in list(enumerate(properties)):
                data = self.Request(property)
                item = self.create_mega_confirm(request=data)
                items.append(item)
            return Response({'items': items, 'message': 'Inmuebles creados'}, status=status.HTTP_207_MULTI_STATUS)
        return Response({'message': 'No hay inmubles por revisar'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if 'clave' in request.GET.keys():
            queryset = self.get_property(property_key=request.GET['clave'])
            if queryset:
                serializer = PropertyReferenceSerializer(queryset)
                return Response({'items': serializer.data,'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
            return Response({
                'messgae': 'La búsqueda del inmueble con la ID especificada no ha tenido éxito. Verifica que la ID sea correcta y asegúrate de que estás utilizando el formato adecuado.',
                'error': 'Inmueble no encontrado con la ID proporcionada.'
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            fk_client = request.GET['clientes'] if 'clientes' in request.GET.keys() else None
            fk_province = request.GET['estado'] if 'estado' in request.GET.keys() else None
            fk_municipality = request.GET['municipio'] if 'municipio' in request.GET.keys() else None
            state = request.GET['state'] if 'state' in request.GET.keys() else True
            queryset = self.get_queryset(state=state, fk_client=fk_client, fk_municipality=fk_municipality, fk_province=fk_province)
            if queryset:
                message = 'Se encontraron ' + str(len(queryset)) + ' inmuebles registrados.'
                serializers = PropertiesSerializer(queryset, many=True)
                return Response({'items': serializers.data, 'message': message}, status=status.HTTP_200_OK)
            return Response({
                'message': 'La consulta no ha arrojado resultados positivos. No hemos encontrado inmuebles que cumplan con los criterios específicos que has proporcionado.',
                'error': 'La consulta no ha sido satisfactoria. No se encontraron inmuebles con el filtro proporcionado.'
            }, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'items': serializer.data,
                'message': 'La solicitud ha tenido éxito y ha llevado a la creación de un inmueble.'
            },status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def create_mega_confirm(self, request):
        serializer = self.serializer_class(data=request.property)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return {'error': serializer.errors, 'status': 400}

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = PropertyRetriveSerializer(queryset)
            return Response({'items': serializer.data,'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({
            'messgae': 'La búsqueda del inmueble con la ID especificada no ha tenido éxito. Verifica que la ID sea correcta y asegúrate de que estás utilizando el formato adecuado.',
            'error': 'Inmueble no encontrado con la ID proporcionada.'
        }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializer = PropertyRetriveSerializer(queryset)
                return Response({
                    'items': serializer.data,
                    'message': 'El inmueble fue actualizado correctamente.'
                }, status=status.HTTP_202_ACCEPTED)
            return Response({'error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'El inmueble fue eliminado recientemente.', 'error': '404 No Encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            queryset.state = False
            queryset.save()
            return Response({'message': 'Inmueble eliminado correctamente'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'El inmueble dejo ya fue eliminado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)
