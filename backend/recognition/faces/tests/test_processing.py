from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.test import override_settings, TestCase
from PIL import Image

from faces.models import FacesSubmission
from faces.tasks import process_faces_image


def get_temp_face_image(image_relative_path: str) -> NamedTemporaryFile:
    image = Image.open(Path(__file__).parent / image_relative_path)
    tmp_file = NamedTemporaryFile(dir=settings.MEDIA_ROOT, suffix=f'.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


@override_settings(
    STORAGE_ROOT=TemporaryDirectory(prefix='statictest').name,
)
class FacesRecognitionTaskTestCase(TestCase):
    @patch('faces.tasks.publish_detection')
    def test_successful_one_face_recognition(self, mocked_publish_detection):
        face_image = get_temp_face_image('images/one_face_image.jpeg')
        submission = FacesSubmission.objects.create(image=face_image.name)

        process_faces_image(submission.id)

        submission.refresh_from_db()
        self.assertEqual(submission.faces_count, 1)
        self.assertIsNotNone(submission.processed_at)
        self.assertTrue(submission.processed_image.name.endswith('.jpg'))
        mocked_publish_detection.assert_called_once_with(submission)

    @patch('faces.tasks.publish_detection')
    def test_successful_multiple_face_recognition(self, mocked_publish_detection):
        face_image = get_temp_face_image('images/two_faces_image.jpg')
        submission = FacesSubmission.objects.create(image=face_image.name)

        process_faces_image(submission.id)

        submission.refresh_from_db()
        self.assertEqual(submission.faces_count, 2)
        self.assertIsNotNone(submission.processed_at)
        self.assertTrue(submission.processed_image.name.endswith('.jpg'))
        mocked_publish_detection.assert_called_once_with(submission)

    @patch('faces.tasks.publish_detection')
    def test_no_face_recognition(self, mocked_publish_detection):
        face_image = get_temp_face_image('images/no_face_image.jpeg')
        submission = FacesSubmission.objects.create(image=face_image.name)

        process_faces_image(submission.id)

        submission.refresh_from_db()
        self.assertEqual(submission.faces_count, 0)
        self.assertIsNotNone(submission.processed_at)
        self.assertTrue(submission.processed_image.name == '')
        mocked_publish_detection.assert_not_called()
