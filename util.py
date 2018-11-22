from PIL import Image, ExifTags

def jpeg_image_from_file(image_file):
    """Returns a PIL image by reading from the given file.
    Returns None if the image is not a valid jpeg."""
    try:
        image = Image.open(image_file)
    except:
        return None
    if image.format != 'JPEG':
        return None
    return image

def jpeg_header_length(byte_array):
    """Finds the length of a jpeg header, given the jpeg data in byte array format"""
    result = 417
    for i in range(len(byte_array) - 3):
        if byte_array[i] == 0xFF and byte_array[i + 1] == 0xDA:
            result = i + 2
            break
    return result

def rotate_image_if_necessary(image):
    """Given a PIL image, this function returns a rotated image
    if camera orientation info can be found in the EXIF data."""
    orientation = 1
    for k, v in ExifTags.TAGS.items():
        if v == 'Orientation':
            exif = image._getexif()
            if k in exif:
                orientation = exif[k]
            break
    if orientation == 3:
        return image.rotate(180, expand = True)
    elif orientation == 6:
        return image.rotate(270, expand = True)
    elif orientation == 8:
        return image.rotate(90, expand = True)
    else:
        return image
