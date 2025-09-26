from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class NGO(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    email = models.EmailField()
    ngoid = models.IntegerField()
    profile = models.ImageField(upload_to="ngo/", null=True, blank=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    email = models.EmailField()
    phone = models.IntegerField(
        validators=[MinValueValidator(0000000000), MaxValueValidator(9999999999)]
    )
    fssai = models.IntegerField()
    profile = models.ImageField(upload_to="rest/", null=True, blank=True)

    def __str__(self):
        return self.name


class Donation(models.Model):
    """
    Represents a single food donation listed by a restaurant.
    """
    STATUS_CHOICES = [
        ('Ld', 'Listed'),
        ('Clmd', 'Claimed'),
        ('PkUp', 'Picked Up'),
    ]

    # Links to the restaurant that made the donation. If the restaurant is deleted, their donations are too.
    rest = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, blank=True, null=True)

    # Details of the food item
    dish = models.CharField(max_length=200)
    qty = models.IntegerField(validators=[MinValueValidator(1)], help_text="Number of servings")

    # Pickup and status information
    pickup_datetime = models.DateTimeField()
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='Ld')

    # Links to the NGO that claimed the donation. Can be empty if unclaimed.
    claimed_ngo = models.ForeignKey(NGO, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.dish} from {self.rest.name} ({self.get_status_display()})"


class CustomUser(AbstractUser):
    type = models.CharField(
        choices=[
            ("NGO", "NGO"),
            ("Rest", "Restaurant"),
        ]
    )

    ngo = models.ForeignKey(NGO, on_delete=models.SET_NULL, blank=True, null=True)
    rest = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, blank=True, null=True
    )
