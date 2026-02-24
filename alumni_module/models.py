from django.db import models
from django.contrib.auth.models import User

class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Info
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    # Address Info
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class AcademicDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    student_id = models.CharField(max_length=50, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year_of_admission = models.IntegerField(null=True, blank=True)
    year_of_graduation = models.IntegerField(null=True, blank=True)
    achievements = models.TextField(blank=True)


class ProfessionalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    current_designation = models.CharField(max_length=100, blank=True)
    current_company = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    year_of_experience = models.IntegerField(null=True, blank=True)
    company_location = models.CharField(max_length=200, blank=True)
    linkedin_profile = models.URLField(blank=True)
    career_highlights = models.TextField(blank=True)


class ContactDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)

class AlumniEngagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    membership_status = models.CharField(max_length=50, blank=True)
    events_attended = models.IntegerField(null=True, blank=True)
    mentorship_interest = models.BooleanField(default=False)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volunteer_activities = models.TextField(blank=True)
    newsletter_subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"Engagement - {self.user.username}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"    