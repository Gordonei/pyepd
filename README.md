**PyEPD**
---------
Library for generating the image format used by Pervasive Display's Mpico control modules (EPD).

Supports a wide range of input image formats, and uses dithering to produce greyscale output images.

Setup
----
Should be installable from pip3:
```bash
pip3 install pyepd
```

Alternatively from the command line (in the repo root directory):
```bash
python3 setup.py install
```

Running
----
In addition to installing the `pyepd` Python library, a utility script `img2epd` should be installed:
```
usage: img2epd [-h] [-w] [-r] [-d {TCM-P74-230}] input_image output_image

positional arguments:
  input_image           Path of input image file
  output_image          Path of output image file

optional arguments:
  -h, --help            show this help message and exit
  -w, --white-background
                        Set background to be white. Default is black.
  -r, --rotate          Rotate image 90° right. May be used multiple times.
  -d {TCM-P74-230}, --device {TCM-P74-230}
                        Select display panel controller. Default is
                        TCM-P74-230.
```

Limitations
-----------
Currently only the TC-P74-230 (7.4") module is supported.
Adding support for other modules types should be relatively straight-forward.

I'm very open to pull requests or engineering samples to enhance the package.
