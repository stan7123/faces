import uuid
from pathlib import Path

from django.conf import settings
from PIL import Image


def get_upload_path(_, filename):
    """Generating unique file names to avoid collisions"""

    unique_name = str(uuid.uuid4())
    extension = Path(filename).suffix

    return f'faces/{unique_name[:2]}/{unique_name[2:4]}/{unique_name}{extension}'


def save_processed_image(image: Image) -> Path:
    """Returns public URL relative path"""

    unique_name = str(uuid.uuid4())
    filename = f'{unique_name}.jpg'
    relative_directory = Path('processed_faces') / unique_name[:2] / unique_name[2:4]
    storage_directory = settings.STORAGE_ROOT / relative_directory
    storage_directory.mkdir(parents=True, exist_ok=True)
    storage_path = storage_directory / filename
    image.save(storage_path, format='JPEG')
    public_path = settings.STATIC_URL / relative_directory / filename
    return public_path
