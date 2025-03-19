from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import PostForm, SubscribeForm
from .models import *
from .filters import PostFilter
from .signals import new_post_message


class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        x = self.request.user
        y = self.object.category.all()
        context['category_post_all'] = y
        context['not_available_in_the_database'] = not SubscribCategory.objects.filter(user=x, category__in=y).exists()
        return context


class ArticleOrNewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_news_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            post.article_or_news = 'NE'
        elif self.request.path == '/news/article/create/':
            post.article_or_news = 'AR'
        post.save()
        new_post_message.delay(self)
        return super().form_valid(form)


class ArticleOrNewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_news_create.html'
    permission_required = ('news.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


class SubscribCategoryCreate(CreateView):
    form_class = SubscribeForm
    model = SubscribCategory
    template_name = 'flatpages/subscrib.html'

    def form_valid(self, form):
        sub = form.save(commit=False)
        sub.user = self.request.user
        if self.request.path == '/news/subscribe/1':
            sub.category = Category.objects.get(id=1)
        elif self.request.path == '/news/subscribe/2':
            sub.category = Category.objects.get(id=2)
        elif self.request.path == '/news/subscribe/3':
            sub.category = Category.objects.get(id=3)
        elif self.request.path == '/news/subscribe/4':
            sub.category = Category.objects.get(id=4)
        sub.save()
        return super().form_valid(form)
