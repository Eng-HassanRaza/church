# Generated by Django 3.1.5 on 2021-02-26 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20210226_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='account_number',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='routing_number',
            field=models.BigIntegerField(),
        ),
    ]