from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_poll, name='create'),
    path('vote/<poll_id>/', views.vote, name='vote'),
    path('results/<poll_id>/', views.results, name='results'),
    path('voter-registration', views.voter_registration, name='voter-registration'),
]