from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

# models
from apps.users.models import Charge

# serializers
from apps.properties.api.serializers.property import PropertiesSerializer

class PropertyUserChargeViewSet(GenericViewSet):

    serializer_class = PropertiesSerializer

    def get_queryset_provinces(self, fk_user_charge=None):
        return Charge.objects.filter(charge=fk_user_charge).first()
    
    def get_queryset(self, list_fk_privinve=[], fk_client=None, fk_province=None, fk_municipality=None):
        if fk_client and fk_province and fk_municipality:
            return self.get_serializer().Meta.model.objects.filter(state=True, client=fk_client, province=fk_province, municipality=fk_municipality).all()
        if fk_province and fk_municipality:
            return self.get_serializer().Meta.model.objects.filter(state=True, province=fk_province, municipality=fk_municipality).all()
        if fk_client and fk_province:
            return self.get_serializer().Meta.model.objects.filter(state=True, client=fk_client, province=fk_province).all()
        if fk_province:
            return self.get_serializer().Meta.model.objects.filter(state=True, province=fk_province).all()
        if fk_client and len(list_fk_privinve):
            return self.get_serializer().Meta.model.objects.filter(state=True, client=fk_client, province__in=list_fk_privinve).all()
        if len(list_fk_privinve):
            return self.get_serializer().Meta.model.objects.filter(state=True, province__in=list_fk_privinve)

    def retrieve(self, request, pk=None):
        client = request.GET.get('cliente') if 'cliente' in request.GET.keys() else None
        province = request.GET.get('estado') if 'estado' in request.GET.keys() else None
        municipality = request.GET.get('municipio') if 'municipio' in request.GET.keys() else None
        queryset_provinces = self.get_queryset_provinces(fk_user_charge=pk)
        if queryset_provinces:
            list_properties = list(queryset_provinces.provinces.values_list('id', flat=True).all())
            if province:
                if int(province) not in list_properties:
                    return Response({
                        'error': 'No tienes autorización para listar inmuebles en este estado.',
                        'message': 'No tienes los permisos necesarios para listar inmuebles en este estado. Si crees que esto es un error o necesitas acceso adicional, por favor, ponte en contacto con el administrador del sistema o el equipo de soporte para obtener la asistencia necesaria.'
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    queryset = self.get_queryset(fk_client=client, fk_province=province, fk_municipality=municipality)  
            else:
                queryset = self.get_queryset(list_fk_privinve=list_properties, fk_client=client, fk_province=province, fk_municipality=municipality)
            if queryset:
                queryset = queryset.order_by('-modified_date')
                serializer = self.get_serializer(queryset, many=True)
                return Response({'items': serializer.data, 'message': 'Consulta exitosa. Se encontraron inmuebles bajo la responsabilidad del usuario.'}, status=status.HTTP_200_OK)
            return Response({
                'error': 'No se encontraron inmuebles en los estados a cargo del usuario.',
            'message': 'La búsqueda de inmuebles en los estados bajo la responsabilidad del usuario no ha arrojado resultados. Verifica los estados especificados y asegurarte de que la información sea correcta.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'error':'No se ha encontrado al usuario en el campo especificado.',
            'message': 'La búsqueda del usuario en el campo especificado no arrojó resultados positivos. Por favor, verifica la información proporcionada y asegúrate de que el campo sea correcto.'},
            status=status.HTTP_404_NOT_FOUND)