# django-resized

Resizes image origin to specified size. Compatible with sorl-thumbnail.

## Installation
    
    pip install django-resized


# Configuration (optional)

settings.py

    DJANGORESIZED_DEFAULT_SIZE = [800, 600]

Default size is 1920x1080.

## Usage 

models.py

    from django_resized import ResizedImageField
    
    class MyModel(models.Model):
        ...
        image = ResizedImageField(max_width=500, max_height=300, upload_to='whatever')





