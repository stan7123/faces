import logging

import face_recognition
from django.utils import timezone
from django_rq import job
from rq import Retry
from PIL import Image, ImageDraw

from faces.models import FacesSubmission
from faces.storage import save_processed_image

logger = logging.getLogger('rq.worker')


@job('default', retry=Retry(10, interval=[5 * 2**n for n in range(10)]))
def process_faces_image(submission_id: int):
    try:
        submission = FacesSubmission.objects.get(id=submission_id)
    except FacesSubmission.DoesNotExist:
        logger.error(f'Could not find submission with {submission_id=} in DB.')
        return

    logger.info(f'Processing image: {submission.image.name}')

    image_np_array = face_recognition.load_image_file(submission.image.path)
    face_locations = face_recognition.face_locations(image_np_array)

    logger.info(f'Detected {len(face_locations)} faces.')

    if len(face_locations) > 0:
        marked_image = Image.fromarray(image_np_array)
        draw = ImageDraw.Draw(marked_image)
        for top, right, bottom, left in face_locations:
            draw.rectangle(((left, top), (right, bottom)), outline=255, fill=None, width=2)
        marked_image_path = save_processed_image(marked_image)

        logger.info(f'Saved processed image to: {marked_image_path}')

        submission.faces_count = len(face_locations)
        submission.processed_at = timezone.now()
        submission.processed_image = str(marked_image_path)
        submission.save()
    else:
        logger.info('Skipping image marking.')

        submission.faces_count = len(face_locations)
        submission.processed_at = timezone.now()
        submission.save()
