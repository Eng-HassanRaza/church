# Generated by Django 3.1.5 on 2021-02-22 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20210222_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountspayable',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_accountspayable', to='main.vendor'),
        ),
        migrations.AlterField(
            model_name='accountsreceivable',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_accountspayable', to='main.customer'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_transaction', to='main.accounts'),
        ),
    ]
