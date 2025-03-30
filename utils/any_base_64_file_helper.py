import io
import logging
import magic  # To detect file types
from drf_extra_fields.fields import Base64FileField

logger = logging.getLogger(__name__)


class Base64AnyFileField(Base64FileField):
    """Custom Base64 file field that accepts any file type with validation."""

    def __init__(self, required=True, allow_empty_file=False, **kwargs):
        super().__init__(required=required, allow_empty_file=allow_empty_file, **kwargs)

    ALLOWED_TYPES = [
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "txt",
        "jpg",
        "jpeg",
        "png",
        "gif",
        "zip",
        "tar",
        "mp4",
        "mp3",
    ]
    MIME_TYPES = {
        "pdf": "application/pdf",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "txt": "text/plain",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "zip": "application/zip",
        "tar": "application/x-tar",
        "mp4": "video/mp4",
        "mp3": "audio/mpeg",
    }

    def get_file_extension(self, filename, decoded_file):
        """Check file validity and return the file extension."""
        mime = magic.Magic(mime=True)
        detected_mime_type = mime.from_buffer(decoded_file)

        # Find the file extension based on detected MIME type
        file_extension = None
        for ext, mime_type in self.MIME_TYPES.items():
            if mime_type == detected_mime_type:
                file_extension = ext
                break

        if file_extension and file_extension in self.ALLOWED_TYPES:
            return file_extension
        else:
            logger.warning(f"Invalid file type: {detected_mime_type}")
            raise ValueError("Unsupported file type.")
