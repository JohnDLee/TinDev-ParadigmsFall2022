from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.forms import widgets
from .models import RecruiterProfile


class RecruiterProfileCreationForm(forms.Form):
    ''' Form for creating recruiter profile.'''
    
    # attributes
    name = forms.CharField(min_length=1, 
                            max_length=200, 
                            widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "type":"name",
                                                               "placeholder":"Name"
                                                               }))

    zip_code = forms.CharField(widget=widgets.TextInput(attrs={"class": "form-control",
                                                                  "type":"zip_code", 
                                                                  "placeholder":"Zip Code"
                                                                  }),
                                validators = [MinLengthValidator(5, 'Zip Code must be 5 digits.'),
                                                MaxLengthValidator(5, 'Zip Code must be 5 digits.')])

    company = forms.CharField(min_length=1,
                                max_length=200,
                                widget=widgets.TextInput(attrs={"class": "form-control",
                                                                "type":"company",
                                                                "placeholder": "Company"}))
    
    def save(self, req, commit=True):
        ''' save to recruiter profile '''

        recruiter = RecruiterProfile(user = req.user,
                                    name = self.cleaned_data['name'],
                                    zip_code = self.cleaned_data['zip_code'],
                                    company = self.cleaned_data['company'])

        return recruiter