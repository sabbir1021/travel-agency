from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

#Signal import
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='users',null=True,blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.user_profile.save()
    except Exception as e:
        pass
