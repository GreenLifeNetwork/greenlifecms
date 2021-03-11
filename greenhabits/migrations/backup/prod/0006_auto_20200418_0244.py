# Generated by Django 2.2.6 on 2020-04-18 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('greenhabits', '0005_auto_20200416_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpageindex',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='blogtagpage',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='blogtagpage',
            name='tag',
        ),
        migrations.RenameField(
            model_name='greenhabitpage',
            old_name='summary',
            new_name='suggestion',
        ),
        migrations.DeleteModel(
            name='BlogPage',
        ),
        migrations.DeleteModel(
            name='BlogPageIndex',
        ),
        migrations.DeleteModel(
            name='BlogTagPage',
        ),
    ]