from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
    context_object_name = 'posts_search'
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


class ArticleOrNewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            post.article_or_news = 'NE'
        elif self.request.path == '/news/article/create/':
            post.article_or_news = 'AR'
        post.save()
        return super().form_valid(form)


class ArticleOrNewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_news_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')



