from django.contrib import admin
from .models import Account, Comment, Post, Photo

# Register your models here.

admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Photo)