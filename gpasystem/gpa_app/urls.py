from django.urls import path
from . import views

# to be edited to desired routes
urlpatterns = [
    path('', views.signin, name="login"),
    path('usereg/', views.registerUser, name = "adduser"),
    path('userview/', views.viewUser, name = "viewuser"),
    path('dashboard/', views.dashboard, name = "home"),
    path('regcourse/', views.registerCourse, name = "addcourse"),
    path('regresults/', views.registerResults, name = "addresults"),
    path('fetchunits/', views.fetchstudentsunit, name = "studentunits"),
    path('viewresults/', views.viewResults, name = "viewresults"),
    path('displaymarks/', views.displayResults, name = "displaymarks"),
    path('viewcourse/', views.viewCourse, name = "viewcourse"),
    path('asynfetch/', views.fetchCourse, name = "fetchcourse"),
    path('asynfetchview/', views.fetchCourseView, name = "fetchcourseview"),
    path('usercourse/', views.userCourse, name = "fetchuserCourse"),
    
]