# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.views.generic import CreateView
# from django.contrib.auth.models import User
# from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
# from .models import Plan, Customer, Campaign, Coupon, Setting, LinkedinProfile, Connection
# from django.contrib.admin.widgets import AdminDateWidget
# # from django.forms.extras.widgets import SelectDateWidget

# class LinkedinProfileForm(forms.ModelForm):
#     class Meta:
#         model = LinkedinProfile
#         fields = ('fullname', 'linkedin_email', 'password')
    
#     def __init__(self, *args, **kwargs):
#         super(LinkedinProfileForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Field('password', type="password"),
#             # ButtonHolder(
#             #     Submit('submit', 'Submit', css_class='button white')
#             # )
#         )

# class CampaignForm(forms.ModelForm):
#     # schedule = forms.DateField(widget=AdminDateWidget())
#     # schedule = forms.DateField(widget=SelectDateWidget)

#     class Meta:
#         model = Campaign
#         fields = ('subject', 'text', 'schedule')
#         # widgets = {'schedule': AdminDateWidget()}
    
#     def __init__(self, *args, **kwargs):
#         super(CampaignForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         # self.helper.layout = Layout(
#             # Div(
#             #     Field('schedule'), css_class="datepicker"
#             #     # Field('schedule', css_class='datepicker')
#             # ),            
#             # Field('schedule', css_class='datepicker')
#             # Field('schedule', wrapper_class='datepicker')
#             # Field('password', type="password"),
#             # ButtonHolder(
#             #     Submit('submit', 'Submit', css_class='button white')
#             # )
#         # )
