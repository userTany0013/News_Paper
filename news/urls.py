from django.urls import path
from .views import PostList, PostDetail, PostSearchList, NewsCreate

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', PostSearchList.as_view()),
    path('create/', NewsCreate.as_view(), name='news_create'),
]
