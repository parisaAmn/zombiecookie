from django.contrib.auth import login, authenticate , logout
from django.shortcuts import render, redirect , get_object_or_404
from .forms import SignUpForm , SignInForm
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.hashers import make_password
import uuid
from django.contrib import messages 
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings 
from django.utils.translation import activate


# Create your views here.
def index(request):
    print('index function')
    return render (request , 'blog/index.html')

def signup(request):
    activate('fa')
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
        else:
            return render(request, 'blog/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'blog/signup.html', {'form': form})

def signout(request):
    print('sign out func')
    logout(request)
    messages.info(request , "signout" , extra_tags='signout')
    return render(request , "blog/logout.html")

def ajaxx(request):
    print('ajax func')
    if request.is_ajax() and request.method == 'GET':
        print('request is ajax and get')
        if request.COOKIES.get('persistent-user-id') is not None :
            print('zcookie exists')
            zcookie = request.COOKIES.get('persistent-user-id', None)
            print(zcookie)
            if zcookie is not None:
                print('zcookie is not None')
                zcookie = uuid.UUID(zcookie)
                print('zcookie converted to UUID')
                number = Profile.objects.filter(cookieval = zcookie).count()
                print('calculate if there is a user with this cookie in database')
                if number == 1:
                    print('there is a user in DB')
                    user = Profile.objects.get(cookieval = zcookie)
                    print('get user with that cookie value')
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request , user)
                    print('user logged in')
                    return render(request , 'blog/index.html')
                else:
                    return render(request , 'blog/index.html')
            else:
                return render(request , 'blog/index.html')
        else:
            return render(request , 'blog/index.html')
    else:
        return render(request , 'blog/index.html')




def SendEmail(email):
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
    # email_to = [ email, ]
    send_mail(subject, message, email_from, email_to, fail_silently=False, )
    # END SEND WARNING EMAIL

def updatecookie(username , zcookie):
    # update cookie of this user to the new cookie
    zcookie = uuid.uuid4()
    print('cookie created')
    Profile.objects.filter(username=username).update(cookieval = zcookie)


def signin(request):
    activate('fa')
    if request.method == 'POST':#1
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():#2
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:#3
                print("sign in function")
                this_user = Profile.objects.get(username = username )
                zcookie = request.COOKIES.get('persistent-user-id' , None)
                if zcookie is None :#4
                    print('cookie is None')
                    SendEmail(this_user.email)
                    zcookie = uuid.uuid4()
                    updatecookie(this_user.username , zcookie)
                    login(request, user)
                    messages.info(request , str(zcookie) , extra_tags='signin')
                    return redirect('index')
                else:#4 cookie exists in client machine
                    print('cookie is Not None')
                    zcookie = request.COOKIES.get('persistent-user-id' , None)
                    if this_user.cookieval != uuid.UUID(zcookie):
                        print('this_user.cookie is not same as seesion cookie')
                        print('user cookie: {}'.format(this_user.cookieval))
                        print('session cookie: {}'.format(zcookie))
                        SendEmail(this_user.email)
                        login(request, user)
                        print("user loged in")
                        zcookie = this_user.cookieval
                        messages.info(request , str(zcookie) , extra_tags='signin')
                        return redirect('index')
                    else:
                        print('this_user.cookie is same as session cookie')
                        login(request, user)
                        print("user loged in")
                        messages.info(request , str(zcookie) , extra_tags='signin')
                        return redirect('index')

            else:#3
                messages.error(request, "نام کاربری یا رمز عبور معتبر نیست")
                return render(request, 'blog/signin.html', {'form': form})
        else:#2
            messages.error(request, "نام کاربری یا رمز عبور معتبر نیست")
            return render(request, 'blog/signin.html', {'form': form})
    else:#1
        form = SignInForm()
    return render(request, 'blog/signin.html', {'form': form})