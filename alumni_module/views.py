from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import AlumniProfile
from django.contrib.auth.decorators import login_required
from admin_module.models import SystemMetadata

def home(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")

        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # 👇 Automatically create AlumniProfile
            AlumniProfile.objects.create(
                user=user,
                first_name="",
                last_name="",
                gender="",
                date_of_birth="2000-01-01"
            )

            return redirect('home')

    return render(request, 'register.html')

@login_required
def dashboard(request):
    metadata, created = SystemMetadata.objects.get_or_create(
        user=request.user
    )

    if not metadata.verified_by_admin:
        return render(request, 'not_verified.html')

    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    profile, created = AlumniProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "first_name": "",
            "last_name": "",
            "gender": "",
            "date_of_birth": "2000-01-01"
        }
    )

    if request.method == "POST":
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.gender = request.POST.get('gender')
        profile.save()
        return redirect('dashboard')

    return render(request, 'edit_profile.html', {'profile': profile})
