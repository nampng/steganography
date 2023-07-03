import cv2
import numpy as np
import random
from types import FunctionType

"""
Select a random channel to store data.
"""
def change_pixel_channel_simple(value: int, row: int, pix: int, image):
    channel = random.randint(0, 2)

    if image[row][pix][channel] + value < 255:
        image[row][pix][channel] += value
    else:
        image[row][pix][channel] -= value

"""
Spread the data between all channels to make pixel change more subtle.

if divisble by 3, easy

if not, hard? everything will end in .33 or .66

10 / 3 = 3.33 -> 3 + 3 + 4 -> if it ends in 3.33 add 1 to the ones place
 
8 / 3 = 2.66 -> 2 + 2 + 4 -> if it ends in .66 add 2 to ones place

more examples:

61 / 3 = 20.33 -> 20 + 20 + 21 = 61
62 / 3 = 20.66 -> 20 + 20 + 22 = 62

71 / 3 = 23.66 -> 23 + 23 + 25 = 71

Not really sure how to detect the .33 or .66 so I'll just do it in a way that makes sense to me.

If rounded down, rounded + rounded + rounded + 1
If rounded up, rounded + rounded + rounded - 1

61 / 3 = 20.33 -> 20 + 20 + 21 = 61

71 / 3 = 23.66 -> 24 + 24 + 23 = 71
"""
def change_pixel_channel_spread(value: int, row: int, pix: int, image):
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

def decode_simple_pixel(original_pixel: np.array, altered_pixel: np.array) -> str:
    original_pixel = original_pixel.astype(np.int16)
    altered_pixel = altered_pixel.astype(np.int16)

    delta = np.subtract(altered_pixel, original_pixel)

    condition = np.not_equal(delta, np.zeros((1, 3)))
    unicode_value = abs(np.extract(condition, delta)[0])

    # print(original_pixel, altered_pixel, delta, unicode_value, chr(unicode_value))

    return chr(unicode_value)

def decode_spread_pixel(original_pixel: np.array, altered_pixel: np.array) -> str:
    original_pixel = original_pixel.astype(np.int16)
    altered_pixel = altered_pixel.astype(np.int16)

    delta = np.subtract(altered_pixel, original_pixel)
    delta = np.abs(delta)

    unicode_value = int(np.sum(delta))

    # print(original_pixel, altered_pixel, delta, unicode_value, chr(unicode_value))

    return chr(unicode_value)

"""
Store the secret string by just writing each pixel by row and column. Very simple and noticeable.
"""
def store_secret_string_simple(secret_str: str, file_path: str, encoder: FunctionType):
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

"""
Make an effort to hide the changed pixels by spreading them out throughout the image.
"""
def store_secret_string_spread(secret_str: str, file_path: str, encoder: FunctionType):
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

"""
Decode the hidden message by comparing every single pixel between the old and new image.
"""
def decode_secret_string(original_file_path: str, alt_file_path: str, decoder: FunctionType) -> str:
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
    file_path = "inputs/blizzard.jpg"
    file_name = file_path.split('.')[0].split('/')[1]

    # store_secret_string_simple(secret_str=secret_str, file_path=file_path, encoder=change_pixel_channel_spread)
    # secret = decode_secret_string(original_file_path=file_path, alt_file_path="outputs/output-"+file_name+".png", decoder=decode_spread_pixel)

    store_secret_string_spread(secret_str=secret_str, file_path=file_path, encoder=change_pixel_channel_spread)
    secret = decode_secret_string(original_file_path=file_path, alt_file_path="outputs/output-"+file_name+".png", decoder=decode_spread_pixel)

    print("Decoded secret is", secret)