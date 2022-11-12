from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.forms import widgets
from .groups import candidate_group, recruiter_group


class CustomUserCreationForm(forms.Form):
    ''' Custom User formatted form for creating a user.'''
    
    # attributes
    username = forms.CharField(min_length=4, 
                               max_length=150, 
                               widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "type":"username",
                                                               "placeholder":"Username"
                                                               }),
                               validators=[ASCIIUsernameValidator()])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                  "type":"password", 
                                                                  "placeholder":"Password"
                                                                  }),
                                validators=[MinLengthValidator(8,
                                                              message="Password must be at least 8 characters"),
                                            ])   
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password", "placeholder": "Password"}))
    profile_type = forms.ChoiceField(choices = (("Candidate","Candidate"), ("Recruiter","Recruiter")), widget = forms.RadioSelect(attrs={'class':"form-check-input", "type": "radio"}))

    def clean_username(self):
        ''' minor extra validation of the username '''
        username = self.cleaned_data['username'].lower()
        # avoid dupes
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        # no spaces
        if ' ' in username or '\t' in username:
            raise ValidationError("Username cannot contain spaces.")
        
        return username

    def clean_password2(self):
        ''' double check passwords '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        ''' save as a particular group '''
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
            
        )
        # select which group
        if self.cleaned_data['profile_type'] == 'Candidate':
            user.groups.add(candidate_group)
        elif self.cleaned_data['profile_type'] == 'Recruiter':
            user.groups.add(recruiter_group)
            
        return user