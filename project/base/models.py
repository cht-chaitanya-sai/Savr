from django.db import models
from accounts.models import Restaurant, NGO


class Orders(models.Model):
    dish=models.CharField(max_length=100)
    qty=models.IntegerField()
    rest=models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    pickup_datetime=models.DateTimeField()
    status=models.CharField(default="Ld", choices=[
        ('Ld', 'Listed'),
        ('Clmd', 'Claimed'),
        ('Clcd', 'Collected')
    ])
    claimed_ngo=models.ForeignKey(NGO, on_delete=models.SET_NULL, blank=True, null=True)
    