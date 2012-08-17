import os
import Image
from StringIO import StringIO

from django.core.files.base import ContentFile

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField


class ResizedImageFieldFile(ImageField.attr_class):
    
    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)
        img = Image.open(content.file)
        img.thumbnail((
            self.field.max_width, 
            self.field.max_height
            ), Image.ANTIALIAS)
        img.save(new_content, format=img.format)

        new_content = ContentFile(new_content.getvalue())

        super(ResizedImageFieldFile, self).save(name, new_content, save)


class ResizedImageField(ImageField):
    
    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.max_width = kwargs.get('max_width', 800)
        self.max_height = kwargs.get('max_height', 600)
        super(ResizedImageField, self).__init__(verbose_name, name, **kwargs) 
