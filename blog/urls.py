from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path("signout", views.signout, name="signout"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('clear/' , views.clearcookie, name='clear'),
    # path('set/' , views.set, name='set'),
    # path('ajax/' , views.ajaxx, name='ajaxx'),
    
]