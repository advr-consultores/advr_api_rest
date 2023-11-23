from rest_framework import serializers

from apps.works.models import Work

from apps.resources.api.serializers.petition import PetitionWorksSerializers


class ResourceWorkSerializers(serializers.ModelSerializer):

    petition = PetitionWorksSerializers(read_only=True)


    class Meta:
        model = Work
        fields = ('petition', )

    # def to_representation(self, value):
    #     return PetitionWorksSerializers(value.petition).data["resource"][0]
