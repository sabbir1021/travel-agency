from django.db import models

# Create your models here.


class Location(models.Model):
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
