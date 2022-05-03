#!/usr/bin/env python
import os
import sys
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

settings.configure(

    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    INSTALLED_APPS = (
        'django_resized.tests',
        'django_resized',
    ),
    MIDDLEWARE_CLASSES = [],
    DJANGORESIZED_DEFAULT_SIZE = [400, 300],
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media'),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv[:1] + ['test'] + sys.argv[1:])
