import argparse
import sys
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

def store_sequential(secret_str: str, file_path: str, output_dir: str, encoder: FunctionType):
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
                file_name = file_path.split('.')[0]
                cv2.imwrite(f"{output_dir}/output-"+file_name+".png", image)
                print("Done!")
                return

            char = secret.pop()

            encoder(ord(char), row, pix, image)


def store_spread(secret_str: str, file_path: str, output_dir: str, encoder: FunctionType):
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
                r = file_path.rindex(".")
                l = file_path.rindex("/")

                file_name = file_path[l+1:r]

                print(file_name)

                cv2.imwrite(f"{output_dir}/output-"+file_name+".png", image)
                print("Done!")
                return

            count += 1

            if count == indexes[0]:
                indexes.pop(0)
                char = secret.pop()

                encoder(ord(char), row, pix, image)

def read_secret_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog="encoder.py",
    description="Encode a secret into an image.",
    epilog="Thanks for trying my program. - Nam"
    )
    parser.add_argument("image_path", help="path of image")
    parser.add_argument("secret_text_path", help="Path of secret text file")
    parser.add_argument(
        "store", 
        choices=["seq", "spread"], 
        help="Sequential - will store data in sequential order. Spread - spread data throughout the image."
        )
    parser.add_argument(
        "encoder", 
        choices=["simple", "split"], 
        help="Simple - target one color channel to write data to. Split - split data between all three color channels."
        )
    parser.add_argument("--output", default="./outputs", help="Output dir")

    args = parser.parse_args()

    print(args)

    if args.store == "seq":
        store = store_sequential
    else:
        store = store_spread

    if args.encoder == "simple":
        encoder = encode_simple
    else:
        encoder = encode_split

    # try:
    secret = read_secret_from_file(file_path=args.secret_text_path)
    store(secret_str=secret, file_path=args.image_path, output_dir=args.output,  encoder=encoder)

    # except Exception as e:
    #     print(e)