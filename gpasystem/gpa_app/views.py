from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'login.html')

# register user
def registerUser(request):

    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        print(request.POST)
      
        if form.is_valid():
            print(request.POST)
            form.save()
            
            messages.success(request, "user saved succesful.")
            return redirect('home')  # Redirect to the login page
    return render(request,'userreg.html',{"form": form})


# view users
def  viewUser(request):
    return render(request,'userview.html')