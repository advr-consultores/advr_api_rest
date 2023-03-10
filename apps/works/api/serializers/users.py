
from rest_framework import serializers

# models
from apps.works.models import Work

from apps.projects.api.serializers.concepts import ConceptSerializer
from apps.properties.api.serializers.works import PropertySerializer


class WorksUserListSerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    property_office = PropertySerializer(read_only=True)
    status = serializers.SlugRelatedField(read_only=True, slug_field='name')
    comments = serializers.StringRelatedField(many=True)
    area_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    assigned_user = serializers.SlugRelatedField(read_only=True, slug_field='username')


    class Meta:
        model= Work
        fields= (
            'id',
            'status',
            'created_date',
            'modified_date',
            'deleted_date',
            'property_office',
            'concept',
            'area_user',
            'assigned_user',
            'comments',
        )