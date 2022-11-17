from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
# Create your views here.

# Log In View


# Register View
def signup_view(request):
    ''' Allows a user to signup'''
    if request.method == 'POST':
        # POST
        # create bound form
        form = CustomUserCreationForm(request.POST, prefix = 'signup') 
        # if form is valid
        if form.is_valid():
            form.save()
            #save and redirect to login
            return HttpResponseRedirect("/register/login/")
        else:
            #if "username" in form.errors:
            username_err = None
            if form.has_error('username'):
                username_err = form.errors['username']
            password1_err = None
            if form.has_error('password1'):
                password1_err = form.errors['password1']
            password2_err = None
            if form.has_error('password2'):
                password2_err = form.errors['password2']
            
            
            # get errors.
            context = {"form": CustomUserCreationForm(prefix='signup'),
                       "password1_err": password1_err,
                       "password2_err": password2_err,
                       "username_err": username_err}
            return render(request, "register/signup.html", context)
    else:
        # GET, just returns the page with unbound form.
        form = CustomUserCreationForm(prefix='signup')
        return render(request, "register/signup.html", {"form":form})
    
def login_view(request):
    ''' Allows a user to login'''
    if request.method == 'POST':
        # POST
        username = request.POST['login-username'].lower()
        password = request.POST['login-password']
        user = authenticate(request, username=username, password=password)
        
        # failure to authenticate
        if user is None:
            login_err = 'Username or Password does not match valid user.'
            return render(request, "register/login.html", {"login_err": login_err})
        
        # authenticated
        else:
            login(request, user)
            group_list = list(user.groups.all())
            if len(group_list) < 1:
                # superuser
                return HttpResponseRedirect("/admin/")
            group = group_list[0].name
            if group == 'Candidates':
                return HttpResponseRedirect("/candidate/homepage/")
            elif group == 'Recruiters':
                return HttpResponseRedirect("/recruiter/homepage/")
            print(group)
            print(user.is_authenticated)
            
    else:
        # GET, just returns the page.
        return render(request, "register/login.html", {})
    
    
# note, look into @group_required("group") decorator for group only views
# For authentication blocking https://docs.djangoproject.com/en/4.1/topics/auth/default/

