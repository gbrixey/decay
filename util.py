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

def jpeg_header_length(byte_array):
    """Finds the length of a jpeg header, given the jpeg data in byte array format"""
    result = 417
    for i in range(len(byte_array) - 3):
        if byte_array[i] == 0xFF and byte_array[i + 1] == 0xDA:
            result = i + 2
            break
    return result
