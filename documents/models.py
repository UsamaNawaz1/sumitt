from django.db import models

from django.contrib.auth.models import User
from datetime import datetime


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    max_sentences = models.IntegerField(default=10)
    start_scan_page = models.IntegerField(null=True)
    end_scan_page = models.IntegerField(null=True)
    text = models.TextField(default="", blank=True)
    summary = models.TextField(default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return format(self.name)

class Usage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    current_month = models.CharField(max_length=5, null=True)

    def __str__(self):
        return format(self.user)
