# Generated by Django 3.1.5 on 2021-02-22 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20210222_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='fund_tag',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='user_allowed',
        ),
        migrations.RemoveField(
            model_name='accountspayable',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='accountsreceivable',
            name='customer',
        ),
        migrations.DeleteModel(
            name='CurrentLiabilities',
        ),
        migrations.DeleteModel(
            name='FixedAssets',
        ),
        migrations.DeleteModel(
            name='LongTermLiabilities',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='account',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='expense_transaction',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='income_transaction',
        ),
        migrations.DeleteModel(
            name='Accounts',
        ),
        migrations.DeleteModel(
            name='AccountsPayable',
        ),
        migrations.DeleteModel(
            name='AccountsReceivable',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Expense',
        ),
        migrations.DeleteModel(
            name='Funds',
        ),
        migrations.DeleteModel(
            name='Income',
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]
