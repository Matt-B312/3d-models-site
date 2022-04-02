from audioop import reverse
from distutils.command.upload import upload
from django.db import models
from django.forms import ImageField
from pkg_resources import to_filename
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



##Account

# class User(AbstractUser):
#     picture = models.CharField(default=None, blank=True, null=True, max_length=2000)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def get_absolute_url(self):
#         return reverse('detail', kwargs = {'account_id': self.id})
    
#     def __str__(self):
#         return self.username

class Account(models.Model):
    picture = models.CharField(default='https://i.imgur.com/VKXouC4.png', blank=True, null=True, max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes = models.ManyToManyField(Comment)

    def get_absolute_url(self):
        return reverse('detail', kwargs = {'account_id': self.id})
    
    def __str__(self):
        return self.user['username']




    

##Post

class Post(models.Model):
    title = models.CharField(max_length=100)
    files = models.FileField(blank=True, null=True, upload_to="models/%Y/%m/$D/")
    images = models.CharField(max_length=2000, default=None, blank=True, null=True )
    text_content = models.TextField(max_length=1000, default=None, blank=True, null=True)
    tags = models.TextField(max_length=1000, default=None, blank=True, null=True)
    downloads = models.IntegerField(default=0)
    type = models.CharField(max_length=50, default="STL")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)

    # comments = models.ManyToManyField(Account)
    # favorites = models.ManyToManyField(Account)
    
## Comment
class Comment(models.Model):
    images = models.CharField(max_length=2000, default=None, blank=True, null=True)
    text_content = models.CharField(max_length=3000)
    title = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)