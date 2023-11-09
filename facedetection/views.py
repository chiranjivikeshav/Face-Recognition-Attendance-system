import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Students,Course,Attendance
import face_recognition
import pandas as pd
import json
from django.contrib import messages
import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from io import BytesIO
from retinaface import RetinaFace


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
                messages.success(request,'Student added into University Database')
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
        messages.success(request,'Course added into University Database')
        for roll_number in student_roll_numbers:
            try:
                student = Students.objects.get(Roll_no=roll_number)
                course.students.add(student)
            except Students.DoesNotExist:
                pass

        return redirect('home') 
    return render(request, 'add_course.html')




def cosine_distance(vector_a, vector_b):
    return 1 - cosine_similarity([vector_a], [vector_b])[0][0]

def detect_faces_and_embeddings(image_data):
    # Load the image using RetinaFace for face detection
    img = Image.open(BytesIO(image_data))
    img_array = np.array(img)
    obj = RetinaFace.detect_faces(img_array)
    face_encodings = []

    for key in obj.keys():
        identity = obj[key]
        x, y, w, h = identity['facial_area']
        face_img = img_array[y:y + h, x:x + w]

        rgb_face_img = Image.fromarray(face_img).convert('RGB')
        rgb_face_array = np.array(rgb_face_img)
        
        face_encoding = face_recognition.face_encodings(rgb_face_array)

        if face_encoding:
            face_encodings.append(face_encoding[0])
    return face_encodings

def take_attendance(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        image = request.FILES.get('image').read()

        # Load the course and students
        course = Course.objects.get(id=course_id)
        students = course.students.all()
        attendance_count = int(course.attendece_count)+1
        course.attendece_count =attendance_count
        course.save()
        # Detect faces and calculate embeddings in the uploaded image
        recognized_embeddings = detect_faces_and_embeddings(image)
      
        # Match recognized faces with students using cosine distance
        for recognized_embedding in recognized_embeddings:
            for student in students:
                if student.face_embedding:
                    student_embedding = np.array(student.get_face_embedding())
                    distance = cosine_distance(student_embedding, recognized_embedding)
                    if distance < 0.07:
                        existing_attendance = Attendance.objects.filter(
                            student=student,
                            course=course,
                            date=date
                        )
                        if not existing_attendance:
                             Attendance.objects.create(student=student, course=course, date=date, attendance=True)
        messages.success(request,'Attendance Taken Successfully')
    courses = Course.objects.all()
    return render(request, 'take_attend.html', {'courses': courses})

def courses(request):
    courses = Course.objects.all()
    return render(request,'course.html',{'courses': courses})

def attendance(request,id):
    course = Course.objects.get(pk=id)
    students = course.students.all()

    attendance_data = []
    for student in students:
        attendance_percentage = course.attendance_percentage(student)
        attendance_data.append({
            'student': student,
            'attendance_percentage': attendance_percentage,
        })

    context = {'course': course, 'attendance_data': attendance_data}
    return render(request, 'attendance.html', context)



def download_attendance_sheet(request,id):
    if request.method == 'POST':
        course_id = id
        date = request.POST.get('date')
        attendance_data = Attendance.objects.filter(course=course_id, date=date)
        # Create CSV content
        csv_content = "Roll No,Student Name,Attendance\n"
        for attendance_record in attendance_data:
            csv_content += f"{attendance_record.student.Roll_no},{attendance_record.student.Name},{attendance_record.attendance}\n"
        # Create response object with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendance_sheet_{date}_{course_id}.csv"'
        response.write(csv_content)
        return response
    messages.success(request,'Attendance Sheet Downloaded Successfully')
    return redirect('attendance',id)



