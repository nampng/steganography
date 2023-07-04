import cv2
import numpy as np
import random
from types import FunctionType


def encode_simple(value: int, row: int, pix: int, image):
    """
    Select a random channel to store data.
    """

    channel = random.randint(0, 2)

    if image[row][pix][channel] + value < 255:
        image[row][pix][channel] += value
    else:
        image[row][pix][channel] -= value


def encode_split(value: int, row: int, pix: int, image):
    """
    Split the data between all channels to make pixel change more subtle.
    """

    values = []
    interval = value / 3

    if interval.is_integer():
        values = [interval, interval, interval]
    else:
        rounded = round(interval)
        if interval < rounded: # rounded up
            values = [rounded, rounded, rounded - 1]
        else: # rounded down
            values = [rounded, rounded, rounded + 1]

    for channel, val in zip(range(3), values):
        if image[row][pix][channel] + val < 255:
            image[row][pix][channel] += val
        else:
            image[row][pix][channel] -= val


def decode_simple(original_pixel: np.array, altered_pixel: np.array) -> str:
    """
    Decode a pixel that was encoded with simple algo.
    """

    original_pixel = original_pixel.astype(np.int16)
    altered_pixel = altered_pixel.astype(np.int16)

    delta = np.subtract(altered_pixel, original_pixel)

    condition = np.not_equal(delta, np.zeros((1, 3)))
    unicode_value = abs(np.extract(condition, delta)[0])

    print(original_pixel, altered_pixel, delta, unicode_value, chr(unicode_value))

    return chr(unicode_value)


def decode_split(original_pixel: np.array, altered_pixel: np.array) -> str:
    """
    Decode a pixel that was encoded with split algo. 
    Can also decode simple algo.
    """

    original_pixel = original_pixel.astype(np.int16)
    altered_pixel = altered_pixel.astype(np.int16)

    delta = np.subtract(altered_pixel, original_pixel)
    delta = np.abs(delta)

    unicode_value = int(np.sum(delta))

    print(original_pixel, altered_pixel, delta, unicode_value, chr(unicode_value))

    return chr(unicode_value)


def store_sequential(secret_str: str, file_path: str, encoder: FunctionType):
    """
    Store the secret string by just writing each pixel by row and column. Very simple and noticeable.
    Will alter pixel depending on given encoder function.
    """

    print("SIMPLE - Storing secret into image...")
    image = cv2.imread(file_path)
    rows, cols, _ = image.shape
    secret = list(secret_str)

    if rows * cols < len(secret):
        raise ValueError("More data than pixels.")

    for row in range(rows):
        for pix in range(cols):
            if not secret:
                file_name = file_path.split('.')[0].split('/')[1]
                cv2.imwrite("outputs/output-"+file_name+".png", image)
                print("Done!")
                return

            char = secret.pop()

            encoder(ord(char), row, pix, image)


def store_spread(secret_str: str, file_path: str, encoder: FunctionType):
    """
    Make an effort to hide the changed pixels by spreading them out throughout the image.
    Will alter pixel depending on given encoder function.
    """

    print("SPREAD - Storing secret into image...")
    image = cv2.imread(file_path)
    rows, cols, _ = image.shape
    total = rows * cols
    
    secret = list(secret_str)
    interval = total // len(secret)

    if interval == 0:
        raise ValueError("More data than pixels, cannot spread since interval == 0")

    count = 0

    indexes = []

    for c in secret:
        indexes.append((count * interval) + random.randint(0, interval - 1))
        count += 1

    count = 0

    for row in range(rows):
        for pix in range(cols):
            if not secret:
                file_name = file_path.split('.')[0].split('/')[1]
                cv2.imwrite("outputs/output-"+file_name+".png", image)
                print("Done!")
                return

            count += 1

            if count == indexes[0]:
                indexes.pop(0)
                char = secret.pop()

                encoder(ord(char), row, pix, image)


def get_secret_string(original_file_path: str, alt_file_path: str, decoder: FunctionType) -> str:
    """
    Decode the hidden message by comparing every single pixel between the old and new image.
    The pair of pixels will be given to the given decoder function.
    """

    print("Decoding image.")

    original = cv2.imread(original_file_path)
    altered = cv2.imread(alt_file_path)

    rows, cols, _ = original.shape

    secret_str = []

    for row in range(rows):
        for pix in range(cols):
            if not (original[row][pix] == altered[row][pix]).all():
                char = decoder(original[row][pix], altered[row][pix])
                secret_str.append(char)

    return ''.join(reversed(secret_str))

def read_secret_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    secret_str = read_secret_from_file("secret_string.txt")
    file_path = "inputs/minecraft_house.jpg"
    file_name = file_path.split('.')[0].split('/')[1]

    # store_simple(secret_str=secret_str, file_path=file_path)
    # secret = get_secret_string(original_file_path=file_path, alt_file_path="outputs/output-"+file_name+".png", decoder=decode_split)

    store_spread(secret_str=secret_str, file_path=file_path, encoder=encode_split)
    secret = get_secret_string(original_file_path=file_path, alt_file_path="outputs/output-"+file_name+".png", decoder=decode_split)

    print("Decoded secret is", secret)