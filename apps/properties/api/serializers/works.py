from rest_framework import serializers

# models
from apps.properties.models import Property
from apps.works.api.serializers.serializers import WorksPropertySerializer


class PropertiesWorkSerializer(serializers.ModelSerializer):

    works = WorksPropertySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ('works', )


class PropertyWorkSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = serializers.SlugRelatedField(read_only=True, slug_field='name')
    municipality = serializers.SlugRelatedField(read_only=True, slug_field='name')
    locality = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Property
        fields = ('name', 'property_key', 'client', 'province', 'municipality', 'locality', )
