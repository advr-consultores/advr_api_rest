from rest_framework import serializers

# model
from apps.users.models import Charge
from apps.territories.api.serializers.territories import ProvinceSerializer

#
from apps.users.api.serializers.serializers import UserAssignmentsSerializers


class UserChargeSerializers(serializers.ModelSerializer):


    class Meta:
        model= Charge
        fields = ('__all__')


class UserChargeProvincesSerializers(serializers.ModelSerializer):

    charge = UserAssignmentsSerializers(read_only=True)
    provinces = ProvinceSerializer(read_only=True, many=True)


    class Meta:
        model= Charge
        fields = ('id', 'charge', 'provinces', )


class UserChargeProvincesObjSerializers(serializers.ModelSerializer):

    provinces = ProvinceSerializer(read_only=True, many=True)


    class Meta:
        model= Charge
        fields = ('id', 'provinces', )


class ChargeSerializers(serializers.ModelSerializer):

    charge = serializers.IntegerField(required=True)


    class Meta:
        model= Charge
        fields = ('charge', )


class UserChargeProvinceIdSerializers(serializers.ModelSerializer):

    provinces = serializers.SlugRelatedField(read_only=True, many=True, slug_field='id')
    

    class Meta:
        model= Charge
        fields = ('provinces', )
 