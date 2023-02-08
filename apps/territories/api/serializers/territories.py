
from rest_framework import serializers

from apps.territories.models import Locality, Province, Municipality


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
        fields = ('id', 'name', 'locality')
