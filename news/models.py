from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

article = 'AR'
news = 'NE'
TYPE = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField('Рейтинг автора', default=0)

    def update_rating(self):
        posts_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0)).get('cr')
        posts_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'), 0)).get('pcr')

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()
        return


class Category(models.Model):
    name = models.CharField('Название категории', max_length=25, unique=type)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='posts')
    article_or_news = models.CharField('Статья или новость', max_length=2, choices=TYPE)
    date_time = models.DateTimeField('Дата и время', auto_now=True)
    category = models.ManyToManyField(Category,  through='PostCategory')
    heading = models.CharField('Заголовок', max_length=250)
    text = models.TextField('Текст')
    rating = models.IntegerField('Рейтинг статьи', default=0)

    def preview(self):
        return f'{self.text[:124]}...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.heading

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField('Текст')
    date_time = models.DateTimeField('Дата и время', auto_now=True)
    rating = models.IntegerField('Рейтинг омментария', default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
