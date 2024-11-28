import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.shortcuts import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from faces.models import FacesSubmission


def get_temp_image(extension: str = 'jpg') -> NamedTemporaryFile:
    image = Image.new('RGB', (100, 100))
    tmp_file = NamedTemporaryFile(suffix=f'.{extension}')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


def get_temp_corrupted_image() -> NamedTemporaryFile:
    tmp_file = NamedTemporaryFile(suffix='.jpg')
    tmp_file.write(b'qweqweqwe')  # Writing text instead of image data
    tmp_file.seek(0)
    return tmp_file


class SubmitImageViewTestSuite(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint_url = reverse('faces-image-submit')

    def test_successful_image_submission(self):
        self.assertEqual(FacesSubmission.objects.count(), 0)
        temp_image = get_temp_image()

        response = self.client.post(self.endpoint_url, {'image': temp_image}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        expected_response = {
            'message': 'Request accepted. Starting image processing.',
            'feed_url': 'TODO',
        }
        self.assertEqual(response.data, expected_response)
        self.assertEqual(FacesSubmission.objects.count(), 1)
        submission = FacesSubmission.objects.get()
        self.assertTrue(submission.processed_image.name == '')
        self.assertIsNone(submission.processed_at)
        self.assertIsNone(submission.faces_count)
        self.assertTrue(submission.image.name.endswith(Path(temp_image.name).suffix))

    def test_no_image_send_returns_bad_data(self):
        self.assertEqual(FacesSubmission.objects.count(), 0)

        response = self.client.post(self.endpoint_url, {}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = {
            'image': ['No file was submitted.']
        }
        self.assertEqual(json.loads(response.content), expected_response)
        self.assertEqual(FacesSubmission.objects.count(), 0)

    def test_if_returns_bad_data_if_send_file_has_no_image_content(self):
        self.assertEqual(FacesSubmission.objects.count(), 0)
        temp_broken_image = get_temp_corrupted_image()

        response = self.client.post(self.endpoint_url, {'image': temp_broken_image}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = {
            'image': ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
        }
        self.assertEqual(json.loads(response.content), expected_response)
        self.assertEqual(FacesSubmission.objects.count(), 0)

    def test_if_returns_bad_data_if_send_file_has_unsupported_extension(self):
        self.assertEqual(FacesSubmission.objects.count(), 0)
        temp_unsupported_image = get_temp_image('tiff')

        response = self.client.post(self.endpoint_url, {'image': temp_unsupported_image}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = {
            'image': ['File extension “tiff” is not allowed. Allowed extensions are: gif, jpg, jpeg, png.']
        }
        self.assertEqual(json.loads(response.content), expected_response)
        self.assertEqual(FacesSubmission.objects.count(), 0)
