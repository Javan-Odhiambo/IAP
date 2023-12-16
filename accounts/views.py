from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

User = get_user_model()


def login_user(request):
    """Logs in a user"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, "accounts/login.html")


def signup_user(request):
    """Signs up a user"""
    if request.method == "POST":
        first_name = request.POST.get(
            "first_name"
        )  # change depending on the name attribute of the input field
        last_name = request.POST.get(
            "last_name"
        )  # change depending on the name attribute of the input field
        email = request.POST.get(
            "email"
        )  # change depending on the name attribute of the input field
        password1 = request.POST.get(
            "password1"
        )  # change depending on the name attribute of the input field
        password2 = request.POST.get(
            "password2"
        )  # change depending on the name attribute of the input field
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
            )
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "home"))
    return render(request, "accounts/signup.html")


@login_required
def logout_user(request):
    """Logs out a user"""
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    """Displays and edit the user profile"""
    if request.method == "POST":
        first_name = request.POST.get(
            "first_name", request.user.first_name
        )  # change depending on the name attribute of the input field
        last_name = request.POST.get(
            "last_name", request.user.last_name
        )  # change depending on the name attribute of the input field
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile")
    return render(request, "accounts/edit-profile.html")
