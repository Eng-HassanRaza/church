# Generated by Django 3.1.5 on 2021-02-26 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_remove_church_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='state_abbrev',
            field=models.CharField(max_length=2),
        ),
    ]
