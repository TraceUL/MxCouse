# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-19 02:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20171116_0329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': '\u8bfe\u7a0b', 'verbose_name_plural': '\u8bfe\u7a0b'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': '\u7ae0\u8282', 'verbose_name_plural': '\u7ae0\u8282'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': '\u89c6\u9891', 'verbose_name_plural': '\u89c6\u9891'},
        ),
    ]
