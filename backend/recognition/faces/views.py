from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from faces.serializers import FacesSubmissionSerializer


class SubmitImageView(CreateAPIView):
    serializer_class = FacesSubmissionSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        response_data = {
            'message': 'Request accepted. Starting image processing.',
            'feed_url': 'TODO',
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
