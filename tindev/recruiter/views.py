from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import RecruiterProfile
from django.http import HttpResponseRedirect
from .forms import RecruiterProfileCreationForm
from django.urls import reverse_lazy
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
    if request.method == 'POST':
        # create bound form
        form = RecruiterProfileCreationForm(request.POST, prefix='profile_creation')
        # if form valid
        if form.is_valid():
            # save and redirect to recruiter page
            recruiter = form.save(req=request)
            recruiter.save()
            return HttpResponseRedirect('/recruiter/homepage/')
        else:
            # if zip code has error
            zip_code_err = None
            if form.has_error('zip_code'):
                zip_code_err = form.errors['zip_code']

            # get errors
            context = {'form': RecruiterProfileCreationForm(prefix='profile_creation'),
                        'zip_code_err': zip_code_err}
            return render(request, 'recruiter/profile_creation.html', context)
    else:
        # GET, check if profile exists
        try:
            recruiter = RecruiterProfile.objects.get(user = request.user)
            # recruiter profile exists already, redirect to homepage.
            return HttpResponseRedirect('/recruiter/homepage/')
        except RecruiterProfile.DoesNotExist:
            # recruiter profile does not exist, load profile creation.
            form = RecruiterProfileCreationForm(prefix='profile_creation')
            return render(request, 'recruiter/profile_creation.html', {'form':form})