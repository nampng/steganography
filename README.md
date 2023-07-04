# steganography

A small weekend project for exploring steganography.

The two main files you'll be interested in will be `encoder.py` and `decoder.py`.

## Encoder

Hide the contents of a text file inside of an image.

Pixel selection:

- Sequential
  - Insert data sequentially starting from the very first pixel.
  - Results in a very obvious streak of changed pixels at the top of the image.

- Spread
  - Spread the data throughout the image
  - Results in harder to find pixels that are scattered throughout the image.
 
Encoding:

- Simple
  - Simply choose random color channel to store the unicode value of a character.
  - Results in a distinct change in color of the pixel.
    
- Split
  - Divide the unicode value into three parts and add the values to all three color channels.
  - Results in a slightly lighter or darker color pixel.
 
## Decoder

Use the original image as a key to decode the altered image.

Decoding:

- Simple
  - Used to decode images that used simple encoding
  - Using this on an image that used split encoding will lead to gibberish.
 
- Split
  - Used to decode images that used split encoding.
  - Can also decode simple encoding.
