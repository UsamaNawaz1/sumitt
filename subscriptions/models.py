from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime

class Plan(models.Model):
    title = models.CharField(max_length=255)
    # text = models.TextField()
    monthly_summaries = models.IntegerField()
    # price = models.IntegerField(default=0)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    stripe_id = models.CharField(max_length=255)
    # premium = models.BooleanField(default=True)

    def __str__(self):
        return format(self.title)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(default="",max_length=255)
    stripe_subscription_id = models.CharField(default="",max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    current_period_end = models.CharField(default="", max_length=50)
    # plan = models.ForeignKey(Plan)

    def __str__(self):
        return format(self.user)

class Coupon(models.Model):
    name = models.CharField(max_length=50, default="")
    code = models.CharField(max_length=50, default="")
    discount = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return format(self.name)


class Setting(models.Model):
    stripe_api_key = models.CharField(max_length=250, default="")
    publishable_key = models.CharField(max_length=250, default="")

    def __str__(self):
        return format(self.stripe_api_key)


