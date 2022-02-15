from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django import forms
# from document.core.models import Document
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from documents.models import Document


# class DocumentForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     description = forms.CharField(widget=forms.Textarea)
#     file = forms.FileField()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'description', 'file', 'start_scan_page',
                  'end_scan_page', 'max_sentences')
