import os
import Image
from StringIO import StringIO

from django.core.files.base import ContentFile

from sorl.thumbnail import ImageField


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

    def __init__(self, verbose_name=None, name=None, upload_to='', max_width=800, max_height=600, storage=None, **kwargs):
        self.max_width = max_width
        self.max_height = max_height
        super(ResizedImageField, self).__init__(verbose_name, name, upload_to, storage, **kwargs) 
