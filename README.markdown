# django-resized

Resizes image origin to specified size. Compatible with sorl-thumbnail.

## Installation

    pip install django-resized


# Configuration (optional)

settings.py

    DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
    DJANGORESIZED_DEFAULT_QUALITY = 75


## Usage

models.py

    from django_resized import ResizedImageField

    class MyModel(models.Model):
        ...
        image1 = ResizedImageField(size=[500, 300], upload_to='whatever')
        image2 = ResizedImageField(size=[100, 100], crop=['top', 'left'], upload_to='whatever')
        image3 = ResizedImageField(size=[100, 100], crop=['middle', 'center'], upload_to='whatever')
        image4 = ResizedImageField(size=[500, 300], quality=75, upload_to='whatever')

### Options

    size - max width and height, for example [640, 480]
    crop - resize and crop. ['top', 'left'] - top left corner, ['middle', 'center'] is center cropping, ['bottom', 'right'] - crop right bottom corner.
    quality - quality of resized image 1..100


## How to run tests

    pip install -r django_resized/testapp/requirements.txt
    ./runtests.py

## Move to 0.3.x

If you use South, you may receive such error:

    TypeError: __init__() got an unexpected keyword argument 'max_width'

Just remove old arguments (max_width, max_height, use_thumbnail_aspect_ratio, background_color) from last South migrations file.

