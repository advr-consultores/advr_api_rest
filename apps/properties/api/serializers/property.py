from rest_framework import serializers

# models
from apps.properties.models import Property


class PropertySerializer(serializers.ModelSerializer):

    address = serializers.CharField(allow_null=False, allow_blank=False)


    class Meta:
        model = Property
        fields = (
            'id',
            'name',
            'property_key',
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
    province = serializers.SlugRelatedField(read_only=True, slug_field='name')
    municipality = serializers.SlugRelatedField(read_only=True, slug_field='name')
    locality = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model = Property
        exclude = ('state', )


class PropertyReferenceSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model = Property
        fields = ('name', 'property_key', 'client', 'province', )


class PropertyWorksSerializer(serializers.ModelSerializer):

    works = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Property
        fields = ('works', )
