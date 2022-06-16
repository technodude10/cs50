from django.contrib import admin
from .models import Like, User, Newpost, Follow


class NewpostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "date")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "profile", "follow")
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "like")



# Register your models here.
admin.site.register(User)
admin.site.register(Newpost, NewpostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)