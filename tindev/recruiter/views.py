from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import RecruiterProfile
from django.http import HttpResponseRedirect
# Create your views here.


def recruiter_check(user):
        ''' checks that a user is a part of candidate'''
        return list(user.groups.all())[0].name == 'Recruiters'

login_url = '/register/login/'

# decorators to check logged in and correct candidate
@login_required(login_url = login_url)
@user_passes_test(recruiter_check, login_url = login_url)
def homepage_view(request):
    ''' Homepage View'''
    
    # there should only be get method for now
    if request.method == 'GET':
        try:
            recruiter = RecruiterProfile.objects.get(user = request.user)
            # recruiter profile exists already, load page.
            context = {'recruiter': recruiter}
            return render(request, 'recruiter/homepage.html', context=context)
        except RecruiterProfile.DoesNotExist:
            # recruiter profile does not exist, redirect to profile creation.
            return HttpResponseRedirect('/recruiter/profile_creation')
        

@login_required(login_url = login_url)
@user_passes_test(recruiter_check, login_url = login_url)
def profile_creation_view(request):
    ''' profile creation view'''
    # fill this
    return render(request, 'recruiter/profile_creation.html', context = {})