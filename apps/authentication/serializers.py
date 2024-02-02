from rest_framework import serializers

# models
from apps.users.models import User

# serializers
from apps.groups.api.serializers.groups import GroupsSerializer


class UserLoginSerializer(serializers.ModelSerializer):

    groups = GroupsSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password', 'user_permissions')


class LoginCredentialSerializer(serializers.ModelSerializer):

    email = serializers.CharField(allow_blank=False, allow_null=False)
    password = serializers.CharField(allow_blank=False, allow_null=False)


    class Meta:
        model=User
        fields = ('email', 'password', )
