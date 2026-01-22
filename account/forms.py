from django import forms
from django.contrib.auth import get_user_model

# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Kyc
from account import helper
from baseapp import utils


User = get_user_model()


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["profile_image"]


class RegisterForm(UserCreationForm):
    """
    The default

    """

    first_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "First_name",
                "autocomplete": False,
            }
        ),
        label="First Name",
        required=True,
    )

    midle_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Middle name",
                "autocomplete": False,
            }
        ),
        label="Middle name",
        required=True,
    )

    last_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Last name",
                "autocomplete": False,
            }
        ),
        label="Last name",
        required=True,
    )

    username = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": False,
            }
        ),
        label="Username",
        required=True,
    )

    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "Email",
                "autocomplete": False,
            }
        ),
        label="Email",
        required=True,
    )

    phone_number = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "placeholder": "eg:+14042717669",
                "autocomplete": False,
            }
        ),
        label="Phone",
        required=True,
    )

    country = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
        label="Country",
        required=True,
    )

    account_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Account Type",
        required=True,
    )

    security_pin = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Security Pin",
        required=True,
    )

    password1 = forms.CharField(
        max_length=30,
        min_length=6,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
    )
    password2 = forms.CharField(
        max_length=30,
        min_length=6,
        label="Confirm Password:",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Verify Password",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "midle_name",
            "last_name",
            "username",
            "email",
            "country",
            "phone_number",
            "account_type",
            "security_pin",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)  # Get the form instance

        # Process and assign additional fields if needed
        user.ip_address = utils.gen_random_number()

        # Save the user to the database if commit=True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=80,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "autocomplete": "off",
            }
        ),
        label="Email",
        required=True,
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")

            cleaned_data["user"] = user

        return cleaned_data


class KycForm(forms.ModelForm):
    class Meta:
        model = Kyc
        fields = "__all__"
        exclude = ["user", "is_approved", "status", "created_at"]
