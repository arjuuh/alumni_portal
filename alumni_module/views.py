from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import AlumniProfile, AcademicDetails, ProfessionalDetails, ContactDetails, Post
from django.contrib.auth.decorators import login_required
from admin_module.models import SystemMetadata
from .models import AlumniEngagement
from django.db import transaction


def home(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                metadata = SystemMetadata.objects.filter(user=user).first()

                if not metadata:
                    messages.error(request, "Profile not found.")
                    return redirect("home")

                if metadata.status == "PENDING":
                    messages.warning(request, "Your account is waiting for approval.")
                    return redirect("waiting_approval")

                if metadata.status == "REJECTED":
                    messages.error(request, "Your account was rejected. Contact admin.")
                    return redirect("home")

                # If APPROVED
                login(request, user)
                return redirect("dashboard")

            else:
                messages.error(request, "Invalid credentials")

        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "auth/home.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "auth/register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "auth/register.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "auth/register.html", {
                "error": "Email already registered"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create metadata with PENDING status
        from admin_module.models import SystemMetadata
        SystemMetadata.objects.create(
            user=user,
            status="PENDING"
        )

        return redirect("complete_profile")

    return render(request, "auth/register.html")

@login_required
def dashboard(request):

    metadata = SystemMetadata.objects.filter(user=request.user).first()

    if not metadata or not metadata.verified_by_admin:
        return redirect("waiting_approval")
    
    profile, _ = AlumniProfile.objects.get_or_create(user=request.user)
    professional = ProfessionalDetails.objects.filter(user=request.user).first()
    academic = AcademicDetails.objects.filter(user=request.user).first()
    contact = ContactDetails.objects.filter(user=request.user).first()

    posts = Post.objects.filter(user=request.user)

    return render(request, "alumni/dashboard.html", {
        "profile": profile,
        "professional": professional,
        "academic": academic,
        "contact": contact,
        "posts": posts,
        "followers_count": 0,
        "following_count": 0,
    })

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):

    profile, _ = AlumniProfile.objects.get_or_create(user=request.user)
    academic, _ = AcademicDetails.objects.get_or_create(user=request.user)
    professional, _ = ProfessionalDetails.objects.get_or_create(user=request.user)
    contact, _ = ContactDetails.objects.get_or_create(user=request.user)
    engagement, _ = AlumniEngagement.objects.get_or_create(
    user=request.user
)



    if request.method == "POST":

        # Personal
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.gender = request.POST.get('gender')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.country = request.POST.get('country')
        profile.postal_code = request.POST.get('postal_code')
        profile.save()

        # Academic
        academic.student_id = request.POST.get('student_id')
        academic.degree = request.POST.get('degree')
        academic.department = request.POST.get('department')
        admission = request.POST.get('year_of_admission')
        academic.year_of_admission = int(admission) if admission else None
        graduation = request.POST.get('year_of_graduation')
        academic.year_of_graduation = int(graduation) if graduation else None
        academic.achievements = request.POST.get('achievements')
        academic.save()

        # Professional
        professional.current_designation = request.POST.get('current_designation')
        professional.current_company = request.POST.get('current_company')
        professional.industry = request.POST.get('industry')
        year_exp = request.POST.get('year_of_experience')
        professional.year_of_experience = int(year_exp) if year_exp else None
        professional.company_location = request.POST.get('company_location')
        professional.linkedin_profile = request.POST.get('linkedin_profile')
        professional.career_highlights = request.POST.get('career_highlights')
        professional.save()

        # Contact
        contact.email = request.POST.get('contact_email')
        contact.phone_number = request.POST.get('phone_number')
        contact.alternate_phone = request.POST.get('alternate_phone')
        contact.save()

        # Engagement
        engagement.membership_status = request.POST.get('membership_status')

        events = request.POST.get('events_attended')
        engagement.events_attended = int(events) if events else None

        engagement.mentorship_interest = bool(request.POST.get('mentorship_interest'))
        engagement.donation_amount = request.POST.get('donation_amount') or None
        engagement.volunteer_activities = request.POST.get('volunteer_activities')
        engagement.newsletter_subscription = bool(request.POST.get('newsletter_subscription'))

        engagement.save()

        return redirect('dashboard')

    return render(request, 'alumni/edit_profile.html', {
    'profile': profile,
    'academic': academic,
    'professional': professional,
    'contact': contact,
    'engagement': engagement,
})

