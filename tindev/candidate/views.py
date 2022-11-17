from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CandidateProfile
from django.http import HttpResponseRedirect
from .forms import CustomCandidateCreationForm
from django.urls import reverse_lazy
# Create your views here.


def candidate_check(user):
    ''' checks that a user is a part of candidate'''
    return list(user.groups.all())[0].name == 'Candidates'


login_url = '/register/login/'

# decorators to check logged in and correct candidate


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def homepage_view(request):
    ''' Homepage View'''

    # there should only be get method for now
    if request.method == 'GET':
        try:
            candidate = CandidateProfile.objects.get(user=request.user)
            # candidate profile exists already, load page.
            context = {'candidate': candidate}
            return render(request, 'candidate/homepage.html', context=context)
        except CandidateProfile.DoesNotExist:
            # candidate profile does not exist, redirect to profile creation.
            return HttpResponseRedirect('/candidate/profile_creation')


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def profile_creation_view(request):
    ''' profile creation view'''
    # check that user doesn't already have an associated model
    try:
        candidate = CandidateProfile.objects.get(user = request.user)
        # candidate profile exists already, redirect to homepage.
        return HttpResponseRedirect('/candidate/homepage/')
    except CandidateProfile.DoesNotExist:
        pass
    
    # fill this
    if request.method == 'POST':
        # create the bound form
        form = CustomCandidateCreationForm(
            request.POST, prefix='profile_creation')
        # if a valid form, send to their dashboard
        if form.is_valid():
            candidate = form.save(req=request)
            candidate.save()
            return HttpResponseRedirect("/candidate/homepage/")
        else:
            zip_code_err = None
            if form.has_error('zip_code'):
                zip_code_err = form.errors['zip_code']
            exper_err = None
            if form.has_error('experience'):
                exper_err = form.errors['experience']

            context = {"form": CustomCandidateCreationForm(prefix='profile_creation'),
                       "zip_code_error": zip_code_err,
                       "exper_error": exper_err
                       }
            return render(request, "candidate/profile_creation.html", context)
    else:
        # candidate profile does not exist, load profile creation.
        form = CustomCandidateCreationForm(prefix='profile_creation')
        return render(request, 'candidate/profile_creation.html', {'form':form})
