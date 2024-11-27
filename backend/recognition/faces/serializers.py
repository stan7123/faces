from rest_framework import serializers

from faces.models import FacesSubmission


class FacesSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacesSubmission
        fields = ('image',)
