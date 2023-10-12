from rest_framework import serializers

# models
from apps.beneficiary.models import Beneficiary


class BeneficiarySerializer(serializers.ModelSerializer):

    bank = serializers.CharField(allow_null = False)


    class Meta:
        model = Beneficiary
        fields = ('__all__')