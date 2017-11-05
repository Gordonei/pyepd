# PyEPD
# Gordon Inggs (gordon.e.inggs@ieee.org)
# November 2017

import numpy
from PIL import Image

from contextlib import contextmanager


@contextmanager
def acquire_and_normalise(filename, display_panel_controller, background_colour=0, rotate_count=0):
    """
    Reads in input image, and converts to correct size. Adds a border if necessary.

    :param filename: path to image file to use
    :param display_panel_controller: display panel controller that is being used.
    :param background_colour: default background colour value to use (0 is black, 255 is white).
    :param rotate_count: rotate image by specified number of 90° rotations
    :return: PIL image object
    """
    x_res = display_panel_controller.x_res
    y_res = display_panel_controller.y_res
    size = (x_res, y_res)

    with Image.open(filename) as img:
        img = img.rotate(90 * rotate_count, expand=True)

        # Coping with images of a different size
        if img.size[0] != x_res or img.size[1] != y_res:
            # Resizing
            img.thumbnail(size, Image.ANTIALIAS)

            # Centering the image, and adding a border
            background = Image.new('RGB', size, (background_colour, background_colour, background_colour))
            background.paste(img,
                             ((x_res - img.size[0]) // 2, (y_res - img.size[1]) // 2)
                             )
            img = background

        yield img


def convert(image):
    """
    Convert image data to 1-bit colour depth data array. Also inverts the image.

    :param image: PIL Image object
    :return: 1-bit image data array
    """

    # converts to 1-bit colour and dithers
    data = image.convert('1').getdata()

    # Converting to numpy array
    data = numpy.asarray(data)

    # Inverting the colours
    data ^= 255

    return data
