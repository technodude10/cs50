from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    bid = models.FloatField(default=0)
    url = models.URLField(max_length=200)
    category = models.CharField(max_length=200) 
    open_or_close = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userid")
    def __str__(self):
        return f"{self.title}, {self.desc}, {self.bid}, {self.url}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userwatchlist")
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listwatchlist") 
    def __str__(self):
        return f"{self.user}, {self.list}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  default='0', related_name="user")
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, default='0', related_name="list")
    bid_value = models.FloatField(default='0')
    def __str__(self):
        return f"{self.user}, {self.list}, {self.bid_value}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  default='0', related_name="comment_user")
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, default='0', related_name="comment_list")
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}, {self.list}, {self.comment}, {self.date}"

