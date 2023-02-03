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
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):  # encripta las contraseñas asignadas
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user


class UserSerializers(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password', 'user_permissions')


class UserPartialSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'email', 'username')


class UserGetUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', )
