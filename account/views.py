from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileImageForm
from django.contrib.auth import authenticate, login, logout
from user.models import Account


from baseapp import utils


@login_required
def update_profile_image(request):
    user = request.user
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():

            form.save()
            messages.info(request, f"Profile Image Uploaded")
            return redirect("account-overview")
        else:
            messages.info(request, f"{form.errors}")
            return redirect("account-overview")
    else:
        messages.info(request, f"GET REQUEST NOT ACCEPTED")
        return redirect("account-overview")


def register_acct(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()  # or whatever you do to create the user

            return JsonResponse(
                {
                    "success": True,
                    "message": "Account created successfully, You can now login",
                    "redirect_url": "/login/",
                }
            )

        # Form is invalid → send errors as nice JSON
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors,
                "message": "Please correct the errors below.",
            },
            status=400,
        )
    else:
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})


def logi_acct(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already logged in")
        return redirect("dashboard")

    destination = utils.get_next_destination(request)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            if destination:
                return redirect(destination)
            return redirect("dashboard")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def forgot_pass(request):
    return render(request, "auth/forgot-pasword.html")


def log_out(request):
    logout(request)
    return redirect("login_acct")
