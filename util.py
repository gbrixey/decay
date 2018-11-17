from uuid import uuid4

def is_valid_jpeg_file(image_file):
    """Returns True if the given file is a jpeg, or False otherwise.
    This function just performs some basic checks and is not guaranteed to be 100% accurate."""
    # Check file extension first.
    filename = image_file.filename
    jpeg_extensions = set(['jpg', 'jpeg'])
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in jpeg_extensions:
        # Then check the actual image data.
        b = bytearray(image_file.read())
        image_file.seek(0)
        return b[0] == 0xFF and b[1] == 0xD8 and b[-2] == 0xFF and b[-1] == 0xD9
    return False

def small_uuid():
    """Returns the first 8 characters of a random uuid."""
    return str(uuid4())[:8]