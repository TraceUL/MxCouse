# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-15 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u8bfe\u7a0b\u673a\u6784'),
        ),
    ]