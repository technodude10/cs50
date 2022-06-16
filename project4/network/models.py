from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "id": self.id,
            "user": self.username
        }

class Newpost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=400)
    like = models.ManyToManyField(User, blank=True, related_name="like")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content}, {self.date}, {self.user}, {self.like}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content
        }

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followuser")
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followprofile")
    follow = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user}, {self.profile}, {self.follow}"
    
    def serialize(self):
        return {
            "follow": self.follow
        }

