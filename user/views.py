from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
# Create your views here.


def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user/user_list.html', {'users': users})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful!")
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "user/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
    else:
        form = CustomAuthenticationForm()

    return render(request, "user/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")

def dashboard_view(request):
    return render(request, "user/dashboard.html", {"user": request.user})