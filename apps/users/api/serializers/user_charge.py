from rest_framework import serializers

# model
from apps.users.models import Charge

# serializer
from apps.territories.api.serializers.territories import ProvinceSerializer


class UserChargeSerializers(serializers.ModelSerializer):


    class Meta:
        model= Charge
        fields = ('__all__')


class UserChargeSerializersUserProvinceSerializers(serializers.ModelSerializer):

    charge = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = ProvinceSerializer(read_only=True, many=True)


    class Meta:
        model= Charge
        fields = ('__all__')