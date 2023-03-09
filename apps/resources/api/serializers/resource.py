from rest_framework import serializers

# models
from apps.resources.models import Resource

# serializers
from apps.resources.api.serializers.petition import PetitionsSerializers


class ResourceSerializers(serializers.ModelSerializer):
    
    total_amout = serializers.ReadOnlyField()

    class Meta:
        model = Resource
        exclude = ( 'state', )


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

    class Meta:
        model = Resource
        exclude = ('state',)
