# django-resized

Resizes image origin to specified size. Compatible with sorl-thumbnail.

## Installation
    
    pip install django-resized


## Usage 

models.py

    from django_resized import ResizedImageField
    
    class MyModel(models.Model):
        ...
        image = ResizedImageField(max_width=500, max_height=300, upload_to='whatever')





