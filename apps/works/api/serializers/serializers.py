from rest_framework import serializers

# serializers
from apps.users.api.serializers.serializers import UserAssignmentsSerializers
from apps.properties.api.serializers.property import PropertyReferenceSerializer
from apps.projects.api.serializers.concepts import ConceptSerializer
from apps.works.api.serializers.status import WorkStatusSerializer

# models
from apps.works.models import Work, UploadFileForm


class WorkPropertySerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    assigned_user = UserAssignmentsSerializers(read_only=True)
    area_user = UserAssignmentsSerializers(read_only=True)
    property_office = serializers.SlugRelatedField(read_only=True, slug_field='name')
    status = WorkStatusSerializer(read_only=True)
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model= Work
        fields= (
            'id',
            'status',
            'created_date',
            'modified_date',
            'deleted_date',
            'property_office',
            'concept',
            'assigned_user',
            'area_user',
            'comments',
        )

class WorksPropertySerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    assigned_user = serializers.SlugRelatedField(read_only=True, slug_field='name')
    area_user = serializers.SlugRelatedField(read_only=True, slug_field='name')
    property_office = PropertyReferenceSerializer(read_only=True)
    status = serializers.SlugRelatedField(read_only=True, slug_field='name')
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model= Work
        fields= (
            'id',
            'status',
            'created_date',
            'modified_date',
            'deleted_date',
            'property_office',
            'concept',
            'assigned_user',
            'area_user',
            'comments',
            'state',
        )


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadFileForm
        fields = ("id", "title", "file", "work")