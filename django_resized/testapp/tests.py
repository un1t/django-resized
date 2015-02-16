# coding: utf-8
import Image
import os
import shutil
from django.conf import settings
from django.test import TestCase
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image
from .models import Product


class ResizeTest(TestCase):

    def tearDown(self):
        dirname = os.path.join(settings.MEDIA_ROOT, 'testapp')
        if os.path.exists(dirname):
            shutil.rmtree(dirname)

    def test_resize_to_specified_size(self):
        product = Product.objects.create(
            image1=File(open('media/big.jpg')),
        )
        im1 = Image.open(product.image1.path)
        self.assertEquals(im1.size, (466, 350))

    def test_resizes_settings_default(self):
        product = Product.objects.create(
            image2=File(open('media/big.jpg')),
        )
        im2 = Image.open(product.image2.path)
        self.assertEquals(im2.size, (400, 300))

    def test_resize_crop_center(self):
        product = Product.objects.create(
            image3=File(open('media/big.jpg')),
        )
        im3 = Image.open(product.image3.path)
        self.assertEquals(im3.size, (40, 40))


    def test_resize_crop_right(self):
        product = Product.objects.create(
            image4=File(open('media/big.jpg')),
        )
        im4 = Image.open(product.image4.path)
        self.assertEquals(im4.size, (100, 100))

    def test_resize_with_quality(self):
        product = Product.objects.create(
            image1=File(open('media/big.jpg')),
            image5=File(open('media/big.jpg')),
        )
        self.assertTrue(os.path.getsize(product.image1.path) > os.path.getsize(product.image5.path))

    def test_keep_exif(self):
        product = Product.objects.create(
            image1=File(open('media/exif.jpg')),
        )
        im1 = Image.open(product.image1.path)
        self.assertTrue(self.has_exif(product.image1.path))

    def test_remove_exif(self):
        product = Product.objects.create(
            image6=File(open('media/exif.jpg')),
        )
        im6 = Image.open(product.image6.path)
        self.assertFalse(self.has_exif(product.image6.path))

    def has_exif(self, filename):
        return bool(Image.open(filename)._getexif())

    def test_resize_without_upscale(self):
        product = Product.objects.create(
            image7=File(open('media/big.jpg')),
        )
        im7 = Image.open(product.image7.path)
        self.assertEquals(im7.size, (604, 453))

