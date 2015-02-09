# coding: utf-8
from django.db import models
from django_resized import ResizedImageField


class Product(models.Model):
    image1 = ResizedImageField(width=500, height=350, upload_to='testapp', blank=True, quality=10)
    image2 = ResizedImageField(upload_to='testapp')
    image3 = ResizedImageField(width=40, height=40, crop=['middle', 'center'], upload_to='testapp', blank=True)
    image4 = ResizedImageField(width=100, height=100, crop=['top', 'right'], upload_to='testapp', blank=True)
    # image4 = ResizedImageField(width=40, height=40, crop=True, upload_to='testapp', blank=True)
    # image5 = ResizedImageField(width=40, height=40, crop=True, upload_to='testapp', blank=True)
