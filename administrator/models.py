from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save
from datetime import datetime

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
        unique_together = ["course", "students"]
        db_table = 'course_students'


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teachers = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.teachers)

    class Meta:
        unique_together = ["course", "teachers"]
        db_table = 'course_teachers'


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

    class Meta:
        unique_together = ["course", "date"]
        db_table = 'classes'
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Class, self).save(*args, **kwargs)


class Attendance(models.Model):
    attendance_id = models.CharField(max_length=50, primary_key=True)
    status = models.BooleanField(default = False)
    date = models.DateField()
    course = models.ForeignKey(Course, related_name='course_identifier', on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'attendances'
