from django.contrib import admin
from django.urls import path
from facedetection import views

urlpatterns = [
    path('',views.home,name="home"),
    path('add_student_page',views.add_student_page,name="add_student_page"),
    path('add_course_page',views.add_course_page,name="add_course_page"),
    path('add_students',views.add_students,name="add_students"),
    path('add_course',views.add_course,name="add_course"),
    path('take_attendance',views.take_attendance,name="take_attendance"),
    path('courses',views.courses,name="courses"),
    path('attendance/<int:id>',views.attendance,name="attendance"),
    path('download_attendance_sheet/<int:id>',views.download_attendance_sheet, name='download_attendance_sheet'),
]