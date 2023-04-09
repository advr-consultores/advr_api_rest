from rest_framework import serializers
from django.contrib.auth.models import Group, Permission


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
