# Generated by Django 3.1.5 on 2021-02-16 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210216_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='present',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]