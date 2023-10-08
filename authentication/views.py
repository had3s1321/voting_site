from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
from .utils import email_verification_token
from validate_email import validate_email
from helpers.decorators import auth_user_should_not_access
from .models import User
import threading



User = get_user_model()

# sends email in background for increased speed
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html',{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user)
    })


    email = EmailMessage(subject=email_subject, body=email_body,
                 from_email=settings.EMAIL_FROM_USER, to=[user.email])
    
    EmailThread(email).start()


@auth_user_should_not_access
def register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 8:
            messages.add_message(request, messages.ERROR, 'Password should be at least 8 characters!')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Your passwords must match!')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Enter a valid email address!')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR, 'Username is required!')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username is taken, please choose another one!')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email is already registered!')
            context['has_error'] = True

        if not context['has_error']:
            user = User.objects.create_user(username=username, email=email, password=password)

            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS, 'Account created! Please check your email to verify your account.')
            return redirect('register')


    return render(request, 'authentication/register.html')



@auth_user_should_not_access
def login_user(request):

    if request.method == 'POST':
        context = {'data':request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox!')
            return render(request, 'authentication/login.html', context)

        if not user:
            messages.add_message(request, messages.ERROR, 
                                 'Invalid credentials')
            return render(request, 'authentication/login.html', context)
        
        login(request, user)

        messages.add_message(request, messages.SUCCESS, f'Welcome {user.username}')
        return redirect(reverse('home'))

    return render(request, 'authentication/login.html')


def logout_user(request):

    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')

    return redirect(reverse('login'))


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 
                             'Email verified, you can now continue your registration')
        return redirect(reverse('login'))
    
    return render(request, 'authentication/activation-failed.html', {'user': user})