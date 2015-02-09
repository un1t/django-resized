# django-resized

Resizes image origin to specified size. Compatible with sorl-thumbnail.

## Installation
    
    pip install django-resized


# Configuration (optional)

settings.py

    DJANGORESIZED_DEFAULT_SIZE = [800, 600]

Default size is 1920x1080.

## Field options

    use_thumbnail_aspect_ratio

Defaults to False.  If set to True, the thumbnail will have the full specified or default size and will be centered if it does not occupy the full space in either dimension.

    background_color

Defaults to transparent or white (depending on whether the source image supports transparency).  Only used if use_thumbnail_aspect_ratio is True.

## Usage 

models.py

    from django_resized import ResizedImageField
    
    class MyModel(models.Model):
        ...
        image = ResizedImageField(max_width=500, max_height=300, upload_to='whatever')

## How to run tests

    pip install -r django_resized/testapp/requirements.txt
    ./runtests.py
