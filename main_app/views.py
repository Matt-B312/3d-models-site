from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Account, Comment, Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import uuid
import boto3
import os
from dotenv import load_dotenv


from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from .forms import UploadFileForm
# from .forms import ModelFormWithFileField
import os


# Add these "constant" variables below the imports
S3_BASE_URL = os.getenv('S3_BASE_URL')
S3_LINK_URL = os.getenv('S3_LINK_URL')
BUCKET = os.getenv('BUCKET')

def add_photo(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_LINK_URL}{key}"
            # url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return render(request, 'home.html')
    # return redirect('posts', post_id=post_id)

# Create your views here.

def home(request):
    post_list = Post.objects.all()
    print(os.getenv('NAME'))
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #save user to DB
            user = form.save()
            #login the user
            login(request, user)
            Account.objects.create(user=request.user)
            return redirect('/')
        else:
            error_message = "Invalid Sign Up Submission - Try Again"
    form = UserCreationForm()
    context = {'form':form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# def upload_file(request):
#     if request.method == 'POST':
#         form = ModelFormWithFileField(request.POST, request.FILES)
#         if form.is_valid():
#             # file is saved
#             form.save()
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = ModelFormWithFileField()
#     return render(request, 'upload.html', {'form': form})

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    # fields = '__all__'
    fields = ['title','files','images','text_content','tags','type']
    
    #overriding in child class
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_absolute_url(self):
        return redirect("post", post_id=self.id)
        # return reverse("/", kwargs={"post_id": self.id})
    
    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','files','images','text_content','tags','type']
    

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"    
    
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    # fields = '__all__'
    fields = ['title','files','images','text_content','tags','type']
    
    
    
    #overriding in child class
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_absolute_url(self):
        return reverse("/", kwargs={"post_id": self.id})
    
    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','files','images','text_content','tags','type']
    success_url = "/posts/"
    

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/posts/" 
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    
# def posts_details(request, post_id):
#     posts = Post.objects.get(id=post_id)
#     return render(request, 'posts.html', post_id=post_id)

  
class PostList(LoginRequiredMixin, ListView):
    model = Post
    
        
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    # fields = '__all__'
    fields = ['title','images','text_content']
    
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        print("initial test",initial)
        return initial
    
    
    #overriding in child class
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_absolute_url(self):
        return reverse("/", kwargs={"post_id": self.id})