import io

import magic
from fastapi import UploadFile

from src.media_storage.schemas import MediaCreate


def guess_media_type(data: bytes) -> str:
    """
    Determine the MIME type of the given byte data.

    This function uses the `magic` library to analyze the bytes of the input data and
    returns the corresponding MIME type as a string. The MIME type can be used to identify
    the format of the data (e.g., 'image/jpeg', 'text/plain').

    Parameters:
    - data (bytes): The data whose MIME type needs to be determined.

    Returns:
    - str: The MIME type of the input data.
    """
    mime = magic.Magic(mime=True)
    return mime.from_buffer(data)


def get_file_name(media_create: MediaCreate) -> str:
    return media_create.file_name


def read_upload_file(file: UploadFile) -> (io.BytesIO, int):
    file_io = io.BytesIO()

    contents = file.file.read()
    file_io.write(contents)
    file_size = len(contents)

    file_io.seek(0)

    return file_io, file_size
