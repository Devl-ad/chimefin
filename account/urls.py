from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_acct, name="register_acct"),
    path("login/", views.logi_acct, name="login_acct"),
    path("forgot-password/", views.forgot_pass, name="forgot-password"),
    path(
        "profile-image/",
        views.update_profile_image,
        name="update_profile_image",
    ),
]
