# Generated by Django 3.0.6 on 2020-06-11 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0030_auto_20200611_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='text',
            field=models.TextField(default='no text', max_length=10000),
        ),
    ]
