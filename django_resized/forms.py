from PIL import Image, ImageOps
from StringIO import StringIO

from django.conf import settings
from django.core.files.base import ContentFile

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField


DEFAULT_SIZE = getattr(settings, 'DJANGORESIZED_DEFAULT_SIZE', [1920, 1080])
DEFAULT_COLOR = (255, 255, 255, 0)
DEFAULT_FORMAT = 'jpeg'


class ResizedImageFieldFile(ImageField.attr_class):

    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)
        thumb = ImageOps.fit(
            Image.open(content.file),
            (self.field.width, self.field.height),
            Image.ANTIALIAS
        )

        thumb.save(new_content, format=self.field.format.upper(), **thumb.info)

        new_content = ContentFile(new_content.getvalue())

        super(ResizedImageFieldFile, self).save(name, new_content, save)


class ResizedImageField(ImageField):

    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.width = kwargs.pop('width', DEFAULT_SIZE[0])
        self.height = kwargs.pop('height', DEFAULT_SIZE[1])
        self.format = kwargs.pop('format', DEFAULT_FORMAT)
        super(ResizedImageField, self).__init__(verbose_name, name, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
    rules = [
        (
            (ResizedImageField,),
            [],
            {
                "width": ["width", {'default': DEFAULT_SIZE[0]}],
                "height": ["height", {'default': DEFAULT_SIZE[1]}],
                "format": ["format", {'default': DEFAULT_FORMAT}],
            },
        )
    ]
    add_introspection_rules(rules, ["^django_resized\.forms\.ResizedImageField"])
except ImportError:
    pass
