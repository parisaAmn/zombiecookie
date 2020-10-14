from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # if request.COOKIES.get('persistent-user-id') is not None : 
    #     cookieval = request.COOKIES.get('persistent-user-id')
    #     print(cookieval)
    return render(request , 'blog/index.html')