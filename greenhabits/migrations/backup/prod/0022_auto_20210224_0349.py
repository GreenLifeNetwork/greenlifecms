# Generated by Django 2.2.5 on 2021-02-24 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greenhabits', '0021_auto_20210224_0344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='greenhabitpage',
            old_name='link',
            new_name='other_link',
        ),
        migrations.RemoveField(
            model_name='greenhabitpage',
            name='links',
        ),
    ]
