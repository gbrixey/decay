import math
import numpy
import random
from PIL import Image, ImageChops
from util import jpeg_header_length, jpeg_image_from_file, random_block
from constants import BLOCK_SIZE

################################
# IMAGE DEGRADING METHODS
################################

LAST_SEED_USED = 0
    
def degrade_jpeg_byte_array(byte_array):
    """Sets some of the bytes in the given jpeg byte array to zero.
    Number of bytes affected depends on the size of the array."""
    # Try not to edit the jpeg header.
    header_length = jpeg_header_length(byte_array)
    max_index = len(byte_array) - header_length - 4
    iterations = max(10, int(len(byte_array) / 50000))
    seed = random.randint(0, 100)
    global LAST_SEED_USED
    while seed == LAST_SEED_USED:
        seed = random.randint(0, 100)
    LAST_SEED_USED = seed
    seed_percent = seed / 100
    for i in range(iterations):
        min_pixel_index = math.floor(max_index / iterations * i)
        max_pixel_index = math.floor(max_index / iterations * (i + 1))
        delta = max_pixel_index - min_pixel_index
        pixel_index = math.floor(min_pixel_index + delta * seed_percent)
        if pixel_index > max_index:
            pixel_index = max_index
        index_in_byte_array = math.floor(header_length + pixel_index)
        byte_array[index_in_byte_array] = 0x00
    return byte_array

def degrade_jpeg(input_file, output_file):
    """Randomly edits bytes in the given jpeg file and writes the result to the output file."""
    with open(input_file, 'rb') as f:
        input_byte_array = bytearray(f.read())
    output_byte_array = degrade_jpeg_byte_array(input_byte_array)
    with open(output_file, 'wb') as f:
        f.write(output_byte_array)

def fake_degrade_jpeg(input_file, output_file):
    """Manipulates the image to achieve a similar effect to degrade_jpeg, but without
    corrupting the file."""
    image = jpeg_image_from_file(input_file)
    iterations = 10
    options = [fake_adjust_color, fake_offset]
    weights = [0.8, 0.2]
    for i in range(iterations):
        option = numpy.random.choice(options, p = weights)
        image = option(image)
    image.save(output_file, quality = 50, optimize = True)
    
def fake_adjust_color(image):
    """Randomly adjusts the RGB values of part of the image."""
    component = random.randint(0, 2)
    amount = random.randint(20, 40)
    start_column, start_row = random_block(image)
    array = numpy.zeros((image.height, image.width, 3), dtype = numpy.uint8)
    array[start_row:(start_row + BLOCK_SIZE), start_column:, component].fill(amount)
    if start_row + BLOCK_SIZE < image.height:
        array[(start_row + BLOCK_SIZE):, :, component].fill(amount)
    map_image = Image.fromarray(array, 'RGB')
    # Add or subtract
    if random.choice([True, False]):
        return ImageChops.add(image, map_image)
    else:
        return ImageChops.subtract(image, map_image)

def fake_offset(image):
    """Randomly moves parts of the image right or left."""
    start_column, start_row = random_block(image)
    cropped_image = image.crop((0, start_row, image.width, image.height))  
    offset = random.choice([-1, 1]) * BLOCK_SIZE
    offset_image = ImageChops.offset(cropped_image, offset, 0)
    image.paste(offset_image, (0, start_row))
    return image

################################
# TEXT DEGRADING METHODS
################################
        
def degrade_text(text):
    """Adds several typographic errors to the given string and returns the result.
    The number of errors added depends on the length of the string."""
    iterations = int(len(text) / 8)
    options = [delete_character, delete_character_leaving_space, swap_two_characters, duplicate_character, insert_character_from_text]
    for _ in range(iterations):
        option = random.choice(options)
        text = option(text)
    return text
    
def swap_two_characters(text):
    """Swaps two adjacent characters in the given string and returns the result."""
    index = random.randint(0, len(text) - 2)
    return text[:index] + text[index + 1] + text[index] + text[(index + 2):]
    
def duplicate_character(text):
    """Doubles up a character in the given string and returns the result.
    e.g. "example" -> "examplle"
    """
    index = random.randint(0, len(text) - 1)
    return text[:index] + text[index] + text[index] + text[(index + 1):]
    
def insert_character_from_text(text):
    """Selects a character in the given string, inserts a copy of that character
    somewhere else in the string, and returns the result."""
    new_character = random.choice(text)
    index = random.randint(0, len(text))
    return text[:index] + new_character + text[index:]

def delete_character(text):
    """Deletes a character from the given string and returns the result."""
    index = random.randint(0, len(text) - 1)
    return text[:index] + text[(index + 1):]

def delete_character_leaving_space(text):
    """Deletes a character from the given string, leaving a space. Returns the result."""
    index = random.randint(0, len(text) - 1)
    return text[:index] + ' ' + text[(index + 1):]
