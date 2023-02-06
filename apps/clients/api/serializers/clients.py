from rest_framework import serializers

# models
from apps.clients.models import Client


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ('state', )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', )
