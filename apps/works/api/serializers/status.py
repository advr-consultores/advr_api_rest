from rest_framework import serializers

# models
from apps.works.models import Status


class WorkStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model= Status
        fields= ('id', 'name')