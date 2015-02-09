# coding: utf-8
from django.db import models
from django_resized import ResizedImageField


class Product(models.Model):
    image1 = ResizedImageField(max_width=40, max_height=30, upload_to='testapp', blank=True)
    image2 = ResizedImageField(upload_to='testapp')
    image3 = ResizedImageField(max_width=400, max_height=100, upload_to='testapp', blank=True)
    image4 = ResizedImageField(use_thumbnail_aspect_ratio=True, max_width=40, max_height=40, upload_to='testapp', blank=True)
    image5 = ResizedImageField(use_thumbnail_aspect_ratio=False, max_width=40, max_height=40, upload_to='testapp', blank=True)
