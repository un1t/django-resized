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
        thumb = Image.open(content.file)
        thumb.thumbnail((
            self.field.max_width, 
            self.field.max_height
            ), Image.ANTIALIAS)
        
        if self.field.use_thumbnail_aspect_ratio:
            img = Image.new("RGBA", (self.field.max_width, self.field.max_height), self.field.background_color)
            img.paste(thumb, ((self.field.max_width - thumb.size[0]) / 2, (self.field.max_height - thumb.size[1]) / 2))
        else:
            img = thumb
        
        img.save(new_content, format=thumb.format, **img.info)

        new_content = ContentFile(new_content.getvalue())

        super(ResizedImageFieldFile, self).save(name, new_content, save)


class ResizedImageField(ImageField):
    
    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.max_width = kwargs.pop('max_width', DEFAULT_SIZE[0])
        self.max_height = kwargs.pop('max_height', DEFAULT_SIZE[1])
        self.use_thumbnail_aspect_ratio = kwargs.pop('use_thumbnail_aspect_ratio', False)
        self.background_color = kwargs.pop('background_color', (255, 255, 255, 0))
        super(ResizedImageField, self).__init__(verbose_name, name, **kwargs) 
