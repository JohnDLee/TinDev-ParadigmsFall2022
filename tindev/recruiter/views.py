from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import RecruiterProfile, JobPost
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from .forms import RecruiterProfileCreationForm
from django.db.models.functions import Lower
from django import forms
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
    try:
        recruiter = RecruiterProfile.objects.get(user = request.user)
        # recruiter profile exists already, load page.

        
        # get the Job postings corresponding to recruiter
        queryset = JobPost.objects.filter(recruiter = recruiter)
        if request.method == 'GET':
            filter = request.GET.get("filter", "")
            if filter == "Active":
                queryset = queryset.filter(status = filter)
            elif filter == "Inactive":
                queryset = queryset.filter(status = filter)
            elif filter == "Interested":
                queryset = queryset.filter(interested_candidates__gte = 1)
                
                
        queryset = queryset.order_by(Lower('pos_title'))
        
        print(queryset)
        context = {'recruiter': recruiter,
                    'job_posts': queryset,
                    "filter": forms.ChoiceField(choices = (("Candidate","Candidate"), ("Recruiter","Recruiter")))}
        
        return render(request, 'recruiter/homepage.html', context=context)
    except RecruiterProfile.DoesNotExist:
        # recruiter profile does not exist, redirect to profile creation.
        return HttpResponseRedirect('/recruiter/profile_creation')
    

@login_required(login_url = login_url)
@user_passes_test(recruiter_check, login_url = login_url)
def profile_creation_view(request):
    ''' profile creation view'''
    # check if a recruiter profile exists already
    try:
        recruiter = RecruiterProfile.objects.get(user = request.user)
        # recruiter profile exists already, redirect to homepage.
        return HttpResponseRedirect('/recruiter/homepage/')
    except RecruiterProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        # create bound form
        form = RecruiterProfileCreationForm(request.POST, prefix='profile_creation')
        # if form valid
        if form.is_valid():
            # save and redirect to recruiter page
            recruiter = form.save(req=request)
            recruiter.save()
            return HttpResponseRedirect(f'/recruiter/homepage/')
        else:
            # if zip code has error
            zip_code_err = None
            if form.has_error('zip_code'):
                zip_code_err = form.errors['zip_code']
            print(form.errors)

            # get errors
            context = {'form': RecruiterProfileCreationForm(prefix='profile_creation'),
                        'zip_code_err': zip_code_err}
            return render(request, 'recruiter/profile_creation.html', context)
    else:
        # recruiter profile does not exist, load profile creation.
        form = RecruiterProfileCreationForm(prefix='profile_creation')
        return render(request, 'recruiter/profile_creation.html', {'form':form})
    
@login_required(login_url = login_url)
@user_passes_test(recruiter_check, login_url = login_url)
def post_creation_view(request):
    pass