# Generated by Django 3.1.5 on 2021-02-16 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210216_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_registration', to=settings.AUTH_USER_MODEL),
        ),
    ]
