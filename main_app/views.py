from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Comment, Post, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, path, reverse_lazy
from .forms import AccountCreate
from .forms import EditProfileForm

import uuid
import boto3
import os
from dotenv import load_dotenv

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




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
    #infiniscroll test
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list , 'posts': posts})


def posts_index(request):
    post_list = Post.objects.all()
    #infiniscroll test
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 18)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'main_app/posts_index.html', {'post_list': post_list , 'posts': posts})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        account_form = AccountCreate(request.POST)
        if form.is_valid():
            #save user to DB
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            #login the user
            login(request, user)
            Account.objects.create(user=request.user)
            return redirect('/')
        else:
            error_message = "Invalid Sign Up Submission - Try Again"
    form = UserCreationForm()
    account_form = AccountCreate()
    context = {'form':form, 'error_message': error_message , 'account_form': account_form}
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

@login_required
def profile(request):
    profile_details = Account.objects.all
    return render(request, 'registration/profile.html', {'profile_details':profile_details})


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

# class PostList(LoginRequiredMixin, ListView):
#     model = Post
    


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
    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', self.post.id)
    def delete(self, request, *args, **kwargs):
        self.book_pk = self.get_object().post.id
        return super(CommentDelete, self).delete(request, *args, **kwargs)
    
            
    
    # def get_success_url(self):
    #     comment = Comment.objects.get(id=self.id)
    #     print('comment test', comment)
    #     post = Post.objects.get(id=comment.id)
    #     print('post test', post)
    #     return self.request.GET.get('next', reverse('home'))  
    
# def form_valid(self, form, *args,**kwargs):
#         print("POST Test",self.request.POST)
#         form = Post(title=self.request.POST.get('title'),text_content=self.request.POST.get('text_content'),tags=self.request.POST.get('tags') )
#         form.user_id = self.request.user.id
#         form.save()
#         add_model(self.request, form.id)
#         post = Post.objects.get(id=form.id)
#         print("post test",post.title)
#         return HttpResponseRedirect(reverse('post_detail', args=[form.id]))
    

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
        posts = Post.objects.filter(Q(tags__icontains=searched)| Q(title__icontains=searched))
        return render(request, 'main_app/post_search.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'main_app/post_search.html', {})

class UserEditView(generic.CreateView):
    form_class = EditProfileForm
    template = 'registration/edit_profile.html'
    success_url = '/home' 

def edit_profile(request):
    error_message = ''
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            #save user to DB
            Account.objects.update(user=request.user)
            form.save()
            return redirect('/home/')
        
        else:
            error_message = "Invalid Edit Submission - Try Again"
    form = EditProfileForm(instance=request.user)
    context = {'form':form, 'error_message': error_message}
    return render(request, 'registration/edit_profile.html', context)

# def signup(request):
#     error_message = ''
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             #save user to DB
#             user = form.save()
#             #login the user
#             login(request, user)
#             Account.objects.create(user=request.user)
#             return redirect('/')
#         else:
#             error_message = "Invalid Sign Up Submission - Try Again"
#     form = UserCreationForm()
#     context = {'form':form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)

