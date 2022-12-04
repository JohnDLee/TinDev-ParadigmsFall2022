from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CandidateProfile
from django.http import HttpResponseRedirect
from .forms import CustomCandidateCreationForm
from django.urls import reverse_lazy
from recruiter.models import JobPost
from django.db.models.functions import Lower
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

            queryset = JobPost.objects

            # FILTER STUFF GOES HERE, ALSO ADD TO CONTEXT
            if request.method == 'GET':
                interestFilter = request.GET.get("interestFilter", "")
                statusFilter = request.GET.get("statusFilter", "")
                locationFilter = request.GET.get("locationFilter", "")
                keywordFilter = request.GET.get("keywordFilter", "")

                if interestFilter == "Interested":
                    # FIX ME
                    # Should be whether the user is interested, not if there are any interested users for the post
                    queryset = queryset.filter(interested_candidates__gte=1)

                if statusFilter == "Active":
                    queryset = queryset.filter(status=statusFilter)
                elif statusFilter == "Inactive":
                    queryset = queryset.filter(status=statusFilter)

                # FIX ME
                # Should not require exact match, copy format from keyword
                if locationFilter != "":
                    queryset = queryset.filter(
                        location__icontains=locationFilter)

                if keywordFilter != "":
                    queryset = queryset.filter(
                        description__icontains=keywordFilter)

            queryset = queryset.order_by(Lower('pos_title'))

            print(queryset)
            context = {'candidate': candidate,
                       'job_posts': queryset}

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
        candidate = CandidateProfile.objects.get(user=request.user)
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
        return render(request, 'candidate/profile_creation.html', {'form': form})
