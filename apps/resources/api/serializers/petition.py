from rest_framework import serializers

# models
from apps.resources.models import Petition, Resource


# serializer
from apps.resources.api.serializers.works import WorkResourceSerializers


class PetitionSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = Petition
        fields = '__all__'


class ResourceValidationPartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ('id', 'validate', )


class PetitionInResourceSerializer(serializers.ModelSerializer):

    resource = ResourceValidationPartialSerializer(many=True, read_only=True)


    class Meta:
        model = Petition
        fields = ('resource', 'work', 'amount', )


class PetitionsIDSerializers(serializers.ModelSerializer):


    class Meta:
        model = Petition
        fields = ('id', )


class PetitionsSerializers(serializers.ModelSerializer):

    work = WorkResourceSerializers(read_only=True)

    
    class Meta:
        model = Petition
        exclude = ('state', 'deleted_date', )


class PetitionWorksSerializers(serializers.ModelSerializer):
    
    resource = serializers.SlugRelatedField(read_only=True, many=True, slug_field='id')
    
    
    class Meta:
        model = Petition
        fields = ('resource', )


class PetitionConfirmSerializer(serializers.ModelSerializer):

    work = serializers.IntegerField(required=True)


    class Meta:
        model = Petition
        fields = ('work', 'amount', )


class PetitionsCheckStruct(serializers.ModelSerializer):

    works = serializers.ListField(required=True, allow_empty=False)


    class Meta:
        model = Petition
        fields = ('works', )
