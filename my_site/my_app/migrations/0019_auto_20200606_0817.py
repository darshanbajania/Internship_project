# Generated by Django 3.0.6 on 2020-06-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0018_auto_20200606_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentors',
            name='name',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
