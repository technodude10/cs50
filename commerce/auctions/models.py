from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    bid = models.IntegerField()
    url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.title}, {self.desc}, {self.bid}, {self.url}"

class Bid(models.Model):
    pass

class Comments(models.Model):
    pass