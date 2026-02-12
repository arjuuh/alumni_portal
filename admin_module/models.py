from django.db import models
from django.contrib.auth.models import User


class SystemMetadata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_by_admin = models.BooleanField(default=False)
    profile_completion = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
