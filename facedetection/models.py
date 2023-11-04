from django.db import models
import json

class Course(models.Model):
    Course_name = models.CharField(max_length=50)
    Course_Code = models.CharField(max_length=10)
    students = models.ManyToManyField('Students', blank=True)
    def __str__(self):
        return self.Course_name




class Students(models.Model):
    Name = models.CharField(max_length=50)
    Roll_no = models.CharField(max_length=20)
    face_embedding = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.Name
    def set_face_embedding(self, embedding):
        self.face_embedding = json.dumps(embedding)
    def get_face_embedding(self):
        return json.loads(self.face_embedding)



class Attendance(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date = models.DateField()
    attendance = models.BooleanField(default=False)
    
     
