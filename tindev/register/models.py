from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

# Base profile template
class Profile(models.Model):
    name = models.CharField('Name', max_length = 200)
    zip_code = models.IntegerField('Zip Code',
                                   validators = [MinLengthValidator(5, 'Zip Code must be 5 digits.'),
                                                 MaxLengthValidator(5, 'Zip Code must be 5 digits.')
                                                 ]
                                   )
    username = models.CharField('Username', max_length = 200)
    password = models.CharField('Password', max_length = 200)

# Candidate Profile
class CandidateProfile(Profile):
    bio = models.CharField('Profile Bio', max_length = 500)
    skills = models.TextField('Skills')
    github = models.CharField('Github Username', max_length = 200)
    experience = models.PositiveSmallIntegerField('Years Of Experience')
    education = models.TextField('Education')

# Recruiter profile
class RecruiterProfile(Profile):
    company =  models.CharField('Company', max_length = 200)


