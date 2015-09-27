# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wordplay.responses.models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open_date', models.DateField()),
                ('close_date', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(verbose_name=b'Temperature (1-10)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('word', models.CharField(max_length=32, verbose_name=b"One word to describe how you're feeling", validators=[django.core.validators.RegexValidator(regex=b"^[A-Za-z0-9'-]+$", message=b'Please enter a single word with alphanumeric characters only.', code=b'Invalid Word')])),
                ('responded_at', models.DateTimeField(auto_now=True)),
                ('collector', models.ForeignKey(to='responses.Collector')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.CharField(default=wordplay.responses.models.make_uuid, max_length=8, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=8, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='survey',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='responder',
            field=models.ForeignKey(to='responses.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collector',
            name='survey',
            field=models.ForeignKey(to='responses.Survey'),
            preserve_default=True,
        ),
    ]
