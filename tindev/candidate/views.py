from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CandidateProfile
from django.http import HttpResponseRedirect
from .forms import CustomCandidateCreationForm
from django.urls import reverse_lazy
from recruiter.models import JobPost
from django.db.models.functions import Lower
from recruiter.models import Offer
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

            # perform filtering
            if request.method == 'GET':
                interestFilter = request.GET.get("interestFilter", "")
                statusFilter = request.GET.get("statusFilter", "")
                locationFilter = request.GET.get("locationFilter", "")
                keywordFilter = request.GET.get("keywordFilter", "")

                if interestFilter == "Interested":
                    queryset = queryset.filter(
                        interested_ids__icontains=f",{candidate.id},")

                if statusFilter == "Active":
                    queryset = queryset.filter(status=statusFilter)
                elif statusFilter == "Inactive":
                    queryset = queryset.filter(status=statusFilter)

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


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def post_view(request, pk=None):
    ''' Post View '''

    # check if candidate profile exists
    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseRedirect('/candidate/profile_creation')

    # get post by id
    post = JobPost.objects.get(pk=pk)

    # check if post exists
    if not post:
        return HttpResponseRedirect('/candidate/homepage')

    return render(request, 'candidate/post.html', context={'post': post})


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def interested_view(request, pk=None):
    ''' Interested View '''

    # check if candidate profile exists
    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseRedirect('/candidate/profile_creation')

    # get post by id
    post = JobPost.objects.get(pk=pk)

    # add candidate id to post interested list
    if post:
        if str(candidate.id) not in post.interested_ids.split(','):
            post.interested_ids += f',{candidate.id},'
            post.interested_candidates += 1
            post.save()
        # remove post from candidate uninterested list
        if str(post.id) in candidate.uninterested_ids.split(','):
            uninterested_ids = candidate.uninterested_ids.split(',')
            uninterested_ids.remove(str(post.id))
            candidate.uninterested_ids = ',' + \
                ','.join(uninterested_ids)+','
            candidate.save()

    return HttpResponseRedirect('/candidate/homepage')


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def uninterested_view(request, pk=None):
    # check if candidate profile exists
    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseRedirect('/candidate/profile_creation')

    # get post by id
    post = JobPost.objects.get(pk=pk)

    # add post id to candidate uninterested list
    if post:
        if str(post.id) not in candidate.uninterested_ids.split(','):
            candidate.uninterested_ids += f',{post.id},'
            candidate.save()
        # remove candidate from post interested list
        if str(candidate.id) in post.interested_ids.split(','):
            interested_ids = post.interested_ids.split(',')
            interested_ids.remove(str(candidate.id))
            post.interested_ids = ',' + \
                ','.join(interested_ids)+','
            post.interested_candidates -= 1
            post.save()

    return HttpResponseRedirect('/candidate/homepage')


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def offers_view(request):
    # check if candidate profile exists
    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseRedirect('/candidate/profile_creation')

    offers = Offer.objects.filter(candidate=candidate)

    return render(request, 'candidate/offers.html', context={'offers': offers, 'candidate': candidate})


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def offer_accept_view(request, pk=None):
    # check if candidate profile exists
    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseRedirect('/candidate/profile_creation')

    offers = list(Offer.objects.filter(candidate=candidate).filter(pk=pk))

    if not len(offers):
        return HttpResponseRedirect('/candidate/offers')

    offer = Offer.objects.get(pk=pk)

    offer.accept()

    offer.save()

    return HttpResponseRedirect('/candidate/offers')


@login_required(login_url=login_url)
@user_passes_test(candidate_check, login_url=login_url)
def offer_decline_view(request, pk=None):
    # check if candidate profile exists
    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseRedirect('/candidate/profile_creation')

    offers = list(Offer.objects.filter(candidate=candidate).filter(pk=pk))

    if not len(offers):
        return HttpResponseRedirect('/candidate/offers')

    offer = Offer.objects.get(pk=pk)

    offer.decline()

    offer.save()

    return HttpResponseRedirect('/candidate/offers')
