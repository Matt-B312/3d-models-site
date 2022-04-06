from django.urls import path
from . import views
from .views import LikeView, UnlikeView, SearchPost

urlpatterns = [
    path('', views.home, name="home"), #in views folder use home view

    
    
    #POSTs
    path('posts/create', views.PostCreate.as_view(), name="post_create"),
    path('posts', views.posts_index, name="posts_index"),
    path('posts/user', views.user_posts_index, name="user_posts_index"),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name="post_update"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('posts/<int:pk>/', views.detail, name='post_detail'),
    # path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('posts/', views.PostList.as_view(),name="posts_index"),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('posts/<int:post_id>', views.posts_details, name="post_details"),
    path('posts/search/', views.SearchPost, name='search_post'),

    path('like/<int:pk>/', views.LikeView, name='like_post'),
    path('unlike/<int:pk>/', views.UnlikeView, name='unlike_post'),
    
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='post_details'),
    
    
    #COMMENTS
    # path('posts/<int:pk>/comments/create', views.CommentCreate.as_view(), name="comment_create"),
    path('post/<int:pk>/comment/', views.CommentCreate.as_view(), name='comment_create'),
    path('post/<int:pk>/comment/update/', views.CommentUpdate.as_view(), name="comment_update"),   
    path('post/<int:pk>/comment/delete/', views.CommentDelete.as_view(), name="comment_delete"),
    
    #URL path for signup
    path('account/signup',views.signup,name='signup'),
    path('account/edit_profile',views.edit_profile,name='edit_profile'),

    # path('upload/', views.upload, name='upload'),
    
    path('profile/', views.profile, name='profile'),
    
    ]   