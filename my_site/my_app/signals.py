# created on 1/6/20

# formatted on 5/6/20
# by Darshan Bajania
# this file helps in creating a new django user every time a new registration is done
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Mentors


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Mentors.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.Profile.save()
