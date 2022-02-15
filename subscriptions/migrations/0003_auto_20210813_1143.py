# Generated by Django 3.2.4 on 2021-08-13 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_alter_plan_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='current_period_end',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='use_count',
            field=models.IntegerField(default=0),
        ),
    ]