# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 21:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glosario', '0006_auto_20170925_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'permissions': (('can_create_chapter', 'Can create chapter'),)},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': (('can_write_comment', 'Can write comment'),)},
        ),
        migrations.AlterModelOptions(
            name='english_entry',
            options={'permissions': (('can_create_entry', 'Can create entry'), ('can_edit_entry', 'Can edit entry'))},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'permissions': (('can_create_theme', 'Can create theme'),)},
        ),
    ]
