.. image:: https://github.com/un1t/django-resized/actions/workflows/python-app.yml/badge.svg
    :target: https://github.com/un1t/django-resized/actions/workflows/python-app.yml

Resizes image origin to specified size. Compatible with sorl-thumbnail. Inherits from ImageField.

Features
========

- Tested on Django 3.2, 4.0, 4.1, 4.2
- Python 3 support

Installation
============

.. code-block:: bash

    pip install django-resized


Configuration (optional)
========================

settings.py

.. code-block:: python

    DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
    DJANGORESIZED_DEFAULT_SCALE = 0.5
    DJANGORESIZED_DEFAULT_QUALITY = 75
    DJANGORESIZED_DEFAULT_KEEP_META = True
    DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
    DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
    DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
    

Usage
=====

models.py

.. code-block:: python

    from django_resized import ResizedImageField

    class MyModel(models.Model):
        ...
        image1 = ResizedImageField(size=[500, 300], upload_to='whatever')
        image2 = ResizedImageField(size=[100, 100], crop=['top', 'left'], upload_to='whatever')
        image3 = ResizedImageField(size=[100, 150], crop=['middle', 'center'], upload_to='whatever')
        image4 = ResizedImageField(scale=0.5, quality=75, upload_to='whatever')
        image5 = ResizedImageField(size=None, upload_to='whatever', force_format='PNG')
        image6 = ResizedImageField(size=[100, None], upload_to='whatever')

Options
-------


- **size** - max width and height, for example [640, 480]. If a dimension is None, it will resized using the other value and maintains the ratio of the image. If size is None, the original size of the image will be kept.
- **scale** - a float, if not None, which will rescale the image after the image has been resized.
- **crop** - resize and crop. ['top', 'left'] - top left corner, ['middle', 'center'] is center cropping, ['bottom', 'right'] - crop right bottom corner.
- **quality** - quality of resized image 0..100, -1 means default
- **keep_meta** - keep EXIF and other meta data, default True
- **force_format** - force the format of the resized image, available formats are the one supported by `pillow <https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#image-file-formats>`_, default to None


How to run tests
================

.. code-block:: bash

    pip install tox
    tox
