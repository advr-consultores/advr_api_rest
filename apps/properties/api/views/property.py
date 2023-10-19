from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

# models
from apps.territories.models import Province, Municipality, Locality
from apps.properties.models import Property
from apps.clients.models import Client

# serializers
from apps.properties.api.serializers.property import PropertySerializer, PropertiesSerializer
from apps.properties.api.serializers.serializers import PropertyWorkSerializer
# from apps.authentication.authtoken import TokenAuthentication
# from apps.permissions.auth import IsAuthenticated


class PropertyViewSet(GenericViewSet):
    serializer_class = PropertySerializer

    class Request:
        def __init__(self, property):
            self.property = property

    def get_queryset(self, pk=None, is_status=True, clients=[]):
        try:
            if len(clients):
                return self.get_serializer().Meta.model.objects.filter(client__in=clients, state=is_status)
            if pk is None:
                return self.get_serializer().Meta.model.objects.filter(state=is_status)
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        except ValueError:
            return []

    def get_property(self, key=None):
        return self.get_serializer().Meta.model.objects.filter(property_key=key, state=True).first()

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
                serializer = PropertyWorkSerializer(items, many=True)
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

        if len(properties) != 0:
            for index, property in list(enumerate(properties)):
                data = self.Request(property)
                item = self.create_mega_confirm(request=data)
                items.append(item)
            return Response({'items': items, 'message': 'Inmuebles creados'}, status=status.HTTP_207_MULTI_STATUS)
        return Response({'message': 'No hay inmubles por revisar'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        list_clients = request.GET['clientes'] if 'clientes' in request.GET.keys() else []
        is_status = request.GET['status'] if 'status' in request.GET.keys() else True
        if list_clients:
            queryset = self.get_queryset(is_status=is_status, clients=list_clients.split(','))
            message_404='No se encontraron inmuebles registrados con este cliente.'
        else:
            queryset = self.get_queryset(is_status=is_status)
            message_404='No se encontraron inmuebles registrados.'
        if queryset:
            message = 'Se encontraron ' + str(len(queryset)) + ' inmuebles registrados.'
            serializers = PropertiesSerializer(queryset, many=True)
            return Response({'items': serializers.data, 'message': message}, status=status.HTTP_200_OK)
        return Response({'message': message_404, 'error': '404 No Encontrado' }, status=status.HTTP_404_NOT_FOUND )

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
            serializer = self.get_serializer(queryset)
            return Response({'items': serializer.data,'message': 'Consulta satisfactoria.'}, status=status.HTTP_200_OK)
        return Response({'messgae': 'El inmueble fue eliminado recientemente.', 'error': '404 No Encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        queryset = self.get_queryset(pk)
        if queryset:
            serializer = self.serializer_class(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
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
