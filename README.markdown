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
        image1 = ResizedImageField(width=500, height=300, upload_to='whatever')
        image2 = ResizedImageField(width=500, height=300, crop=['top', 'left'], upload_to='whatever')
        image2 = ResizedImageField(width=500, height=300, crop=['middle', 'center'], upload_to='whatever')
        image2 = ResizedImageField(width=500, height=300, quality=75, upload_to='whatever')

## How to run tests

    pip install -r django_resized/testapp/requirements.txt
    ./runtests.py
