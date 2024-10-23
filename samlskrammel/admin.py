from django.contrib import admin

# Register your models here.
from .models import Friend, Post

@admin.register(Friend)
class FriendModelAdmin(admin.ModelAdmin):
    list_display = ['myOwner', 'myFriend']

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['myOwner', 'myWhat', 'myWhen', 'myWeight']
