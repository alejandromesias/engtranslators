# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glosario', '0005_auto_20170724_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='english_entry',
            name='english_related',
            field=models.ManyToManyField(blank=True, related_name='_english_entry_english_related_+', to='glosario.English_Entry'),
        ),
        migrations.AlterField(
            model_name='spanish_entry',
            name='spanish_included',
            field=models.ManyToManyField(blank=True, related_name='spanish_main', to='glosario.Spanish_Entry'),
        ),
    ]
