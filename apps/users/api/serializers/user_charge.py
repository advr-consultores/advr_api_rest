from rest_framework import serializers

# model
from apps.users.models import Charge


class UserChargeSerializers(serializers.ModelSerializer):


    class Meta:
        model= Charge
        fields = ('__all__')


class UserChargeProvincesSerializers(serializers.ModelSerializer):

    charge = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = serializers.PrimaryKeyRelatedField(read_only=True, many=True)


    class Meta:
        model= Charge
        fields = ('id', 'charge', 'province', )


class ChargeSerializers(serializers.ModelSerializer):

    charge = serializers.IntegerField(required=True)


    class Meta:
        model= Charge
        fields = ('charge', )


class UserChargeProvinceIdSerializers(serializers.ModelSerializer):

    province = serializers.SlugRelatedField(read_only=True, many=True, slug_field='id')
    

    class Meta:
        model= Charge
        fields = ('province', )