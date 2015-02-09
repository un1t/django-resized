import os
from PIL import Image, ImageFile, ImageOps

try:
    from io import BytesIO as StringIO # python3
except ImportError:
    from StringIO import StringIO # python2

from django.conf import settings
from django.core.files.base import ContentFile

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField


DEFAULT_SIZE = getattr(settings, 'DJANGORESIZED_DEFAULT_SIZE', [1920, 1080])
DEFAULT_QUALITY = getattr(settings, 'DJANGORESIZED_DEFAULT_QUALITY', 0)


class ResizedImageFieldFile(ImageField.attr_class):

    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)
        img = Image.open(content.file)
        if self.field.crop:
            thumb = ImageOps.fit(
                img,
                (self.field.width, self.field.height),
                Image.ANTIALIAS,
                centering=self.get_centring()
            )
        else:
            img.thumbnail(
                (self.field.width, self.field.height),
                Image.ANTIALIAS,
            )
            thumb = img

        ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, thumb.size[0] * thumb.size[1])
        thumb.save(new_content, format=img.format, quality=self.field.quality, **img.info)
        new_content = ContentFile(new_content.getvalue())

        super(ResizedImageFieldFile, self).save(name, new_content, save)

    def get_centring(self):
        return [
            {
                'top': 0,
                'middle': 0.5,
                'bottom': 1,
            }[self.field.crop[0]],
            {
                'left': 0,
                'center': 0.5,
                'right': 1,
            }[self.field.crop[1]],
        ]


class ResizedImageField(ImageField):

    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.width = kwargs.pop('width', DEFAULT_SIZE[0])
        self.height = kwargs.pop('height', DEFAULT_SIZE[1])
        self.crop = kwargs.pop('crop', None)
        self.quality = kwargs.pop('quality', DEFAULT_QUALITY)
        super(ResizedImageField, self).__init__(verbose_name, name, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    rules = [
        (
            (ResizedImageField,),
            [],
            {
                "width": ["width", {'default': DEFAULT_SIZE[0]}],
                "height": ["height", {'default': DEFAULT_SIZE[1]}],
                "crop": ["crop", {'default': False}],
                "quality": ["quality", {'default': DEFAULT_QUALITY}],
            },
        )
    ]
    add_introspection_rules(rules, ["^django_resized\.forms\.ResizedImageField"])

