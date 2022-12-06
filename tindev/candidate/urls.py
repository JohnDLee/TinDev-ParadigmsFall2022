from django.urls import path
from . import views

app_name = 'candidate'
urlpatterns = [
    # Fill urls here.
    path("homepage/", views.homepage_view, name='homepage'),
    path("profile_creation/", views.profile_creation_view, name='profile_creation'),
    path("post/<int:pk>/", views.post_view, name='post'),
    path("interested/<int:pk>/", views.interested_view, name='interested'),
    path("uninterested/<int:pk>/", views.uninterested_view, name='uninterested'),
    path("offers/", views.offers_view, name='offers'),
    path("offer_accept/<int:pk>/", views.offer_accept_view, name='offer_accept'),
    path("offer_decline/<int:pk>/", views.offer_decline_view, name='offer_decline')
]
