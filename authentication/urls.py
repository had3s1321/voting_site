from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path("logout-user", views.logout_user, name='logout-user'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
]