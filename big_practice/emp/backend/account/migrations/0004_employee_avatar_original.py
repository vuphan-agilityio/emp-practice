# Generated by Django 2.0 on 2018-12-20 10:08

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20181210_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='avatar_original',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=''),
        ),
    ]
