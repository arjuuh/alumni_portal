from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SystemMetadata(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    profile_completion = models.IntegerField(default=0)

    def __str__(self):
        return f"Metadata - {self.user.username}"