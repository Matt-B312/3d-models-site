from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), #in views folder use home view

    
    
    #POSTs
    path('posts/create', views.PostCreate.as_view(), name="post_create"),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name="post_update"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_details'),
    path('posts/', views.PostList.as_view(),name="posts_index"),
    
    
    #COMMENTS
    path('posts/<int:pk>/comments/create', views.CommentCreate.as_view(), name="comment_create"),
    
    
    #URL path for signup
    path('account/signup',views.signup,name='signup'),

    path('upload/', views.upload, name='upload'),
    
    ]   