from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import AlumniProfile, AcademicDetails, ProfessionalDetails, ContactDetails
from django.contrib.auth.decorators import login_required
from admin_module.models import SystemMetadata
from .models import AlumniEngagement


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

    metadata, _ = SystemMetadata.objects.get_or_create(user=request.user)

    if not metadata.verified_by_admin:
        return render(request, 'not_verified.html')

    profile, _ = AlumniProfile.objects.get_or_create(user=request.user)
    academic, _ = AcademicDetails.objects.get_or_create(user=request.user)
    professional, _ = ProfessionalDetails.objects.get_or_create(user=request.user)
    contact, _ = ContactDetails.objects.get_or_create(user=request.user)
    engagement, _ = AlumniEngagement.objects.get_or_create(user=request.user)
    all_fields = [

    # Personal
    profile.first_name,
    profile.last_name,
    profile.gender,
    profile.date_of_birth,
    profile.address,
    profile.city,
    profile.state,
    profile.country,
    profile.postal_code,

    # Academic
    academic.student_id,
    academic.degree,
    academic.department,
    academic.college_name,
    academic.year_of_admission,
    academic.year_of_graduation,
    academic.achievements,

    # Professional
    professional.current_designation,
    professional.current_company,
    professional.industry,
    professional.year_of_experience,
    professional.company_location,
    professional.linkedin_profile,
    professional.career_highlights,

    # Contact
    contact.email,
    contact.phone_number,
    contact.alternate_phone,
]

    filled = sum(1 for field in all_fields if field)
    total = len(all_fields)
    completion_percentage = int((filled / total) * 100) if total > 0 else 0

    return render(request, 'dashboard.html', {
    'profile': profile,
    'academic': academic,
    'professional': professional,
    'contact': contact,
    'engagement': engagement,
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
        academic.college_name = request.POST.get('college_name')
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

    return render(request, 'edit_profile.html', {
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

    return render(request, 'alumni_directory.html', {
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

    return render(request, 'view_profile.html', {
        'profile': profile,
        'academic': academic,
        'professional': professional,
        'contact': contact,
    })
