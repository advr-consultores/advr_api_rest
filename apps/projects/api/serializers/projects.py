
from rest_framework import serializers
from apps.projects.models import Project

from apps.projects.api.serializers.concepts import ConceptsSerializer


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', )


class ProjectSerializer(serializers.ModelSerializer):

    concepts = ConceptsSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'concepts', )
