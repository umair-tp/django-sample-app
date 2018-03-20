from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='media')