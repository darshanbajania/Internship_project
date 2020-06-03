from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='Profile')
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpeg',upload_to='profile_pic')
    pdfs = models.FileField(default='user.pdf',upload_to="props/pdfs")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

    