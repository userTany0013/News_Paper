from django.urls import path
from .views import PostList, PostDetail, PostSearchList, ArticleOrNewsCreate

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearchList.as_view()),
    path('create/', ArticleOrNewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleOrNewsCreate.as_view(), name='news_create'),
]
