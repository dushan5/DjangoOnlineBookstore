# Generated by Django 2.2.1 on 2019-06-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190617_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='latest',
            field=models.BooleanField(default=False),
        ),
    ]
