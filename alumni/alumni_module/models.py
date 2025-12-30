from django.db import models

class Alumni(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    batch = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
