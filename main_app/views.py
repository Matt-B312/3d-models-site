

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os


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