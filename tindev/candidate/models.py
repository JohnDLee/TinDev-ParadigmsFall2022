from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.conf import settings

# Create your models here.


class CandidateProfile(models.Model):
    # unassign these values
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField('Name', max_length=200)
    zip_code = models.IntegerField('Zip Code',
                                   validators=[MinLengthValidator(5, 'Zip Code must be 5 digits.'),
                                               MaxLengthValidator(
                                       5, 'Zip Code must be 5 digits.')
                                   ]
                                   )
    bio = models.CharField('Profile Bio', max_length=500)
    skills = models.TextField('Skills')
    github = models.CharField('Github Username', max_length=200)
    experience = models.IntegerField('Years Of Experience')
    education = models.TextField('Education')
    uninterested_ids = models.TextField('Uninterested IDs', default='')

    def __str__(self):
        return f"{self.user.username}"