from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrazione completata.")
            return redirect("dashboard")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})

def privacy_policy_view(request):
    return render(request, "accounts/privacy_policy.html")

@login_required
def profile_view(request):

    return render(request, "accounts/profile.html")