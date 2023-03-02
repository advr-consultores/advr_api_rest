
from rest_framework import serializers

# models
from apps.works.models import Comment

class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'