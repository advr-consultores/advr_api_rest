
from rest_framework import serializers

# models
from apps.works.models import Work

from apps.projects.api.serializers.concepts import ConceptSerializer
from apps.properties.api.serializers.works import PropertyWorkSerializer


class WorksUserListSerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    property_office = PropertyWorkSerializer(read_only=True)
    status = serializers.CharField(read_only=True, source='get_detail_state_display')
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
