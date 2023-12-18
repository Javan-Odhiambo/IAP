from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", view=views.login_user, name="login"),
    path("signup/", view=views.signup_user, name="signup"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", view=views.edit_profile, name="profile"),
]
