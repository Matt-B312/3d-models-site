from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Comment, Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, path
import uuid
import boto3
import os
from dotenv import load_dotenv
from django.db.models import Q



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
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))
    # return redirect('posts', post_id=post_id)

# Create your views here.

def home(request):
    post_list = Post.objects.all()
    
    return render(request, 'home.html', {'post_list': post_list})


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

def add_model(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('model', None)
    print("photo file test",photo_file)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print("key test", key)
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_LINK_URL}{key}"
            # print("url test",url)
            photo = Photo(url=url, post_id=post_id)
            post = Post.objects.get(id=post_id)
            # print("post test",post.model)
            # print("photo url",photo.url)
            post.model = photo.url
            photo.save()
            post.save()
        except:
            print('An error occurred uploading file to S3')
        
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    # fields = '__all__'
    fields = ['title','model','text_content','tags','type']
    success_url = '/main_app/templates/home.html'
    
    #overriding in child class
    def form_valid(self, form, *args,**kwargs):
        print("POST Test",self.request.POST)
        form = Post(title=self.request.POST.get('title'),text_content=self.request.POST.get('text_content'),tags=self.request.POST.get('tags') )
        form.user_id = self.request.user.id
        form.save()
        add_model(self.request, form.id)
        post = Post.objects.get(id=form.id)
        print("post test",post.title)
        return HttpResponseRedirect(reverse('post_detail', args=[form.id]))
         
        

    
    
    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','model','text_content','tags','type']
    

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"   
    
    

# class PostDetail(LoginRequiredMixin, DetailView):
#     model = Post
def detail(request, pk):
    post = Post.objects.get(id=pk)
    if request.user in Post.objects.get(id=pk).likes.all():
        liked = True
    else:
        liked = False
    print(Post.objects.get(id=pk).likes.all())
    return render(request,'main_app/post_detail.html',{'post': post, 'liked': liked})

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
        # comment = form.save(commit=False)
        # comment.post = 
        form.instance.post_id = self.kwargs.get('pk')
        # print("HELLO:", form.instance.post_id)
        # print("HI THERE:", self.kwargs.get('pk'))
        return super(CommentCreate, self).form_valid(form)
    
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['title','images','text_content']
    
class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))  

def LikeView(request, pk):
    print("POST", Post)
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def UnlikeView(request, pk):
    print("POST", Post)
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print('before',post.likes)
    post.likes.remove(request.user)
    print('after', post.likes)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def SearchPost(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(Q(tags__contains=searched)| Q(title__contains=searched))
        return render(request, 'main_app/post_search.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'main_app/post_search.html', {})
