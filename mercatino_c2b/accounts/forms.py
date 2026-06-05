from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label="Nome"
    )

    last_name = forms.CharField(
        required=True,
        label="Cognome"
    )

    email = forms.EmailField(
        required=True,
        label="Email",
    )

    phone = forms.CharField(
        required=True,
        label="Telefono",
        max_length=20
    )

    privacy = forms.BooleanField(
        required=True,
        label="Accetto la Privacy Policy e il trattamento dei dati personali",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
            "privacy",
        ]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
            )
        
        return user