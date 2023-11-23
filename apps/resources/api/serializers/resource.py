from rest_framework import serializers

# models
from apps.resources.models import Resource

# serializers
from apps.resources.api.serializers.petition import PetitionsSerializers
from apps.beneficiary.api.serializers.beneficiary import BeneficiaryRetriveSerializer


class ResourceSerializers(serializers.ModelSerializer):
    
    total_amout = serializers.ReadOnlyField()
    payment_mode = serializers.CharField(allow_null=False)
    bank = serializers.CharField(allow_null=False)
    beneficiary = serializers.SlugRelatedField(read_only=True, slug_field='name')
    detail_state = serializers.CharField(source='get_detail_state_display')


    class Meta:
        model = Resource
        exclude = ( 'state', )

class ResourcePOSTSerializer(serializers.ModelSerializer):


    class Meta:
        model = Resource
        fields = '__all__'


class ResourcePartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ('request',)

class ResourceValidationPartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ('validate',)


class ResourceRetriveSerializers(serializers.ModelSerializer):

    total_amout = serializers.ReadOnlyField()
    petitions = PetitionsSerializers(many=True, read_only=True)
    beneficiary = BeneficiaryRetriveSerializer(read_only=True)


    class Meta:
        model = Resource
        exclude = ('state',)


class ResourceCheckStructSerializer(serializers.ModelSerializer):

    works = serializers.ListField(required=True, allow_empty=False)


    class Meta:
        model = Resource
        exclude = ('petitions', )

class ResourcePaidSerializer(serializers.ModelSerializer):

    paid = serializers.BooleanField(allow_null=False)
    detail_state = serializers.CharField(allow_null=False)


    class Meta:
        model = Resource
        fields = ('paid', 'detail_state', )


class ResourceInvoicedSerializer(serializers.ModelSerializer):

    invoiced = serializers.BooleanField(allow_null=False)


    class Meta:
        model = Resource
        fields = ('invoiced', )


class ResourceDetailStateSerializer(serializers.ModelSerializer):

    detail_state = serializers.CharField(allow_null=False)


    class Meta:
        model = Resource
        fields = ('detail_state', )
