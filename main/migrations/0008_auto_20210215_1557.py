# Generated by Django 3.1.5 on 2021-02-15 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210214_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='members',
            name='city',
        ),
        migrations.RemoveField(
            model_name='members',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='members',
            name='state_abbrev',
        ),
        migrations.RemoveField(
            model_name='members',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='members',
            name='street_address_line_2',
        ),
        migrations.RemoveField(
            model_name='members',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='state_abbrev',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='street_address',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='street_address_line_2',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zip_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='members',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
