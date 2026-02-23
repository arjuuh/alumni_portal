from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from admin_module.models import SystemMetadata   # ✅ correct import


def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

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
    pending = SystemMetadata.objects.filter(status="PENDING").select_related("user")
    return render(request, "teacher/verify_alumni.html", {"pending": pending})


@login_required
def approve_alumni(request, user_id):
    user = get_object_or_404(User, id=user_id)

    metadata, _ = SystemMetadata.objects.get_or_create(user=user)
    metadata.status = "APPROVED"
    metadata.save()

    return redirect("verify_alumni")



def approved_alumni(request):
    approved = SystemMetadata.objects.filter(status="APPROVED")
    return render(request, "teacher/approved_alumni.html", {"approved": approved})