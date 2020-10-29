from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'نام کاربری'
        self.fields['email'].widget.attrs['placeholder'] = 'ایمیل'
        self.fields['password1'].widget.attrs['placeholder'] = 'روز عبور'
        self.fields['password2'].widget.attrs['placeholder'] = 'تکرار رمز عبور'


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password' )
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'نام کاربری'
        self.fields['password'].widget.attrs['placeholder'] = 'رمز عبور'

