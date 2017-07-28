# LSB-steganography

This is a Python module which facilitates text hiding in an image, using the LSB technique. 
It was made using Python 3.4.2 and the PIL image processing library. 
It works with JPEG and PNG formats for the cover image and always creates PNG stego image due to its lossless compression.

The input message is converted to binary form and a binary ending sequence is attached along with the message to signal its end.
After that the message is embedded in the LSB of each RGB value of every pixel and a new image is created in PNG form.

Once the message is embedded and a new cover image is created containing the message,
we can extract the message by reading all LSBs from the cover image's pixels until the ending bit sequence is found.

The message is then converted to ASCII and becomes readable.
