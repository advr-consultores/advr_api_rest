
from rest_framework import serializers

from apps.projects.models import Concept, Project


class ConceptsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = ('id', 'name')

class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('name', )

class ConceptSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Concept
        fields = ('id', 'name', 'project')

class ConceptCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = '__all__'