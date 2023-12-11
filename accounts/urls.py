from django.urls import path
from .views import loginPage, signupPage, logoutUser, editProfilePage

urlpatterns = [
    path("login/", loginPage, name="login"),
    path("signup/", signupPage, name="signup"),
    path("logout/", logoutUser, name="logout"),
    path("edit-profile/", editProfilePage, name="edit-profile"),
]
