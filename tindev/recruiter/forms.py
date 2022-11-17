from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
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

    zip_code = forms.IntegerField(widget=widgets.NumberInput(attrs={"class": "form-control",
                                                                  "type":"zip_code", 
                                                                  "placeholder":"Zip Code"
                                                                  }),
                                )

    company = forms.CharField(min_length=1,
                                max_length=200,
                                widget=widgets.TextInput(attrs={"class": "form-control",
                                                                "type":"company",
                                                                "placeholder": "Company"}))
    
    def clean_zip_code(self):
        ''' check that zipcode has 5 digits'''
        zip_code = self.cleaned_data['zip_code']
        if len(str(zip_code)) != 5:
            raise ValidationError("Zip code must contain exactly 5 digits.")
        return zip_code
        
    
    def save(self, req, commit=True):
        ''' save to recruiter profile '''

        recruiter = RecruiterProfile(user = req.user,
                                    name = self.cleaned_data['name'],
                                    zip_code = self.cleaned_data['zip_code'],
                                    company = self.cleaned_data['company'])

        return recruiter