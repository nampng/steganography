import argparse
import sys
import cv2
import numpy as np
import random
from types import FunctionType

def decode_simple(original_pixel: np.array, altered_pixel: np.array) -> str:
    """
    Decode a pixel that was encoded with simple algo.
    """

    original_pixel = original_pixel.astype(np.int16)
    altered_pixel = altered_pixel.astype(np.int16)

    delta = np.subtract(altered_pixel, original_pixel)

    condition = np.not_equal(delta, np.zeros((1, 3)))
    unicode_value = abs(np.extract(condition, delta)[0])

    # print(original_pixel, altered_pixel, delta, unicode_value, chr(unicode_value))

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

    # print(original_pixel, altered_pixel, delta, unicode_value, chr(unicode_value))

    return chr(unicode_value)

def get_secret_string(orig_file_path: str, alt_file_path: str, decoder: FunctionType) -> str:
    """
    Decode the hidden message by comparing every single pixel between the old and new image.
    The pair of pixels will be given to the given decoder function.
    """

    print("Decoding image.")

    original = cv2.imread(orig_file_path)
    altered = cv2.imread(alt_file_path)

    rows, cols, _ = original.shape

    secret_str = []

    for row in range(rows):
        for pix in range(cols):
            if not (original[row][pix] == altered[row][pix]).all():
                char = decoder(original[row][pix], altered[row][pix])
                secret_str.append(char)

    return ''.join(reversed(secret_str))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog="decoder.py",
    description="Retrieve a secret by comparing the source image to the altered image.",
    epilog="Thanks for trying my program. - Nam"
    )
    parser.add_argument("original_image_path", help="Path of original image")
    parser.add_argument("altered_image_path", help="Path of altered image")
    parser.add_argument("decoder", choices=["simple", "split"])
    parser.add_argument("-s", "--save", action="store_true")
    args = parser.parse_args()

    print(args)

    if args.decoder == "simple":
        decoder = decode_simple
    else:
        decoder = decode_split

    try:
        secret = get_secret_string(
            orig_file_path=args.original_image_path, 
            alt_file_path=args.altered_image_path,
            decoder=decoder
        )

        print(f"The secret is:\n\n{secret}\n\n")

        if args.save:
            with open("output-secret.txt", "w") as file:
                file.write(secret)

    except Exception as e:
        print(e)