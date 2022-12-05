from django.contrib import admin
from .models import RecruiterProfile, JobPost, Offer
# Register your models here.

admin.site.register(RecruiterProfile)
admin.site.register(JobPost)
admin.site.register(Offer)