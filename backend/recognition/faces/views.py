from rest_framework.generics import CreateAPIView

from faces.serializers import FacesSubmissionSerializer


class SubmitImageView(CreateAPIView):
    serializer_class = FacesSubmissionSerializer
