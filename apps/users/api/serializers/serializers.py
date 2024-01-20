from rest_framework import serializers

# models
from apps.users.models import User


class UserAssignmentsSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('id', 'name', 'last_name', 'image', 'username' )


class ListUsersRole(serializers.ModelSerializer):


    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')
