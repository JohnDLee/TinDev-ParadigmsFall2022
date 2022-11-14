from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CandidateProfile
from django.http import HttpResponseRedirect
# Create your views here.


def candidate_check(user):
        ''' checks that a user is a part of candidate'''
        return list(user.groups.all())[0].name == 'Candidates'

login_url = '/register/login/'

# decorators to check logged in and correct candidate
@login_required(login_url = login_url)
@user_passes_test(candidate_check, login_url = login_url)
def homepage_view(request):
    ''' Homepage View'''
    
    # there should only be get method for now
    if request.method == 'GET':
        try:
            candidate = CandidateProfile.objects.get(user = request.user)
            # candidate profile exists already, load page.
            context = {'candidate': candidate}
            return render(request, 'candidate/homepage.html', context=context)
        except CandidateProfile.DoesNotExist:
            # candidate profile does not exist, redirect to profile creation.
            return HttpResponseRedirect('/candidate/profile_creation')
        

@login_required(login_url = login_url)
@user_passes_test(candidate_check, login_url = login_url)
def profile_creation_view(request):
    ''' profile creation view'''
    # fill this
    return render(request, 'candidate/profile_creation.html', context = {})