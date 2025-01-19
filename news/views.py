from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .forms import PostForm
from .models import *
from .filters import PostFilter

class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearchList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'flatpages/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'
