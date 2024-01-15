from rest_framework import serializers

# models
from apps.properties.models import Property

# serializers
from apps.territories.api.serializers.territories import ProvinceUserChargeSerializer, MunicipalityContactSerializer


class PropertySerializer(serializers.ModelSerializer):

    address = serializers.CharField(allow_null=False, allow_blank=False)


    class Meta:
        model = Property
        fields = (
            'id',
            'name',
            'property_key',
            'sirh',
            'address',
            'province',
            'municipality',
            'locality',
            'client',
            'created_date',
            'modified_date',
            'deleted_date',
        )


class PropertiesSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = ProvinceUserChargeSerializer(read_only=True)
    municipality = MunicipalityContactSerializer(read_only=True)


    class Meta:
        model = Property
        exclude = ('state', )


class PropertyReferenceSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = ProvinceUserChargeSerializer(read_only=True)
    municipality = MunicipalityContactSerializer(read_only=True)


    class Meta:
        model = Property
        fields = ('id', 'name', 'property_key', 'sirh', 'client', 'province', 'municipality', 'address', )


class PropertyWorksSerializer(serializers.ModelSerializer):

    works = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Property
        fields = ('works', )
