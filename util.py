from PIL import Image, ExifTags

IMAGE_WIDTH = 1200

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
            if exif != None and k in exif:
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

def resize_image_if_necessary(image):
    """Returns an image constrained to a desired size."""
    if image.width != IMAGE_WIDTH:
        height = int(image.height * (IMAGE_WIDTH / image.width))
        return image.resize((IMAGE_WIDTH, height))
    else:
        return image

def crop_image_if_necessary(image):
    """Crops the image to a 3:1 aspect ratio"""
    aspect_ratio = image.width / image.height
    if aspect_ratio > 3:
        # Image is wider than 3:1 (e.g. a panorama)
        desired_width = image.height * 3
        left = (image.width - desired_width) / 2
        right = left + desired_width
        bottom = image.height
        return image.crop((left, 0, right, bottom))
    elif aspect_ratio < 3:
        # Image is narrower than 3:1
        # Most images will fall into this category
        desired_height = image.width / 3
        top = (image.height - desired_height) / 2
        bottom = top + desired_height
        right = image.width
        return image.crop((0, top, right, bottom))
    else:
        return image
        