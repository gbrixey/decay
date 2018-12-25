import math
import random
from util import jpeg_header_length

################################
# IMAGE DEGRADING METHODS
################################

last_seed_used = 0
    
def degrade_jpeg_byte_array(byte_array):
    """Sets some of the bytes in the given jpeg byte array to zero.
    Number of bytes affected depends on the size of the array."""
    # Try not to edit the jpeg header.
    header_length = jpeg_header_length(byte_array)
    max_index = len(byte_array) - header_length - 4
    iterations = max(10, int(len(byte_array) / 50000))
    seed = random.randint(0, 100)
    global last_seed_used
    while seed == last_seed_used:
        seed = random.randint(0, 100)
    last_seed_used = seed
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
        
################################
# TEXT DEGRADING METHODS
################################
        
def degrade_text(text):
    """Adds several typographic errors to the given string and returns the result.
    The number of errors added depends on the length of the string."""
    count = int(len(text) / 8)
    # Add the delete function twice so that the length of the string will stay roughly the same.
    options = [delete_character, delete_character, swap_two_characters, duplicate_character, insert_character_from_text]
    for _ in range(count):
        option = random.choice(options)
        text = option(text)
    return text
    
def swap_two_characters(text):
    """Swaps two adjacent characters in the given string and returns the result."""
    index = random.randint(0, len(text) - 2)
    return text[:index] + text[index + 1] + text[index] + text[(index + 2):]
    
def duplicate_character(text):
    """Doubles up a character in the given string and returns the result.
    e.g. "sample" -> "samplle"
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
