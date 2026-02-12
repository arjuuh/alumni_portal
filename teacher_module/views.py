from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_module.models import SystemMetadata
from django.contrib.auth.models import User

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

    return render(request, 'teacher_login.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def verify_alumni(request):
    if not request.user.is_staff:
        return redirect('home')

    users = User.objects.all()
    return render(request, 'verify_alumni.html', {'users': users})

@login_required
def approve_alumni(request, user_id):
    if not request.user.is_staff:
        return redirect('home')

    user = User.objects.get(id=user_id)
    metadata, created = SystemMetadata.objects.get_or_create(user=user)
    metadata.verified_by_admin = True
    metadata.save()

    return redirect('verify_alumni')