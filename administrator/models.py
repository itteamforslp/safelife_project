from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Student(models.Model):
    student_id = models.CharField(max_length=5, primary_key=True)
    student_name = models.CharField(max_length=50)

    def __str__(self):
        return self.student_name

    class Meta:
        db_table = 'students'


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=5, primary_key=True)
    teacher_name = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher_name

    class Meta:
        db_table = 'teachers'


class Course(models.Model):
    course_id = models.CharField(max_length=5, primary_key=True)
    course_name = models.CharField(max_length=50)
    notes = models.CharField(max_length=280)
    is_complete = models.SmallIntegerField(
        default=0,
        validators=[MaxValueValidator(1), MinValueValidator(0)]
     )

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = 'courses'


class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.students)

    class Meta:
        db_table = 'course_students'


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teachers = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.teachers)

    class Meta:
        db_table = 'course_teachers'


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

    class Meta:
        db_table = 'classes'


class Attendance(models.Model):
    students = models.CharField(max_length=5)
    classes = models.CharField(max_length=5)
    status = models.CharField(max_length=50)
    date = models.DateField()
    

    class Meta:
        db_table = 'attendances'

