from rest_framework import serializers

# models
from apps.works.models import Work
from apps.properties.models import Property


class PropertyWorkSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = serializers.SlugRelatedField(read_only=True, slug_field='name')
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

    assigned_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    area_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    property_office = PropertyWorkSerializer(read_only=True)
    concept = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Work
        fields = (
            'id',
            'concept',
            'property_office',
            'assigned_user',
            'area_user',
        )
