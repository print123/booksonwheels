# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bow', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ISBN',
            field=models.ForeignKey(related_name='order_ISBN', default=0, to='bow.Book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rents',
            name='ISBN',
            field=models.ForeignKey(related_name='rent_ISBN', default=0, to='bow.Book'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='bookid',
            field=models.ForeignKey(related_name='order_bookid', to='bow.Book'),
        ),
        migrations.AlterField(
            model_name='rents',
            name='bookid',
            field=models.ForeignKey(related_name='rent_bookid', to='bow.Book'),
        ),
    ]
