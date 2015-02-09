# coding: utf-8
from django.db import models
from django_resized import ResizedImageField

UPLOAD_TO = 'testapp'

class Product(models.Model):
    image1 = ResizedImageField(size=[500, 350], upload_to=UPLOAD_TO, blank=True)
    image2 = ResizedImageField(upload_to=UPLOAD_TO)
    image3 = ResizedImageField(size=[40, 40], crop=['middle', 'center'], upload_to=UPLOAD_TO, blank=True)
    image4 = ResizedImageField(size=[100, 100], crop=['top', 'right'], upload_to=UPLOAD_TO, blank=True)
    image5 = ResizedImageField(size=[500, 350], upload_to=UPLOAD_TO, blank=True, quality=10)
