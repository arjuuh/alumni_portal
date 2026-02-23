from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from teacher_module.models import Alumni


def teacher_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Invalid teacher credentials")

    return render(request, 'teacher/teacher_login.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'teacher/teacher_dashboard.html')

@login_required
def verify_alumni(request):
    if not request.user.is_staff:
        return redirect('home')

    users = User.objects.all()
    return render(request, 'teacher/verify_alumni.html', {'users': users})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import SystemMetadata


def approve_alumni(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Get or create Alumni record
    alumni, created = Alumni.objects.get_or_create(user=user)

    # 👇 THIS IS WHERE YOU PLACE IT
    alumni.status = "APPROVED"
    alumni.save()

    return redirect("verify_alumni")