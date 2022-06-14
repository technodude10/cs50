from django.contrib import admin
from .models import User, Newpost, Follow


class NewpostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "date")

class FollowAdmin(admin.ModelAdmin):
    filter_horizontal = ("follower", "following")

# Register your models here.
admin.site.register(User)
admin.site.register(Newpost, NewpostAdmin)
admin.site.register(Follow, FollowAdmin)