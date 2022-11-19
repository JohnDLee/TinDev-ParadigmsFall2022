from django.urls import path
from . import views

app_name = 'recruiter'
urlpatterns = [
    # Fill urls here.
    path("post_creation/<int:pk>", views.post_creation_view, name = 'post_creation'),
    path("homepage/", views.homepage_view, name = 'homepage'),
    path("profile_creation/", views.profile_creation_view, name = 'profile_creation'),
]