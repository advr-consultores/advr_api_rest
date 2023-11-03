from rest_framework import serializers

# models
from apps.territories.models import Locality, Province, Municipality
from apps.users.models import Charge


class MunicipalitySerializer(serializers.ModelSerializer):


    class Meta:
        model = Municipality
        fields = ('id', 'name', )


class ProvinceMunicipalitiesSerializer(serializers.ModelSerializer):

    municipalities = MunicipalitySerializer(read_only=True, many=True)


    class Meta:
        model = Province
        fields = ('id', 'name', 'abbreviation', 'municipalities', )


class ProvincesSerializer(serializers.ModelSerializer):


    class Meta:
        model = Province
        fields = ('id', 'name', 'abbreviation', )


class ProvinceSerializer(serializers.ModelSerializer):


    class Meta:
        model = Province
        fields = ('id', 'name', )


class LocalitySerializer(serializers.ModelSerializer):


    class Meta:
        model = Locality
        fields = ('id', 'name', )


class MunicipalityLocalitySerializer(serializers.ModelSerializer):

    locality = LocalitySerializer(read_only=True, many=True)


    class Meta:
        model = Municipality
        fields = ('id', 'name', 'locality', )


class ChargeUserChargeSerializer(serializers.ModelSerializer): # No se puede poner en el serializador de user_charge.py por la redundancia

    charge = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model= Charge
        fields = ('charge', )


class ProvinceUserChargeSerializer(serializers.ModelSerializer):

    users_charge = ChargeUserChargeSerializer(many=True, read_only=True)


    class Meta:
        model = Province
        fields = ('name', 'users_charge', )
