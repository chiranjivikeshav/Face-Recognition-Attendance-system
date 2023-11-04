import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Students,Course,Attendance
import face_recognition
import pandas as pd
import json
from django.contrib import messages

def home(request):
    return render(request,'home.html')
def add_student_page(request):
    return render(request, 'add_student.html')
def add_course_page(request):
    return render(request, 'add_course.html')

def add_students(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        image_data = request.FILES.get('image')
        if not Students.objects.filter(Roll_no=roll_number).exists():  # Check if the student already exists
            face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(image_data))
            if face_encoding:
                face_encoding_json = json.dumps(face_encoding[0].tolist())
                student = Students(Name=name, Roll_no=roll_number, face_embedding=face_encoding_json)
                student.save()
                return redirect('add_student_page')  
        else:
            messages.error(request,"Student with this roll number already exists.")
            return render(request, 'add_student.html')
    return redirect('add_student_page')




def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        text_file = request.FILES['text_file']
        student_roll_numbers = []
        for line in text_file:
            roll_number = line.decode('utf-8').strip()  
            student_roll_numbers.append(roll_number)
        course = Course(Course_name=name, Course_Code=code)
        course.save()
        for roll_number in student_roll_numbers:
            try:
                student = Students.objects.get(Roll_no=roll_number)
                course.students.add(student)
            except Students.DoesNotExist:
                pass

        return redirect('home') 
    return render(request, 'add_course.html')






