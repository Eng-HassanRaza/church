# Generated by Django 3.1.5 on 2021-02-22 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20210222_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minutes',
            name='recorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minutes_recorder', to=settings.AUTH_USER_MODEL),
        ),
    ]
