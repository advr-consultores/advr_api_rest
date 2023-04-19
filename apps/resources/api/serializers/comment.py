from rest_framework import serializers

# models
from apps.resources.models import Comment

# serializer
from apps.users.api.serializers.serializers import UserAssignmentsSerializers


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):

    changed_by = UserAssignmentsSerializers(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'changed_by', 'comment')
