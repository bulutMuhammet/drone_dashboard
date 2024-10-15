from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Staff

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)