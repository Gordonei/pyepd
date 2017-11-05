from setuptools import setup

setup(name='pyepd',
      version='0.1',
      description="Package for generating the image format used by Pervasive Display's modules (EPD)",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Software Development :: Embedded Systems'
      ],
      url='https://github.com/Gordonei/pyepd',
      author='Gordon Inggs',
      author_email='gordon.e.inggs@ieee.org',
      license='MIT',
      packages=['pyepd'],
      install_requires=[
          'numpy',
          'Pillow'
      ],
      scripts=['bin/img2epd'],
      zip_safe=False)
