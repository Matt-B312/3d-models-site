from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), #in views folder use home view

    
    
    #URL path for signup
    path('account/signup',views.signup,name='signup'),
    
    ]   