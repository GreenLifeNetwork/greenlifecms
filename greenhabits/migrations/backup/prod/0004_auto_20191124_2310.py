# Generated by Django 2.2.6 on 2019-11-24 23:10

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('greenhabits', '0003_auto_20191102_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='greenhabitpage',
            name='link',
        ),
        migrations.AddField(
            model_name='greenhabitpage',
            name='links',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Call to actions or details regarding suggestion'),
        ),
    ]
