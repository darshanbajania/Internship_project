# Generated by Django 3.0.6 on 2020-06-11 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0028_auto_20200611_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='category',
            field=models.CharField(default='no text', max_length=500),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='summary',
            field=models.CharField(default='no summary', max_length=4000),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(default='no title', max_length=200),
        ),
    ]