from django.db.models import Q
from admin_module.models import SystemMetadata

@login_required
def alumni_directory(request):

    query = request.GET.get('q')
    department = request.GET.get('department')

    profiles = AlumniProfile.objects.all()

    # Show only verified alumni
    verified_users = SystemMetadata.objects.filter(
        verified_by_admin=True
    ).values_list('user', flat=True)

    profiles = profiles.filter(user__in=verified_users)

    if query:
        profiles = profiles.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    if department:
        profiles = profiles.filter(
            user__academicdetails__department__icontains=department
        )

    return render(request, 'alumni/alumni_directory.html', {
        'profiles': profiles
    })


@login_required
def view_profile(request, user_id):

    metadata = SystemMetadata.objects.filter(
        user_id=user_id,
        verified_by_admin=True
    ).first()

    if not metadata:
        return redirect('alumni_directory')

    profile = AlumniProfile.objects.get(user_id=user_id)
    academic = AcademicDetails.objects.get(user_id=user_id)
    professional = ProfessionalDetails.objects.get(user_id=user_id)
    contact = ContactDetails.objects.get(user_id=user_id)

    return render(request, 'alumni/view_profile.html', {
        'profile': profile,
        'academic': academic,
        'professional': professional,
        'contact': contact,
    })


def complete_profile(request):

    if request.method == "POST":
        try:
            with transaction.atomic():

                # ===== PERSONAL PROFILE =====
                profile, created = AlumniProfile.objects.get_or_create(
                    user=request.user
                )

                profile.first_name = request.POST.get("first_name", "")
                profile.last_name = request.POST.get("last_name", "")
                profile.gender = request.POST.get("gender", "")
                profile.date_of_birth = request.POST.get("date_of_birth") or None
                profile.address = request.POST.get("address", "")
                profile.city = request.POST.get("city", "")
                profile.state = request.POST.get("state", "")
                profile.country = request.POST.get("country", "")
                profile.postal_code = request.POST.get("postal_code", "")

                if request.FILES.get("photo"):
                    profile.photo = request.FILES.get("photo")

                profile.save()

                # ===== ACADEMIC DETAILS =====
                academic, created = AcademicDetails.objects.get_or_create(
                    user=request.user
                )

                academic.student_id = request.POST.get("student_id", "")
                academic.degree = request.POST.get("degree", "")
                academic.department = request.POST.get("department", "")
                academic.year_of_admission = request.POST.get("year_of_admission") or None
                academic.year_of_graduation = request.POST.get("year_of_graduation") or None

                academic.save()

                # ===== PROFESSIONAL DETAILS =====
                professional, created = ProfessionalDetails.objects.get_or_create(
                    user=request.user
                )

                professional.current_designation = request.POST.get("current_designation", "")
                professional.current_company = request.POST.get("current_company", "")
                professional.industry = request.POST.get("industry", "")
                professional.year_of_experience = request.POST.get("year_of_experience") or 0
                professional.company_location = request.POST.get("company_location", "")
                professional.linkedin_profile = request.POST.get("linkedin_profile", "")

                professional.save()

                # ===== CONTACT DETAILS =====
                contact, created = ContactDetails.objects.get_or_create(
                    user=request.user
                )

                contact.phone_number = request.POST.get("phone_number", "")
                contact.alternate_phone = request.POST.get("alternate_phone", "")
                contact.email = request.user.email

                contact.save()

                messages.success(request, "Profile submitted. Waiting for approval.")
                return redirect("waiting_approval")

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect("complete_profile")

    return render(request, "alumni/complete_profile.html")

def waiting_approval(request):
    return render(request, "auth/waiting_approval.html")