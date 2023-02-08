from rest_framework import serializers

# models
from apps.properties.models import Property

# serializers
from apps.clients.api.serializers.clients import ClientSerializer
from apps.territories.api.serializers.territories import ProvinceSerializer, MunicipalitySerializer


class PropertyWorkSerializer(serializers.ModelSerializer):

    client = ClientSerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    municipality = MunicipalitySerializer(read_only=True)
    locality = MunicipalitySerializer(read_only=True)

    class Meta:
        model = Property
        fields = (
            'id',
            'name',
            'property_key',
            'client',
            'province',
            'municipality',
            'locality'
        )
