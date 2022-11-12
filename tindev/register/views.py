from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
# from .models import RecruiterProfile, CandidateProfile
from .forms import CustomUserCreationForm
# Create your views here.

# Log In View


# Register View
def signup_view(request):
    ''' Allows a user to signup'''
    if request.method == 'POST':
        # POST
        # create bound form
        data = {'signup-username': request.POST['signup-username'],
                'signup-password1': request.POST['signup-password1'],
                'signup-password2': request.POST['signup-password2'],
                'signup-profile_type': request.POST['signup-profile_type']}
        
        form = CustomUserCreationForm(data, prefix = 'signup') 
        print(data)
        # if form is valid
        if form.is_valid():
            form.save()
            #save and redirect to login
            return HttpResponseRedirect(reverse_lazy("login"))
        else:
            
            print(form.errors.as_data())
            # get errors.
            context = {"form": CustomUserCreationForm(prefix='signup'),
                       "password_error": "x"}
            return render(request, "register/signup.html", context)
    else:
        # GET, just returns the page with unbound form.
        form = CustomUserCreationForm(prefix='signup')
        return render(request, "register/signup.html", {"form":form})
    
    
# note, look into @group_required("group") decorator for group only views