# Generated by Django 3.2.4 on 2021-08-13 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_alter_customer_current_period_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='use_count',
        ),
    ]
