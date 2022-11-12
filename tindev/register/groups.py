from django.contrib.auth.models import Group, Permission

# construct groups for permissions later
recruiter_group, created = Group.objects.get_or_create(name ='Recruiters')
candidate_group, created = Group.objects.get_or_create(name ='Candidates')