from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm

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