from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Comment(models.Model):
    MODELS = (
        ('b', 'blog'),
        ('p', 'photo'),
    )

    text = models.TextField(max_length=200, null=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    is_active = models.BooleanField(default=True)
    model = models.CharField(max_length=1, choices=MODELS, null=False)
    object_id = models.IntegerField(null=False)

    def __str__(self):
        return self.model + " : " + self.text