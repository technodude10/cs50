from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    bid = models.FloatField()
    url = models.URLField(max_length=200)
    category = models.CharField(max_length=200, blank=True) 
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userid")
    def __str__(self):
        return f"{self.title}, {self.desc}, {self.bid}, {self.url}"

class Bid(models.Model):
    pass

class Comments(models.Model):
    pass