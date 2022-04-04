# from attr import fields
from .models import Comment
from django import forms
from django.forms import ModelForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'images', 'text_content')