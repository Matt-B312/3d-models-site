from django.contrib import admin
from  .models import Account, Comment, Post

# Register your models here.

admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(Post)