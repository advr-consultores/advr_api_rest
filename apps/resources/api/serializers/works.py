from rest_framework import serializers

# models
from apps.works.models import Work
from apps.properties.models import Property

# serializers
from apps.territories.api.serializers.territories import ProvinceUserChargeSerializer


class PropertyWorkSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = ProvinceUserChargeSerializer(read_only=True)
    municipality = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model = Property
        fields = (
            'id',
            'name',
            'property_key',
            'client',
            'province',
            'municipality',
        )


class WorkResourceSerializers(serializers.ModelSerializer):

    property_office = PropertyWorkSerializer(read_only=True)
    concept = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model = Work
        fields = (
            'id',
            'concept',
            'property_office',
        )
