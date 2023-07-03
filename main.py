import cv2
import numpy as np
import random

"""
Store the secret string by just writing each pixel by row and column. Very simple and noticeable.
"""
def store_secret_string_simple(secret_str: str, file_path: str):
    print("SIMPLE - Storing secret into image...")
    image = cv2.imread(file_path)
    rows, cols, _ = image.shape
    secret = list(secret_str)

    for row in range(rows):
        if not secret:
            break

        for pix in range(cols):
            if not secret:
                break

            char = secret.pop(0)

            val = ord(char)

            random_index = random.randint(0, 2)

            if image[row][pix][random_index] + val < 255:
                image[row][pix][random_index] += val
            else:
                image[row][pix][random_index] -= val

    file_name = file_path.split('.')[0].split('/')[1]
    cv2.imwrite("outputs/output-"+file_name+".png", image)
    print("Done!")

"""
Make an effort to hide the changed pixels by spreading them out throughout the image.

If an image is 100 x 100, then there are 10000 potential places to place a character. We'd also like to place characters in sequential order.

Example: we have 10 characters

Divide 10000 by 10, each character will be randomly placed within their 1000 pixel section.

We're going to do it the dumb way first and then optimize.
"""
def store_secret_string_spread(secret_str: str, file_path: str):
    image = cv2.imread(file_path)
    secret = list(secret_str)
    rows, cols, _ = image.shape

    total = rows * cols

    interval = total // len(secret)

    if interval == 0:
        print("Too much data. Can't do it man!")
        raise ValueError("More data than pixels, cannot spread since interval == 0")

    count = 0

    indexes = []

    for c in secret:
        indexes.append((count * interval) + random.randint(0, interval - 1))
        count += 1

    count = 0

    for row in range(rows):
        if not secret:
            break
        for pix in range(cols):
            if not secret:
                break

            count += 1

            if count == indexes[0]:
                indexes.pop(0)
                char = secret.pop(0)

                val = ord(char)
                
                random_index = random.randint(0, 2)

                if image[row][pix][random_index] + val < 255:
                    image[row][pix][random_index] += val
                else:
                    image[row][pix][random_index] -= val

    file_name = file_path.split('.')[0].split('/')[1]
    cv2.imwrite("outputs/output-"+file_name+".png", image)
    print("Done!")

"""
Decode the hidden message by comparing every single pixel between the old and new image.
"""
def decode_secret_string(original_file_path: str, alt_file_path: str):
    print("Decoding image.")

    original = cv2.imread(original_file_path)
    altered = cv2.imread(alt_file_path)

    rows, cols, _ = original.shape

    secret_str = []

    for row in range(rows):
        for pix in range(cols):
            for orig_pix, alt_pix in zip(original[row][pix], altered[row][pix]):
                if orig_pix != alt_pix:
                    val = abs(int(alt_pix) - int(orig_pix))
                    secret_str.append(chr(val))

    return ''.join(secret_str)

def read_secret_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
                
if __name__ == "__main__":
    secret_str = read_secret_from_file("secret_string.txt")
    file_path = "inputs/minecraft_house.jpg"
    file_name = file_path.split('.')[0].split('/')[1]
    store_secret_string_spread(secret_str=secret_str, file_path=file_path)
    secret = decode_secret_string(original_file_path=file_path, alt_file_path="outputs/output-"+file_name+".png")
    print("Decoded secret is", secret)