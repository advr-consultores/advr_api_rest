from rest_framework import serializers

# serializers
from apps.users.api.serializers.serializers import UserAssignmentsSerializers
from apps.projects.api.serializers.concepts import ConceptSerializer
from apps.properties.api.serializers.serializers import PropertyRetriveSerializer
from apps.works.api.serializers.serializers import FileSerializer
from apps.properties.api.serializers.works import PropertyWorkSerializer
# models
from apps.works.models import Work


class WorkSerializer(serializers.ModelSerializer):


    class Meta:
        model = Work
        fields = '__all__'


class ListWorksSerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    property_office = PropertyWorkSerializer(read_only=True)
    status = serializers.CharField(read_only=True, source='get_status_display')
    comments = serializers.StringRelatedField(many=True)


    class Meta:
        model = Work
        fields = (
            'id',
            'concept',
            'status',
            'property_office',
            'created_date',
            'modified_date',
            'deleted_date',
            'comments',
        )

class ListWorksAssignmentsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model= Work
        fields = ('concept', 'property_office',)


class WorkRetrieveSerializer(serializers.ModelSerializer):

    concept = ConceptSerializer(read_only=True)
    property_office = PropertyRetriveSerializer(read_only=True)
    status = serializers.CharField(read_only=True, source='get_detail_state_display')
    files = FileSerializer(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True)


    class Meta:
        model = Work
        fields = '__all__'
