from django import forms
from django.forms import ModelMultipleChoiceField

from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'heading', 'text']
