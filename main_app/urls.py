from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), #in views folder use home view

    
    
    #POSTs
    path('posts/create', views.PostCreate.as_view(), name="posts_create"),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name="posts_update"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="posts_delete"),
    
    
    #URL path for signup
    path('account/signup',views.signup,name='signup'),

    path('upload/', views.upload, name='upload'),
    
    ]   