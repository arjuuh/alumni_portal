from django.db import models
from django.contrib.auth.models import User


class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class AcademicDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    degree = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    college_name = models.CharField(max_length=200)
    year_of_admission = models.IntegerField()
    year_of_graduation = models.IntegerField()


class ProfessionalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_designation = models.CharField(max_length=100)
    current_company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    year_of_experience = models.IntegerField()
    company_location = models.CharField(max_length=200)
    linkedin_profile = models.URLField()


class ContactDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)


class AlumniEngagement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_status = models.CharField(max_length=50)
    events_attended = models.IntegerField(default=0)
    mentorship_interest = models.BooleanField(default=False)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volunteer_activities = models.TextField(blank=True)
    newsletter_subscription = models.BooleanField(default=True)
