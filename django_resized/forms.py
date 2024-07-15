import warnings
from io import BytesIO
from PIL import Image, ImageFile, ImageOps, ExifTags
from django.conf import settings
from django.core import checks
from django.core.files.base import ContentFile

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField


DEFAULT_SIZE = getattr(settings, 'DJANGORESIZED_DEFAULT_SIZE', [1920, 1080])
DEFAULT_SCALE = getattr(settings, 'DJANGORESIZED_DEFAULT_SCALE', None)
DEFAULT_QUALITY = getattr(settings, 'DJANGORESIZED_DEFAULT_QUALITY', -1)
DEFAULT_KEEP_META = getattr(settings, 'DJANGORESIZED_DEFAULT_KEEP_META', True)
DEFAULT_FORCE_FORMAT = getattr(settings, 'DJANGORESIZED_DEFAULT_FORCE_FORMAT', None)
DEFAULT_FORMAT_EXTENSIONS = getattr(settings, 'DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS', {})
DEFAULT_NORMALIZE_ROTATION = getattr(settings, 'DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION', True)


def normalize_rotation(image):
    """
    Find orientation header and rotate the actual data instead.
    Adapted from http://stackoverflow.com/a/6218425/723090
    """
    try:
        image._getexif()
    except AttributeError:
        # No exit data; this image is not a jpg and can be skipped
        return image

    for orientation in ExifTags.TAGS.keys():
        # Look for orientation header, stop when found
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    else:
        # No orientation header found, do nothing
        return image
    # Apply the different possible orientations to the data; preserve format
    format = image.format
    exif = image._getexif()
    if exif is None:
        return image
    action_nr = exif.get(orientation, None)
    if action_nr is None:
        # Empty orientation exif data
        return image
    if action_nr in (3, 4):
        image = image.rotate(180, expand=True)
    elif action_nr in (5, 6):
        image = image.rotate(270, expand=True)
    elif action_nr in (7, 8):
        image = image.rotate(90, expand=True)
    if action_nr in (2, 4, 5, 7):
        image = ImageOps.mirror(image)
    image.format = format
    return image

def convert_mode_for_format(to_format, image):
    """
    Converts the mode of image to 'RGB' or 'RGBA' depending on format.
    """
    from_format = image.format.lower()
    to_format = to_format.lower()
    transparent_bg_fill_color = (0,0,0,0)

    if from_format in ('jpg', 'jpeg') and to_format in ('png', 'webp'):
        image = image.convert('RGBA')

    if from_format in ('png', 'webp'):
        image = image.convert('RGBA') if image.mode != 'RGBA' else image
        if to_format in ('jpg', 'jpeg'):
            bg = Image.new('RGBA', image.size, transparent_bg_fill_color)
            image = Image.alpha_composite(bg, image).convert('RGB')

    return image


class ResizedImageFieldFile(ImageField.attr_class):

    def save(self, name, content, save=True):
        content.file.seek(0)
        img = Image.open(content.file)

        if DEFAULT_NORMALIZE_ROTATION:
            img = normalize_rotation(img)

        if self.field.force_format:
            img = convert_mode_for_format(self.field.force_format, img)

        try:
            # Replace ANTIALIAS in PIL 9
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS

        if self.field.size is None:
            self.field.size = img.size

        if self.field.crop:
            thumb = ImageOps.fit(
                img,
                self.field.size,
                resample,
                centering=self.get_centring()
            )
        elif None in self.field.size:
            thumb = img
            if self.field.size[0] is None and self.field.size[1] is not None:
                self.field.scale = self.field.size[1] / img.size[1]
            elif self.field.size[1] is None and self.field.size[0] is not None:
                self.field.scale = self.field.size[0] / img.size[0]
        else:
            img.thumbnail(
                self.field.size,
                resample,
            )
            thumb = img

        if self.field.scale is not None:
            thumb = ImageOps.scale(
                thumb,
                self.field.scale,
                resample
            )

        img_info = img.info
        if not self.field.keep_meta:
            img_info.pop('exif', None)

        ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, thumb.size[0] * thumb.size[1])
        new_content = BytesIO()
        img_format = img.format if self.field.force_format is None else self.field.force_format
        thumb.save(new_content, format=img_format, quality=self.field.quality, **img_info)
        new_content = ContentFile(new_content.getvalue())

        name = self.get_name(name, img_format)
        super().save(name, new_content, save)

    def get_name(self, name, format):
        extensions = Image.registered_extensions()
        extensions = {v: k for k, v in extensions.items()}
        extensions.update({
            "PNG": ".png",  # It uses .apng otherwise
        })
        extensions.update(DEFAULT_FORMAT_EXTENSIONS)
        if format in extensions:
            name = name.rsplit('.', 1)[0] + extensions[format]
        return name

    def get_centring(self):
        vertical = {
            'top': 0,
            'middle': 0.5,
            'bottom': 1,
        }
        horizontal = {
            'left': 0,
            'center': 0.5,
            'right': 1,
        }
        return [
            vertical[self.field.crop[0]],
            horizontal[self.field.crop[1]],
        ]


class ResizedImageField(ImageField):

    attr_class = ResizedImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        # migrate from 0.2.x
        for argname in ('max_width', 'max_height', 'use_thumbnail_aspect_ratio', 'background_color'):
            if argname in kwargs:
                warnings.warn(
                    f'Error: Keyword argument {argname} is deprecated for ResizedImageField, '
                    'see README https://github.com/un1t/django-resized',
                    DeprecationWarning,
                )
                del kwargs[argname]

        self.size = kwargs.pop('size', DEFAULT_SIZE)
        self.scale = kwargs.pop('scale', DEFAULT_SCALE)
        self.crop = kwargs.pop('crop', None)
        self.quality = kwargs.pop('quality', DEFAULT_QUALITY)
        self.keep_meta = kwargs.pop('keep_meta', DEFAULT_KEEP_META)
        self.force_format = kwargs.pop('force_format', DEFAULT_FORCE_FORMAT)
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for custom_kwargs in ('crop', 'size', 'scale', 'quality', 'keep_meta', 'force_format'):
            kwargs[custom_kwargs] = getattr(self, custom_kwargs)
        return name, path, args, kwargs

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_single_dimension_crop(),
            *self._check_webp_quality(),
        ]

    def _check_single_dimension_crop(self):
        if self.crop is not None and self.size is not None and None in self.size:
            return [
                checks.Error(
                    f"{self.__class__.__name__} has both a crop argument and a single dimension size. "
                    "Crop is not possible in that case as the second size dimension is computed from the "
                    "image size and the image will never be cropped.",
                    obj=self,
                    id='django_resized.E100',
                    hint='Remove the crop argument.',
                )
            ]
        else:
            return []

    def _check_webp_quality(self):
        if (
            self.force_format is not None and
            self.force_format.lower() == 'webp' and
            (self.quality is None or self.quality == -1)
        ):
            return [
                checks.Error(
                    f"{self.__class__.__name__} forces the webp format without the quality set.",
                    obj=self,
                    id='django_resized.E101',
                    hint='Set the quality argument.',
                )
            ]
        else:
            return []
