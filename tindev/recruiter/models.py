from django.db import models
from django.conf import settings
from candidate.models import CandidateProfile
# Create your models here.


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField('Name', max_length=200)
    zip_code = models.IntegerField('Zip Code')
    company = models.CharField('Company', max_length=200)

    def __str__(self):
        return f"{self.user.username}"


class JobPost(models.Model):

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    pos_title = models.CharField("Position Title", max_length=200)
    type = models.CharField("Type", max_length=200)
    location = models.CharField("Location", max_length=200)
    des_skills = models.TextField("Desired Skills")
    description = models.TextField("Description")
    company = models.CharField("Company", max_length=200)
    exp_date = models.DateField("Expiration Date")
    status = models.CharField("Status", max_length=200)
    interested_candidates = models.PositiveIntegerField(
        "Interested Candidates", default=0)
    interested_ids = models.TextField("Interested IDs", default="")

    def __str__(self):
        return f"{self.pos_title} ({self.type}) - {self.company}"

    def listify(self):
        return list(map(int, [x for x in self.interested_ids.split(",") if x]))

class Offer(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    yearly_salary = models.PositiveIntegerField("Yearly Salary", default=0)
    due_date = models.DateField("Due Date")
    accepted = models.IntegerField("Accepted", default=0)

    def accept(self):
        self.accepted = 1

    def decline(self):
        self.accepted = -1