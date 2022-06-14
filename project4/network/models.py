from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Newpost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content}, {self.date}, {self.user}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followuser")
    follower = models.ManyToManyField(User, blank=True, related_name="follower")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    
    def __str__(self):
        return f"{self.user}, {self.follower}, {self.following}"
