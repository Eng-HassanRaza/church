# Generated by Django 3.1.5 on 2021-03-07 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_payment_detials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
