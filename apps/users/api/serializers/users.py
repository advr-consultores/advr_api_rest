from rest_framework import serializers

# models
from apps.users.models import User

# serializers
from apps.groups.api.serializers.groups import GroupsSerializer


class UserPOSTPUTSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):  # encripta las contraseñas asignadas
        groups = validated_data['groups']
        del validated_data['groups']
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):  # encripta las contraseñas asignadas
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user


class UserSerializers(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'user_permissions')

class UsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'user_permissions')


class UserImagenPartialSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'email', 'username', 'is_superuser', 'is_active', 'is_staff')

class UserPermissionsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('is_active', 'is_staff', )

class UserGroupsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('groups', )



class UserGetUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', )
