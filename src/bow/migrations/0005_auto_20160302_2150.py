# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bow', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ISBN',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='rents',
            name='ISBN',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='rents',
            name='bookid',
            field=models.ForeignKey(to='bow.Book'),
        ),
    ]
