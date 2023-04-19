from rest_framework import serializers

from apps.resources.models import Resource, Comment, UploadFileForm

class ResourceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource.historial.model
        fields = '__all__'
