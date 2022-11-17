from django.db import models
from django.conf import settings
# Create your models here.

class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField('Name', max_length = 200)
    zip_code = models.IntegerField('Zip Code')
    company =  models.CharField('Company', max_length = 200)
    
    def __str__(self):
        return f"{self.user.username}"