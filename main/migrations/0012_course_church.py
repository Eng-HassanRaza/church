# Generated by Django 3.1.5 on 2021-02-15 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210215_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='church',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_church', to='main.church'),
        ),
    ]
