from django.db import models
from django.conf import settings
from candidate.models import CandidateProfile
from datetime import date
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

    def expire(self):
        if date.today() > self.exp_date:
            self.status = "Inactive"
            self.save()
        return True

    def listify(self):
        # get candidates
        candidates = CandidateProfile.objects.get_queryset()
        # add compat scores
        for c in candidates:
            c.compatability_score = calculateCompatScore(c, self)
            c.save()
        # sort them by sorting algorithm
        #candidates = sorted(candidates, key=lambda x: calculateCompatScore(x, self), reverse=True)
        candidates = sorted(
            candidates, key=lambda x: x.compatability_score, reverse=True)
        # identify interested candidates
        interested = list(
            map(int, [x for x in self.interested_ids.split(",") if x]))
        # filter sorted list to only interested candidates
        candidates = filter(lambda x: x.id in interested, candidates)
        return candidates


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

    def is_expired(self):
        return date.today() > self.due_date

# functions for calculating compatibility score


def bioCompare(candidate, posting):
    numerator = 0
    denominator = 0

    # handle extra chars at end of words, like commas and periods
    for index, item in enumerate(posting):
        if not item[-1].isalpha():
            posting[index] = item[:-1]

    # see how similar candidate bio is to job descrip
    for word in candidate:
        if not word[-1].isalpha():
            word = word[:-1]
        if not len(word):
            continue
        if word in posting:
            numerator += 1
        denominator += 1

    result = numerator/denominator
    return 2*result


def skillCompare(candidate, posting):
    numerator = 0
    denominator = 0

    # handle extra chars at end of words, like commas and periods
    for index, item in enumerate(candidate):
        if not item[-1].isalpha():
            candidate[index] = item[:-1]

    # find number of candidate skills in required skills
    for skill in posting:
        if not skill[-1].isalpha():
            skill = skill[:-1]
        if not len(skill):
            continue
        if skill in candidate:
            numerator += 1
        denominator += 1

    result = numerator/denominator
    return result


def expCheck(canExp, jobType):
    if jobType == "full":
        if canExp > 10:
            return 1
        elif canExp > 5:
            return .5
    else:
        if canExp >= 3:
            return 1
        else:
            return .5


def calculateCompatScore(candidate, job):
    compScore = 0

    canBio = candidate.bio.lower().split()
    canSkills = candidate.skills.lower().split()
    canExp = candidate.experience

    jobDescrip = job.description.lower().split()
    jobSkills = job.des_skills.lower().split()
    jobType = job.type

    compScore += .33*bioCompare(canBio, jobDescrip)
    compScore += .33*skillCompare(canSkills, jobSkills)
    compScore += .34*expCheck(canExp, jobType)

    compScore *= 100

    if compScore > 100:
        compScore = 100

    return round(compScore, 2)
