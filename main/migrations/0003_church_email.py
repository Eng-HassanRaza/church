# Generated by Django 3.1.5 on 2021-02-06 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210126_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='church',
            name='email',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
