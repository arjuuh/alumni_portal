from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from admin_module.models import SystemMetadata
from alumni_module.models import Opportunity, AlumniProfile, AcademicDetails, ProfessionalDetails, ContactDetails


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

    pending_requests = SystemMetadata.objects.filter(status="PENDING")

    verified_count = SystemMetadata.objects.filter(status="APPROVED").count()
    pending_count = pending_requests.count()
    total_alumni = SystemMetadata.objects.count()

    return render(request, "teacher/teacher_dashboard.html", {
        "pending_requests": pending_requests,
        "verified_count": verified_count,
        "pending_count": pending_count,
        "total_alumni": total_alumni,
    })

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


@login_required
def post_job(request):
    if request.method == "POST":
        Opportunity.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            opportunity_type='JOB',
            location=request.POST['location'],
            deadline=request.POST['deadline'],
            posted_by=request.user
        )
        return redirect('teacher_dashboard')

    return render(request, 'teacher/post_job.html')


@login_required
def post_event(request):
    if request.method == "POST":
        Opportunity.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            opportunity_type='EVENT',
            location=request.POST['location'],
            event_date=request.POST['event_date'],
            posted_by=request.user
        )
        return redirect('teacher_dashboard')

    return render(request, 'teacher/post_event.html')

@login_required
def teacher_view_alumni(request, user_id):

    user = get_object_or_404(User, id=user_id)

    profile = AlumniProfile.objects.filter(user=user).first()
    academic = AcademicDetails.objects.filter(user=user).first()
    professional = ProfessionalDetails.objects.filter(user=user).first()
    contact = ContactDetails.objects.filter(user=user).first()

    return render(request, "teacher/alumni_detail.html", {
        "alumni_user": user,
        "profile": profile,
        "academic": academic,
        "professional": professional,
        "contact": contact,
    })

@login_required
def reject_alumni(request, user_id):
    user = get_object_or_404(User, id=user_id)

    metadata = SystemMetadata.objects.filter(user=user).first()

    if metadata:
        metadata.status = "REJECTED"
        metadata.save()

    return redirect('verify_alumni')