from django.urls import path
from . import views

# to be edited to desired routes
urlpatterns = [
    path('', views.index),
    path('usereg/', views.registerUser),
]