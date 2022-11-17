from django import forms
from django.contrib.auth.models import User
from .models import CandidateProfile
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.forms import widgets


class CustomCandidateCreationForm(forms.Form):
    ''' Form for creating candidate profile.'''

    # attributes
    name = forms.CharField(max_length=200,
                           widget=widgets.TextInput(attrs={"class": "form-control",
                                                           "type": "name",
                                                           "placeholder": "Name"}))
    zip_code = forms.CharField(widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "type": "zip_code",
                                                               "placeholder": "Zip Code"}),
                               validators=[MinLengthValidator(5, 'Zip Code must be 5 digits.'),
                                           MaxLengthValidator(5, 'Zip Code must be 5 digits.')])
    bio = forms.CharField(max_length=500, widget=widgets.TextInput(attrs={"class": "form-control",
                                                                          "type": "bio",
                                                                          "placeholder": "Profile Bio"}))
    skills = forms.CharField(widget=widgets.TextInput(attrs={"class": "form-control",
                                                             "type": "skills",
                                                             "placeholder": "Skills"
                                                             }))
    github = forms.CharField(max_length=200,
                             widget=widgets.TextInput(attrs={"class": "form-control",
                                                             "type": "github",
                                                             "placeholder": "Github"
                                                             }))
    experience = forms.IntegerField(widget=widgets.TextInput(attrs={"class": "form-control",
                                                                    "type": "experience",
                                                                    "placeholder": "Years of experience"
                                                                    }))
    education = forms.CharField(widget=widgets.TextInput(attrs={"class": "form-control",
                                                                "type": "education",
                                                                "placeholder": "Education"
                                                                }))

    def save(self, req, commit=True):
        # save a candidate to a profile
        candidate = CandidateProfile(user=req.user,
                                     name=self.cleaned_data['name'],
                                     zip_code=self.cleaned_data['zip_code'],
                                     bio=self.cleaned_data['bio'],
                                     skills=self.cleaned_data['skills'],
                                     github=self.cleaned_data['github'],
                                     experience=self.cleaned_data['experience'],
                                     education=self.cleaned_data['education'])
        return candidate
