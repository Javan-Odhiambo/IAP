from django.shortcuts import render

# Create your views here.


def loginPage(request):
    return render(request, "accounts/login.html")

def signupPage(request):
    return render(request, "accounts/signup.html")

def logoutUser(request):
    ...

def editProfilePage(request):
    return render(request, "accounts/edit-profile.html")