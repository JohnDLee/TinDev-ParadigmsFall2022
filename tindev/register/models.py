from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.



# class CandidateProfile(User):
#     # unassign these values
#     name = models.CharField('Name', max_length = 200)
#     zip_code = models.IntegerField('Zip Code',
#                                    validators = [MinLengthValidator(5, 'Zip Code must be 5 digits.'),
#                                                  MaxLengthValidator(5, 'Zip Code must be 5 digits.')
#                                                  ]
#                                    )
#     bio = models.CharField('Profile Bio', max_length = 500)
#     skills = models.TextField('Skills')
#     github = models.CharField('Github Username', max_length = 200)
#     experience = models.PositiveSmallIntegerField('Years Of Experience')
#     education = models.TextField('Education')
    
# class RecruiterProfile(User):
#     name = models.CharField('Name', max_length = 200)
#     zip_code = models.IntegerField('Zip Code',
#                                    validators = [MinLengthValidator(5, 'Zip Code must be 5 digits.'),
#                                                  MaxLengthValidator(5, 'Zip Code must be 5 digits.')
#                                                  ]
#                                    )
#     company =  models.CharField('Company', max_length = 200)