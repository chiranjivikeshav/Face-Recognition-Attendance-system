from django.contrib import admin
from django.urls import path
from facedetection import views

urlpatterns = [
    path('',views.home,name="home"),
    path('add_student_page',views.add_student_page,name="add_student_page"),
    path('add_course_page',views.add_course_page,name="add_course_page"),
    path('add_students',views.add_students,name="add_students"),
    path('add_course',views.add_course,name="add_course"),
]