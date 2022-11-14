from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.conf import settings
# Create your models here.

class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField('Name', max_length = 200)
    zip_code = models.IntegerField('Zip Code',
                                   validators = [MinLengthValidator(5, 'Zip Code must be 5 digits.'),
                                                 MaxLengthValidator(5, 'Zip Code must be 5 digits.')
                                                 ]
                                   )
    company =  models.CharField('Company', max_length = 200)