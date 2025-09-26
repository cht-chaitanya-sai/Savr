from django.db import models
from accounts.models import Restaurant


class Orders(models.Model):
    dish=models.CharField(max_length=100)
    qty=models.IntegerField()
