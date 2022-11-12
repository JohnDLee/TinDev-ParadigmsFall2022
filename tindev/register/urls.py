from django.urls import path
from . import views

app_name = 'register'
urlpatterns = [
    # Fill urls here.
    path("signup/", views.signup_view, name = 'signup'),
]
