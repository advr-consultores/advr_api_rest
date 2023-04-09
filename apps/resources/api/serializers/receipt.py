from rest_framework import serializers

# models
from apps.resources.models import UploadFileForm

class ProofPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadFileForm
        fields = '__all__'

class ProofResourcePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadFileForm
        fields = ('id', 'file',)
