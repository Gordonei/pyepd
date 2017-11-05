# PyEPD
# Gordon Inggs (gordon.e.inggs@ieee.org)
# November 2017

# These are the unit tests, is this wasn't clear from the filename
from unittest import TestCase

# Various libraries being used
import numpy
from PIL import Image
import io
import tempfile
from contextlib import contextmanager

# Classes under test
import pyepd.DisplayPanelController
import pyepd.ImageHandler


class TestPYEPD(TestCase):
    def setUp(self):
        # Making sure we get the same data everytime
        numpy.random.seed(1234)

    def test_dpc_header(self):
        tc_p74_230_header = numpy.array([0x3A, 0x01, 0xE0, 0x03, 0x20, 0x01, 0x04] +
                                        [0x00] * 9,
                                        dtype=numpy.uint8)

        tcm_p74_230 = pyepd.DisplayPanelController.TC_P74_230()
        self.assertListEqual(list(tcm_p74_230.generate_header()),
                             list(tc_p74_230_header),
                             "TCM-P74-230 header is not correct")

    def test_dpc_data(self):
        tp_p74_230_source_data = numpy.array([0x00, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x00] +
                                             [0x00, 0x01, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00] +
                                             [0x00] * (480 * 800 - 16),
                                             dtype=numpy.uint8)

        tp_p74_230_output_data = [0x00] * 29 + [0x98] + [0x00] * 29 + [0xEC] + [0x00] * (480 * 800 // 8 - 60)

        tcm_p74_230 = pyepd.DisplayPanelController.TC_P74_230()
        test_output_data = tcm_p74_230.generate_epd_image_data(tp_p74_230_source_data)

        self.assertListEqual(list(test_output_data),
                             tp_p74_230_output_data,
                             "TCM-P74-230 image conversion is not correct")

    def check_image_dimensions(self, test_size, expected_size):
        self.assertEquals(test_size[0], expected_size[0],
                          "Image x dimension not sized correctly")
        self.assertEquals(test_size[1], expected_size[1],
                          "Image y dimension not sized correctly")

    def test_image_acquistion(self):
        tcm_p74_230 = pyepd.DisplayPanelController.TC_P74_230()
        expected_size = (tcm_p74_230.x_res, tcm_p74_230.y_res)

        # Undersized image
        undersize = (100, 100)
        with generate_random_image(size=undersize, override_colour_value=0) as undersized_image, \
                generate_image_file(undersized_image) as undersized_image_file:
            with pyepd.ImageHandler.acquire_and_normalise(undersized_image_file.name, tcm_p74_230) as output_image:
                self.check_image_dimensions(output_image.size, expected_size)

        # Oversized image
        oversize = (1024, 1024)
        with generate_random_image(size=oversize, override_colour_value=0) as oversized_image, \
                generate_image_file(oversized_image) as oversized_image_file:
            with pyepd.ImageHandler.acquire_and_normalise(oversized_image_file.name, tcm_p74_230) as output_image:
                self.check_image_dimensions(output_image.size, expected_size)

        # Background colour
        with generate_random_image(size=undersize, override_colour_value=255) as undersized_image, \
                generate_image_file(undersized_image) as undersized_image_file:
            with pyepd.ImageHandler.acquire_and_normalise(undersized_image_file.name, tcm_p74_230) as output_image:
                source_data = numpy.array(undersized_image.getdata())
                output_data = numpy.array(output_image.getdata())

                self.assertEquals(source_data.sum(),
                                  output_data.sum(),
                                  "Border isn't being added correctly")

    def test_image_conversion(self):
        tcm_p74_230 = pyepd.DisplayPanelController.TC_P74_230()
        expected_size = (tcm_p74_230.x_res, tcm_p74_230.y_res)

        with generate_random_image(size=expected_size, override_colour_value=None) as random_image:
            output_data = pyepd.ImageHandler.convert(random_image)

            # Checking that we're preserving the input image's size
            self.assertEquals(output_data.size,
                              expected_size[0] * expected_size[1],
                              "Image size not being preserved in conversion.")

            # Checking that we're getting the right black and white image out.
            # Really, this just guarantees that the function is idempotent
            source_data = numpy.array(random_image.getdata())

            self.assertEquals(source_data.sum() // 3,  # Input has 3 pixels
                              (output_data ^ 255).sum(),  # Output has been inverted
                              "Image output values not being calculated correctly.")


# Utility functions


@contextmanager
def generate_random_image(size, override_colour_value=None):
    # Currying the data generation
    def generate_pixel_data(s):
        if override_colour_value is None:
            # Generate random black and white images
            source_vector = numpy.random.randint(0, 2, (s[0] * s[1],)) * 255
            output_values = numpy.vstack((source_vector, numpy.copy(source_vector), numpy.copy(source_vector)))
            return output_values.transpose()
        else:
            return numpy.ones((s[0] * s[1], 3), dtype=numpy.uint8) * override_colour_value

    # Generating a random image
    img_data = [tuple(pixel) for pixel in generate_pixel_data(size)]
    with Image.new("RGB", size=size) as randomised_image:
        randomised_image.putdata(img_data)

        yield randomised_image


@contextmanager
def generate_image_file(image):
    # Dumping out the raw data
    output = io.BytesIO()
    image.save(output, format='JPEG')

    # Writing it to a temp file
    with tempfile.NamedTemporaryFile() as temp_image_file:
        temp_image_file.write(output.getvalue())
        temp_image_file.file.seek(0)

        yield temp_image_file
