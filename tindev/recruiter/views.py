from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import RecruiterProfile, JobPost
from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from .forms import RecruiterProfileCreationForm, JobPostCreationForm
from django.db.models.functions import Lower
from django import forms
from django.urls import reverse_lazy
from candidate.models import CandidateProfile
# Create your views here.


def recruiter_check(user):
    ''' checks that a user is a part of candidate'''
    return list(user.groups.all())[0].name == 'Recruiters'


login_url = '/register/login/'

# decorators to check logged in and correct candidate


@login_required(login_url=login_url)
@user_passes_test(recruiter_check, login_url=login_url)
def homepage_view(request):
    ''' Homepage View'''
    # there should only be get method for now
    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)
        # recruiter profile exists already, load page.

        # get the Job postings corresponding to recruiter
        queryset = JobPost.objects.filter(recruiter=recruiter)
        if request.method == 'GET':
            filter = request.GET.get("filter", "")
            if filter == "Active":
                queryset = queryset.filter(status=filter)
            elif filter == "Inactive":
                queryset = queryset.filter(status=filter)
            elif filter == "Interested":
                queryset = queryset.filter(interested_candidates__gte=1)

        queryset = queryset.order_by(Lower('pos_title'))

        print(queryset)
        context = {'recruiter': recruiter,
                   'job_posts': queryset,
                   "filter": forms.ChoiceField(choices=(("Candidate", "Candidate"), ("Recruiter", "Recruiter")))}

        return render(request, 'recruiter/homepage.html', context=context)
    except RecruiterProfile.DoesNotExist:
        # recruiter profile does not exist, redirect to profile creation.
        return HttpResponseRedirect('/recruiter/profile_creation')


@login_required(login_url=login_url)
@user_passes_test(recruiter_check, login_url=login_url)
def profile_creation_view(request):
    ''' profile creation view'''
    # check if a recruiter profile exists already
    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)
        # recruiter profile exists already, redirect to homepage.
        return HttpResponseRedirect('/recruiter/homepage/')
    except RecruiterProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        # create bound form
        form = RecruiterProfileCreationForm(
            request.POST, prefix='profile_creation')
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
        return render(request, 'recruiter/profile_creation.html', {'form': form})


@login_required(login_url=login_url)
@user_passes_test(recruiter_check, login_url=login_url)
def post_creation_view(request):
    # check if a recruiter profile exists already
    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        # no recruiter exists
        HttpResponseRedirect("/recruiter/profile_creation/")

    if request.method == 'POST':
        # create bound form
        form = JobPostCreationForm(request.POST, prefix='job_post')
        # if form valid
        print(form.errors)
        if form.is_valid():
            # save and redirect to recruiter page
            form.save(recruiter=recruiter)
            return HttpResponseRedirect(f'/recruiter/homepage/')
        else:
            context = {'form': RecruiterProfileCreationForm(prefix='job_post')}
            return render(request, 'recruiter/post_creation.html', context)
    else:
        # Job Post Init
        form = JobPostCreationForm(prefix='job_post')
        return render(request, 'recruiter/post_creation.html', {'form': form})


class PostView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    # logged in check
    login_url = login_url
    redirect_field_name = "redirect_to"

    # recruiter check

    def test_func(self):
        if recruiter_check(self.request.user):
            try:
                self.recruiter = RecruiterProfile.objects.get(
                    user=self.request.user)
                return True
            except RecruiterProfile.DoesNotExist:
                # no recruiter exists
                HttpResponseRedirect("/recruiter/profile_creation/")
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['candidates'] = CandidateProfile.objects.get_queryset()
        return context

    template_name = 'recruiter/post.html'
    context_object_name = "post"
    model = JobPost


@login_required(login_url=login_url)
@user_passes_test(recruiter_check, login_url=login_url)
def post_delete_view(request, pk=None):
    # check if a recruiter profile exists already
    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        # no recruiter exists
        return HttpResponseRedirect("/recruiter/profile_creation/")

    # check its yours
    post = list(JobPost.objects.filter(recruiter=recruiter).filter(pk=pk))
    if len(post) == 0:
        pass
    else:
        # delete post
        post[0].delete()

    return HttpResponseRedirect("/recruiter/homepage/")


@login_required(login_url=login_url)
@user_passes_test(recruiter_check, login_url=login_url)
def post_update_view(request, pk=None):
    # check if a recruiter profile exists already
    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        # no recruiter exists
        return HttpResponseRedirect("/recruiter/profile_creation/")

    # check its yours
    post = JobPost.objects.filter(recruiter=recruiter).filter(pk=pk)
    if len(list(post)) == 0:
        return HttpResponseRedirect("/recruiter/homepage/")
    # get initial
    init = list(post.values())[0]

    if request.method == 'POST':
        form = JobPostCreationForm(
            request.POST, initial=init, prefix="update_post")

        if form.is_valid():

            # save and redirect to recruiter page
            form.update(recruiter=recruiter,
                        prev_candidates=init['interested_candidates'], pk=pk)
            return HttpResponseRedirect(f'/recruiter/post/{pk}')
        else:

            context = {'form': JobPostCreationForm(initial=init, prefix="update_post"),
                       "pk": pk}
            return render(request, 'recruiter/post_update.html', context)
    else:
        form = JobPostCreationForm(initial=init, prefix="update_post")
        print(form.initial)
        return render(request, "recruiter/post_update.html", context={'form': form, "pk": pk})
