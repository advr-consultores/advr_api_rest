from rest_framework import serializers

# models
from apps.users.models import User

# serializers
from apps.groups.api.serializers.groups import GroupsSerializer, Group
from apps.users.api.serializers.user_charge import UserChargeProvincesObjSerializers


class UserPOSTSerializers(serializers.ModelSerializer):

    groups = serializers.PrimaryKeyRelatedField(required=False, queryset=Group.objects.all(), many=True)
    fathers_last_name = serializers.CharField(required=False, max_length=100, allow_null=False)
    mothers_last_name = serializers.CharField(required=False, max_length=100, allow_null=False)

    class Meta:
        model = User
        exclude = ('last_name', )


    def create(self, validated_data):  # encripta las contraseñas asignadas
        groups = validated_data.get('groups', [])
        last_name = "F'{} M'{}".format(validated_data.get('fathers_last_name', ''), validated_data.get('mothers_last_name', ''),)
        if 'fathers_last_name' in validated_data.keys():
            del validated_data['fathers_last_name']
        if 'mothers_last_name' in validated_data.keys():
            del validated_data['mothers_last_name']
        if 'groups' in validated_data.keys():
            del validated_data['groups']
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.last_name = last_name
        user.save()
        user.groups.set(groups)
        return user

    
class UserUpdateSerializers(serializers.ModelSerializer):

    name = serializers.CharField(required=True, max_length=100, allow_null=False)
    fathers_last_name = serializers.CharField(required=True, max_length=100, allow_null=False)
    mothers_last_name = serializers.CharField(required=True, max_length=100, allow_null=False)
    

    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'fathers_last_name', 'mothers_last_name', )


    def update(self, instance, validated_data):
        last_name = "F'{} M'{}".format(validated_data.get('fathers_last_name', ''), validated_data.get('mothers_last_name', ''),)
        if 'fathers_last_name' in validated_data.keys():
            # last_name = "F'{}".format(validated_data.get('fathers_last_name', ''))
            del validated_data['fathers_last_name']
        if 'mothers_last_name' in validated_data.keys():
            del validated_data['mothers_last_name']
        user = super().update(instance, validated_data)
        user.last_name = last_name
        user.save()
        return user

    
class UserPasswordSerializers(serializers.ModelSerializer):

    old_password = serializers.CharField(required=True, max_length=128)
    new_password = serializers.CharField(required=True, max_length=128)

    
    class Meta:
        model = User
        fields = ('old_password', 'new_password', )

    def update(self, instance, validated_data):  # encripta las contraseñas asignadas
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['new_password'])
        update_user.save()
        return update_user

class UserSerializers(serializers.ModelSerializer):

    groups = GroupsSerializer(many=True, read_only=True)
    last_login = serializers.DateTimeField(format='%d-%m-%Y')
    fathers_last_name = serializers.ReadOnlyField()
    mothers_last_name = serializers.ReadOnlyField()


    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'last_name', )


class UsersSerializers(serializers.ModelSerializer):

    provinces_charge = UserChargeProvincesObjSerializers(many=False, read_only=True)
    groups = GroupsSerializer(many=True, read_only=True)
    last_login = serializers.DateTimeField(format='%d-%m-%Y')
    fathers_last_name = serializers.ReadOnlyField()
    mothers_last_name = serializers.ReadOnlyField()

    def to_representation(self, instance):
        user = super().to_representation(instance)
        if not user['provinces_charge']:
            user['provinces_charge'] = []
        else:
            user['provinces_charge'] = user['provinces_charge']['provinces']
        return user


    class Meta:
        model = User
        exclude = ('password', 'user_permissions')


class UserImagenPartialSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('image', )


class UserStaffSerializers(serializers.ModelSerializer):

    is_staff = serializers.BooleanField(required=True)


    class Meta:
        model = User
        fields = ('is_staff', )


class UserGroupsSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('groups', )


class UserGetUsernameSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('username', 'is_active', )
