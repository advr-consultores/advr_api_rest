
from rest_framework import serializers

# models
from apps.works.models import Work

class ListWorkSerializer(serializers.ModelSerializer):
    
    concept = serializers.SlugRelatedField(read_only=True, slug_field='name')
    property_office = serializers.SlugRelatedField(read_only=True, slug_field='name')
    assigned_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    area_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model= Work
        fields= ('id', 'concept', 'property_office', 'assigned_user', 'area_user', )
