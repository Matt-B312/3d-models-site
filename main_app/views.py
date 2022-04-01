from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Account, Comment, Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from .forms import UploadFileForm
# from .forms import ModelFormWithFileField
import os

# Create your views here.

def home(request):
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