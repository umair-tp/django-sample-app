from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Bookmark(models.Model):
    title = models.TextField(max_length=200, default="Bookmark")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    url = models.TextField(max_length=200, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title