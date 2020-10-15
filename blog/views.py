from django.contrib.auth import login, authenticate , logout
from django.shortcuts import render, redirect
from .forms import SignUpForm , SignInForm
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.hashers import make_password
import uuid
from django.contrib import messages 
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings 


# Create your views here.

def set(request):
    zcookie = uuid.uuid4()
    return render(request , 'blog/set.html', {'cookieval':str(zcookie)})

def clearcookie(request):
    return render(request , 'blog/clear.html')

# def index(request):
#     if request.COOKIES.get('persistent-user-id') is not None : 
#         zcookie = request.COOKIES.get('persistent-user-id')
#         print(zcookie)
#         zcookie = uuid.UUID(zcookie)
#         number = Profile.objects.filter(cookieval = zcookie).count()
#         if number == 1:
#             user = Profile.objects.filter(cookieval = zcookie)
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             login(request , user)
#             return render(request , 'blog/index.html' , {'comefrom':'index'})
#     else: # cookie didn't find
#         return render(request , 'blog/index.html' , {'comefrom':'index'})

#     return render(request , 'blog/index.html' , {'comefrom':'index'})

def index(request):
    print('index function')
    return render (request , 'blog/index.html')

def signup(request):
    if request.method == "POST":
        print('method is post')
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('sign up func:')
            zcookie = uuid.uuid4()
            print('zcookie created')
            user = Profile.objects.create(username=form.cleaned_data.get('username'),
                                        password=make_password(form.cleaned_data.get('password1')),
                                        email=form.cleaned_data.get('email'),
                                        cookieval=zcookie)
            print('user created')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            print('user authenticated')
            login(request, user)
            print('user logged in')
            messages.info(request , str(zcookie) , extra_tags='signup')
            return redirect('index')
            # return render(request, 'blog/index.html')
            # return render(request, 'blog/index.html', {'comefrom': 'signup', 'cookieval':str(zcookie)})
        else:
            form = SignUpForm()
            return render(request, 'blog/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'blog/signup.html', {'form': form})

def ajaxx(request):
    if request.is_ajax() and request.method == 'GET':
        print("after siginup function")
        return render(request , 'blog/index.html', {'comefrom': 'ppp'})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print("sign in function :")
                #
                # SEND WARNING EMAIL
                now = timezone.now()
                subject = "XX Unexpected sign-in attempt XX"
                line0 = "somenoe using an unrecognised device attempted to sign in to your account.\n"
                line1 = " this sign in attempt was made at:\n"
                line2 = "TIME: {}\n".format(now)
                line3 = "if this was you, you don't need to do anything else.\n"
                line4 = "If you did not recently sign in, you should immediately change your password.\n"
                line5 = "Passwords should be unique and not used for any other sites or services.\n"
                message = line0+line1 + line2 + line3 + line4 + line5
                email_from = settings.EMAIL_HOST_USER 
                email_to = ['parisa.amani17@gmail.com', ]
                # email_to = [this_user.email, ]
                send_mail(subject, message, email_from, email_to, fail_silently=False, )
                # END SEND WARNING EMAIL
                #
                # update cookie of this user to the new cookie
                zcookie = uuid.uuid4()
                Profile.objects.filter(username=user.username).update(cookieval = zcookie)
                login(request, user)
                print("user loged in")
                # messages.info(request, f"You are now logged in as {username}")
                render(request, 'blog/index.html', {'comefrom': 'signin', 'cookieval':str(zcookie)})
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, 'blog/signin.html', {'form': form})
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'blog/signin.html', {'form': form})
    else:
        form = SignInForm()
    return render(request, 'blog/signin.html', {'form': form})

def about(request):
    return render(request , 'blog/about.html')

def contact(request):
    return render(request , 'blog/contact.html')

def signout(request):
    print('sign out func:')
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return render(request , "blog/logout.html")

