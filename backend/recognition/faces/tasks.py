import logging

from django_rq import job

logger = logging.getLogger('rq.worker')


@job
def process_faces_image(submission_id: int):
    logger.info(f'Processing faces image {submission_id}')

