# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bow', '0002_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.AddField(
            model_name='book',
            name='imageurl',
            field=models.CharField(default=b'../images/TheSecretLogo.jpg', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='ISBN',
            field=models.CharField(default=b'12344', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rents',
            name='ISBN',
            field=models.CharField(default=b'12344', max_length=20),
            preserve_default=False,
        ),
    ]
