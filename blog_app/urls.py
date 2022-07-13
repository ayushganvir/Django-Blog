from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('login/', views.login, name='post_login'),
    path('logout/', views.logout, name='post_logout'),
    path('post_maker/', views.post_maker, name='post_maker'),
    path('your_posts/', views.AuthorPosts.as_view(), name='author_posts'),
    path('register/', views.register, name='blog_app_register'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
