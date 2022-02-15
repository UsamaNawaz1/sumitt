from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ("name", "description", "file", "text",
                    "summary", "created", "modified")

admin.site.register(Document, DocumentAdmin)
