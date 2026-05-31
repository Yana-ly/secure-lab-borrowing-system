from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator

from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()], required=True)
    username = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9_]{3,30}$",
                message="Username must be 3-30 characters using letters, numbers, and underscores only.",
            )
        ]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class SecureAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileAttachmentForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["attachment"]

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")
        return attachment
