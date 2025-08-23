# coding: utf-8
from django.db import models
from django_resized import ResizedImageField

UPLOAD_TO = 'tests'


class Product(models.Model):
    image1 = ResizedImageField(size=[500, 350], upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image2 = ResizedImageField(upload_to=UPLOAD_TO, height_field='height', width_field='width')
    image3 = ResizedImageField(size=[40, 40], crop=['middle', 'center'], upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image4 = ResizedImageField(size=[100, 100], crop=['top', 'right'], upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image5 = ResizedImageField(size=[500, 350], upload_to=UPLOAD_TO, blank=True, quality=10, height_field='height', width_field='width')
    image6 = ResizedImageField(size=[500, 350], upload_to=UPLOAD_TO, keep_meta=False, blank=True, quality=10, height_field='height', width_field='width')
    image7 = ResizedImageField(size=[2000, 2000], upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image8 = ResizedImageField(size=[100, 100], crop=['top', 'right'], scale=2.0, upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image9 = ResizedImageField(size=[None, None], scale=0.5, upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image10 = ResizedImageField(size=[500, None], upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image11 = ResizedImageField(size=[None, 350], upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image12 = ResizedImageField(size=None, scale=0.5, upload_to=UPLOAD_TO, blank=True, height_field='height', width_field='width')
    image_force_png = ResizedImageField(size=[500, 350], upload_to=UPLOAD_TO, blank=True, force_format='PNG', height_field='height', width_field='width')

    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
