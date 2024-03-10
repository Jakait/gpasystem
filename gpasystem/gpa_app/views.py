from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'login.html')

# register user
def registerUser(request):
    return render(request,'userreg.html')