from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.forms import widgets
from .models import RecruiterProfile, JobPost

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
    
    
class JobPostCreationForm(forms.Form):
    
    pos_title = forms.CharField(min_length=1, 
                            max_length=200, 
                            widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "type":"name",
                                                               "placeholder":"Position Title"
                                                               }))
    type = forms.ChoiceField(choices = (("Part Time","Part Time"), ("Full Time","Full Time")), 
                             widget = forms.RadioSelect(attrs={'class':"form-check-input",
                                                               "type": "radio"}))
    location = forms.CharField(min_length=1, 
                            max_length=200, 
                            widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "type":"location",
                                                               "placeholder":"Location (City, State)"
                                                               }))
    des_skills = forms.CharField(widget=widgets.Textarea(attrs={"class": "form-control",
                                                                          "type": "desired_skills",
                                                                          "placeholder": "Desired Skills",
                                                                          "rows" : "3"}))
    description = forms.CharField(widget=widgets.Textarea(attrs={"class": "form-control",
                                                                          "type": "description",
                                                                          "placeholder": "Description",
                                                                          "rows" : "3"}))
    company = forms.CharField(min_length=1,
                                max_length=200,
                                widget=widgets.TextInput(attrs={"class": "form-control",
                                                                "type":"company",
                                                                "placeholder": "Company"}))
    exp_date = forms.DateField(widget=widgets.DateInput(attrs={"class": "form-control",
                                                                "type":"date",
                                                                }))
    status = forms.ChoiceField(choices = (("Active","Active"), ("Inactive","Inactive")), 
                             widget = forms.RadioSelect(attrs={'class':"form-check-input",
                                                               "type": "radio"}))
    
    def save(self, recruiter, commit=True):
        ''' save to recruiter profile '''
        
        post = JobPost(recruiter = recruiter,
                            pos_title = self.cleaned_data['pos_title'],
                            type = self.cleaned_data['type'],
                            location = self.cleaned_data['location'],
                            des_skills = self.cleaned_data['des_skills'],
                            description = self.cleaned_data['description'],
                            company = self.cleaned_data['company'],
                            exp_date = self.cleaned_data['exp_date'],
                            status = self.cleaned_data['status'],
                            interested_candidates = 0)
        post.save()          
    
    def update(self, recruiter, pk, prev_candidates):
        JobPost.objects.filter(recruiter = recruiter, pk = pk).update(
                            pos_title = self.cleaned_data['pos_title'],
                            type = self.cleaned_data['type'],
                            location = self.cleaned_data['location'],
                            des_skills = self.cleaned_data['des_skills'],
                            description = self.cleaned_data['description'],
                            company = self.cleaned_data['company'],
                            exp_date = self.cleaned_data['exp_date'],
                            status = self.cleaned_data['status'],
                            interested_candidates = prev_candidates)
        