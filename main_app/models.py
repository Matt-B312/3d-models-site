from audioop import reverse
from distutils.command.upload import upload
from django.db import models
from django.forms import ImageField
from pkg_resources import to_filename
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



##Account
class Account(models.Model):
    picture = models.CharField(default=None, blank=True, null=True, max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs = {'account_id': self.id})
    
    def __str__(self):
        return self.username


##Comment

class Comment(models.Model):
    files = models.FileField()
    images = models.CharField(default=None, blank=True, null=True, max_length=2000)
    text_content = models.CharField(max_length=1000)



##Post

class Post(models.Model):
    title = models.CharField(max_length=100)
    files = models.FileField(blank=True, null=True, upload_to="models/%Y/%m/$D/")
    images = models.CharField(default=None, blank=True, null=True, max_length=2000)
    text_content = models.TextField(max_length=1000)
    tags = models.TextField(max_length=1000)
    # download = models.FileField(upload_to="documents")
    download = models.FileField()
    type = models.CharField(max_length=100)
    