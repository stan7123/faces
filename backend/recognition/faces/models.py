from django.core.validators import FileExtensionValidator
from django.db import models

from faces.storage import get_upload_path


class FacesSubmission(models.Model):
    image = models.ImageField(
        'Original image',
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['gif', 'jpg', 'jpeg', 'png'])]
    )
    processed_image = models.ImageField(null=True)
    faces_count = models.PositiveIntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True)
