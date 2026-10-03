from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import StudentProfile, User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
        min_length=8,
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "picture",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile

        fields = [
            "department",
            "date_of_birth",
            "status",
        ]

        widgets = {
            "department": forms.Select(
                attrs={"class": "form-select"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


class StudentCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "password",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }


class StudentStatusForm(forms.ModelForm):
    class Meta:
        model = StudentProfile

        fields = ["status"]

        widgets = {
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }