# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-13 11:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='\u6807\u9898')),
                ('image', models.ImageField(upload_to='banner/%y%m', verbose_name='\u8f6e\u64ad\u56fe')),
                ('url', models.URLField(max_length=100, verbose_name='\u8bbf\u95ee\u5730\u5740')),
                ('index', models.IntegerField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nick_name', models.CharField(default='', max_length=50, verbose_name='\u6635\u79f0')),
                ('briday', models.DateField(blank=True, null=True, verbose_name='\u751f\u65e5')),
                ('gender', models.CharField(choices=[('male', '\u7537'), ('female', '\u5973')], default='female', max_length=10)),
                ('address', models.CharField(default='', max_length=100)),
                ('mobile', models.CharField(blank=True, max_length=11, null=True)),
                ('image', models.ImageField(default='image/default.png', upload_to='image/%Y%m')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
