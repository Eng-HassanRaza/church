# Generated by Django 3.1.5 on 2021-02-14 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_prayerrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='prayerrequest',
            name='church',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='member_church', to='main.church'),
            preserve_default=False,
        ),
    ]