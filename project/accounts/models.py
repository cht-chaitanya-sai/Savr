from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class NGO(models.Model):
    name=models.CharField(max_length=100)
    location=models.TextField()
    email=models.EmailField()
    ngoid=models.IntegerField()
    profile=models.ImageField(upload_to="ngo/")


class Restaurant(models.Model):
    name=models.CharField(max_length=100)
    location=models.TextField()
    email=models.EmailField()
    phone=models.IntegerField(validators=[MinValueValidator(0000000000), MaxValueValidator(9999999999)])
    fssai=models.IntegerField()
    profile=models.ImageField(upload_to="rest/")


class CustomUser(AbstractUser):
    type=models.CharField(choices = [
            ('NGO', 'NGO'),
            ('Rest', 'Restaurant'),
        ]
    )

    ngo = models.ForeignKey(NGO, blank=True, null=True)
    rest = models.ForeignKey(Restaurant, blank=True, null=True)
