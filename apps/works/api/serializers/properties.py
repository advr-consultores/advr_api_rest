
from rest_framework import serializers

# models
from apps.works.models import Work
from apps.projects.api.serializers.concepts import ConceptSerializer


class WorkPropertySerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    assigned_user = serializers.SlugRelatedField(read_only=True, slug_field='name')
    area_user = serializers.SlugRelatedField(read_only=True, slug_field='name')
    status = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model= Work
        exclude = ('property_office', )
