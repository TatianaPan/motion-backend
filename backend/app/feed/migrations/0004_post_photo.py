# Generated by Django 2.2.2 on 2019-06-21 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='posts'),
        ),
    ]
