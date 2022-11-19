from django.urls import path
from . import views

app_name = 'recruiter'
urlpatterns = [
    # Fill urls here.
    path("post_update/<int:pk>/", views.post_update_view, name = 'post_update'),
    path("post_delete/<int:pk>/", views.post_delete_view, name = 'post_delete'),
    path("post/<int:pk>/", views.PostView.as_view(), name = 'post'),
    path("post_creation/", views.post_creation_view, name = 'post_creation'),
    path("homepage/", views.homepage_view, name = 'homepage'),
    path("profile_creation/", views.profile_creation_view, name = 'profile_creation'),
]