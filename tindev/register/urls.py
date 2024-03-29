from django.urls import path
from . import views

app_name = 'register'
urlpatterns = [
    # Fill urls here.
    path("logout/", views.logout_view, name = 'logout'),
    path("login/", views.login_view, name = 'login'),
    path("signup/", views.signup_view, name = 'signup'),
]
