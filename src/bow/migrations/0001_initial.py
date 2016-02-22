# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bookid', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.CharField(max_length=100)),
                ('actual_price', models.DecimalField(max_digits=8, decimal_places=4)),
                ('ISBN', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=b'img')),
                ('genre', models.CharField(max_length=20)),
                ('dosell', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('summary', models.CharField(max_length=200)),
                ('rating', models.DecimalField(max_digits=1, decimal_places=1)),
                ('title', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.AutoField(serialize=False, primary_key=True)),
                ('date_of_order', models.DateTimeField(auto_now_add=True)),
                ('bookid', models.ForeignKey(to='bow.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentid', models.AutoField(serialize=False, primary_key=True)),
                ('mode', models.CharField(max_length=2)),
                ('ispending', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_issue', models.DateTimeField(auto_now_add=True)),
                ('date_of_return', models.DateTimeField()),
                ('bookid', models.ForeignKey(to='bow.Book')),
                ('paymentid', models.ForeignKey(to='bow.Payment')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('contact_no', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('address', models.CharField(max_length=500, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ISBN', models.CharField(max_length=20)),
                ('userid', models.ForeignKey(to='bow.User')),
            ],
        ),
        migrations.AddField(
            model_name='rents',
            name='userid',
            field=models.ForeignKey(to='bow.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='paymentid',
            field=models.ForeignKey(to='bow.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='userid',
            field=models.ForeignKey(to='bow.User'),
        ),
        migrations.AddField(
            model_name='book',
            name='owner_id',
            field=models.ForeignKey(to='bow.User'),
        ),
    ]
