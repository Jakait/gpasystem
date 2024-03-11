from django.urls import path
from . import views

# to be edited to desired routes
urlpatterns = [
    path('', views.index, name="login"),
    path('usereg/', views.registerUser, name = "adduser"),
    path('userview', views.viewUser, name = "home"),
    
]