from rest_framework import serializers

from apps.works.models import Work

class WorkHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Work.historial.model
        fields = '__all__'