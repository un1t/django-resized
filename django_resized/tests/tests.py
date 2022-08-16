# coding: utf-8
import os
import shutil
from PIL import Image

from django.conf import settings
from django.core import checks
from django.test import TestCase
from django.core.files import File

from django_resized import ResizedImageField
from .models import Product


class ResizeTest(TestCase):

    def tearDown(self):
        dirname = os.path.join(settings.MEDIA_ROOT, 'tests')
        if os.path.exists(dirname):
            shutil.rmtree(dirname)

    def test_resize_to_specified_size(self):
        product = Product.objects.create(
            image1=File(open('media/big.jpg', 'rb')),
        )
        im1 = Image.open(product.image1.path)
        self.assertEqual(im1.size, (467, 350))

    def test_resizes_settings_default(self):
        product = Product.objects.create(
            image2=File(open('media/big.jpg', 'rb')),
        )
        im2 = Image.open(product.image2.path)
        self.assertEqual(im2.size, (400, 300))

    def test_resize_crop_center(self):
        product = Product.objects.create(
            image3=File(open('media/big.jpg', 'rb')),
        )
        im3 = Image.open(product.image3.path)
        self.assertEqual(im3.size, (40, 40))

    def test_resize_crop_right(self):
        product = Product.objects.create(
            image4=File(open('media/big.jpg', 'rb')),
        )
        im4 = Image.open(product.image4.path)
        self.assertEqual(im4.size, (100, 100))

    def test_resize_with_quality(self):
        product = Product.objects.create(
            image1=File(open('media/big.jpg', 'rb')),
            image5=File(open('media/big.jpg', 'rb')),
        )
        self.assertTrue(os.path.getsize(product.image1.path) > os.path.getsize(product.image5.path))

    def test_keep_exif(self):
        product = Product.objects.create(
            image1=File(open('media/exif.jpg', 'rb')),
        )
        self.assertTrue(self.has_exif(product.image1.path))

    def test_remove_exif(self):
        product = Product.objects.create(
            image6=File(open('media/exif.jpg', 'rb')),
        )
        self.assertFalse(self.has_exif(product.image6.path))

    def has_exif(self, filename):
        return bool(Image.open(filename)._getexif())

    def test_resize_without_upscale(self):
        product = Product.objects.create(
            image7=File(open('media/big.jpg', 'rb')),
        )
        im7 = Image.open(product.image7.path)
        self.assertEqual(im7.size, (604, 453))

    def test_scale_set_size(self):
        product = Product.objects.create(
            image8=File(open('media/big.jpg', 'rb')),
        )
        im8 = Image.open(product.image8.path)
        self.assertEqual(im8.size, (200, 200))

    def test_scale_default_size(self):
        product = Product.objects.create(
            image9=File(open('media/big.jpg', 'rb')),
        )
        im9 = Image.open(product.image9.path)
        self.assertEqual(im9.size, (302, 226))

    def test_scale_x(self):
        product = Product.objects.create(
            image10=File(open('media/big.jpg', 'rb')),
        )
        im10 = Image.open(product.image10.path)
        self.assertEqual(im10.size, (500, 375))

    def test_scale_y(self):
        product = Product.objects.create(
            image11=File(open('media/big.jpg', 'rb')),
        )
        im11 = Image.open(product.image11.path)
        self.assertEqual(im11.size, (467, 350))

    def test_scale_no_size(self):
        product = Product.objects.create(
            image12=File(open('media/big.jpg', 'rb')),
        )
        im12 = Image.open(product.image12.path)
        self.assertEqual(im12.size, (302, 226))

    def test_force_format(self):
        product = Product.objects.create(
            image_force_png=File(open('media/big.jpg', 'rb')),
        )
        image_force_png = Image.open(product.image_force_png.path)
        self.assertEqual(image_force_png.format, 'PNG')
        self.assertTrue(image_force_png.filename.endswith('.png'))

    def test_crop_single_size_dimension(self):
        self.assertIsInstance(
            ResizedImageField(size=[None, 350], crop=['top', 'right'], blank=True, name='foo').check()[0],
            checks.Error
        )


class ResizeFieldTest(TestCase):

    def test_clone(self):
        field = ResizedImageField(size=[500, 350], keep_meta=False, crop=['top', 'left'], quality=10)
        clone = field.clone()
        self.assertListEqual(clone.size, field.size)
        self.assertListEqual(clone.crop, field.crop)
        self.assertEqual(clone.keep_meta, field.keep_meta)
        self.assertEqual(clone.quality, field.quality)
