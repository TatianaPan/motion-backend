# Generated by Django 2.2.2 on 2019-06-13 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='created'),
        ),
    ]
