from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrazione completata.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})