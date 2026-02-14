from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SystemMetadata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    verified_by_admin = models.BooleanField(default=False)
    profile_completion = models.IntegerField(default=0)

    def __str__(self):
        return f"Metadata - {self.user.username}"