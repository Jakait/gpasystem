from django.urls import path
from . import views

# to be edited to desired routes
urlpatterns = [
    path('', views.signin, name="login"),
    path('signout/', views.signout, name="signout"),
    path('usereg/', views.registerUser, name = "adduser"),
     path('useredit/<int:id>/', views.editUser, name = "edituser"),
       path('userdelete/<int:id>/', views.deleteUser, name = "deleteuser"),
    path('userview/', views.viewUser, name = "viewuser"),
    path('dashboard/', views.dashboard, name = "home"),
    path('unitedit/<int:id>/', views.editUnit, name = "editunit"),
    path('courseedit/<int:id>/', views.editCourse, name = "editcourse"),
    path('regcourse/', views.registerCourse, name = "addcourse"),
    path('coursedelete/<int:id>/', views.deleteCourse, name = "deletecourse"),
    path('unitdelete/<int:id>/', views.deleteUnit, name = "deleteunit"),
    path('regresults/', views.registerResults, name = "addresults"),
    path('fetchunits/', views.fetchstudentsunit, name = "studentunits"),
    path('viewresults/', views.viewResults, name = "viewresults"),
     path('examedit/<int:id>/', views.editExam, name = "editexam"),
     path('examdelete/<int:id>/', views.deleteExam, name = "deletexam"),
    path('displaymarks/', views.displayResults, name = "displaymarks"),
    path('viewcourse/', views.viewCourse, name = "viewcourse"),
    path('asynfetch/', views.fetchCourse, name = "fetchcourse"),
    path('asynfetchview/', views.fetchCourseView, name = "fetchcourseview"),
    path('usercourse/', views.userCourse, name = "fetchuserCourse"),
    path('displayreport/', views.displayReport, name = "displayreport"),
    path('report/', views.report, name = "report"),

    
    
]