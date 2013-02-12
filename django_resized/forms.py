import os
try:
    from PIL import Image
except ImportError:
    import Image
from StringIO import StringIO

from django.conf import settings
from django.core.files.base import ContentFile

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField


DEFAULT_SIZE = getattr(settings, 'DJANGORESIZED_DEFAULT_SIZE', [1920, 1080])


class ResizedImageFieldFile(ImageField.attr_class):
    
    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)
        img = Image.open(content.file)
        img.thumbnail((
            self.field.max_width, 
            self.field.max_height
            ), Image.ANTIALIAS)
        img.save(new_content, format=img.format, **img.info)

        new_content = ContentFile(new_content.getvalue())

        super(ResizedImageFieldFile, self).save(name, new_content, save)


class ResizedImageField(ImageField):
    
    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.max_width = kwargs.pop('max_width', DEFAULT_SIZE[0])
        self.max_height = kwargs.pop('max_height', DEFAULT_SIZE[1])
        super(ResizedImageField, self).__init__(verbose_name, name, **kwargs) 
