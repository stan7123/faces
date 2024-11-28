import uuid
from pathlib import Path

from django.core.validators import FileExtensionValidator
from django.db import models


def upload_path(instance, filename):
    """Generating unique file names to avoid collisions"""

    unique_name = str(uuid.uuid4())
    extension = Path(filename).suffix

    return f'faces/{unique_name[:2]}/{unique_name[2:4]}/{unique_name}{extension}'


class FacesSubmission(models.Model):
    image = models.ImageField(
        'Original image',
        upload_to=upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['gif', 'jpg', 'jpeg', 'png'])]
    )
    processed_image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True)
