from django.urls import path
from .views import PostList, PostDetail, PostSearchList, ArticleOrNewsCreate, ArticleOrNewsUpdate, PostDelete
from .views import upgrade_me

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearchList.as_view()),
    path('create/', ArticleOrNewsCreate.as_view(), name='news_create'),
    path('article/create/', ArticleOrNewsCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', ArticleOrNewsUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/update/', ArticleOrNewsUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('upgrade/', upgrade_me, name='upgrade')
]
