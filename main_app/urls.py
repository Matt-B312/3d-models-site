from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), #in views folder use home view

    
    
    #POSTs
    path('posts/create', views.PostCreate.as_view(), name="post_create"),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name="post_update"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/', views.PostList.as_view(),name="posts_index"),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('posts/<int:post_id>', views.posts_details, name="post_details"),
    
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_details'),
    
    
    #COMMENTS
    # path('posts/<int:pk>/comments/create', views.CommentCreate.as_view(), name="comment_create"),
    path('post/<int:pk>/comment/', views.CommentCreate.as_view(), name='comment_create'),   
    
    
    #URL path for signup
    path('account/signup',views.signup,name='signup'),

    path('upload/', views.upload, name='upload'),
    
    ]   