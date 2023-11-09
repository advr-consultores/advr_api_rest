from rest_framework import serializers

# models
from apps.users.models import Contact


class ContactSerializers(serializers.ModelSerializer):


    class Meta:
        model = Contact
        fields = ('id', 'name', 'last_name', 'phone_one', 'phone_two', 'email', 'municipalities', )


class ContactMunicipalitiesSerializers(serializers.ModelSerializer):


    municipalities = serializers.SlugRelatedField(read_only=True, many=True, slug_field='id')
    

    class Meta:
        model= Contact
        fields = ('municipalities', )
