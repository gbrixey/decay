import math
import random
from PIL import Image, ExifTags
from constants import BLOCK_SIZE, IMAGE_WIDTH, ASPECT_RATIO

def jpeg_image_from_file(image_file):
    """Returns a PIL image by reading from the given file.
    Returns None if the image is not a valid jpeg."""
    try:
        image = Image.open(image_file)
    except IOError as err:
        print("Error opening image: {0}".format(err))
        return None
    if image.format != 'JPEG':
        print("Rejecting image with format: " + image.format)
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
    """Crops the image until its aspect ratio is equal to ASPECT_RATIO.
    Note that the width of the resulting image may not be equal to
    IMAGE_WIDTH."""
    aspect_ratio = image.width / image.height
    if aspect_ratio > ASPECT_RATIO:
        # Image is wider than it should be
        desired_width = image.height * ASPECT_RATIO
        left = (image.width - desired_width) / 2
        right = left + desired_width
        bottom = image.height
        return image.crop((left, 0, right, bottom))
    elif aspect_ratio < ASPECT_RATIO:
        # Image is narrower than it should be
        desired_height = image.width / ASPECT_RATIO
        top = (image.height - desired_height) / 2
        bottom = top + desired_height
        right = image.width
        return image.crop((0, top, right, bottom))
    else:
        return image

def random_block(image):
    """Returns a random index from the image where the x and y values are
    multiples of BLOCK_SIZE."""
    columns = math.floor(image.width / BLOCK_SIZE)
    rows = math.floor(image.height / BLOCK_SIZE)
    blocks = columns * rows
    random_block = random.randint(0, blocks - 1)
    random_column = random_block % columns
    random_row = math.floor(random_block / columns)
    return (random_column * BLOCK_SIZE, random_row * BLOCK_SIZE)
