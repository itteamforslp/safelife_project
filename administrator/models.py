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
        db_table = 'course_students'


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teachers = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.teachers)

    class Meta:
        db_table = 'course_teachers'


class Class(models.Model):
    class_id = models.AutoField(max_length=5, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

    class Meta:
        db_table = 'classes'
#
#    def save(self, *args, **kwargs):
#        created = not self.pk
#        super().save(*args, **kwargs)
#        print("Pre work")
#        if created:
#            print("right before creation!")
#            print(CourseStudent.course)
#            print(CourseStudent.students)
#            Attendance.objects.create(course = CourseStudent.course , student = CourseStudent.students, status = False, date = self.date)
#            print("Created attendance!")

class Attendance(models.Model):
   # classroom = models.ForeignKey(Class, related_name='class_identitfication', on_delete=models.CASCADE) 
    course = models.ForeignKey(Course, related_name='course_identifier', on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT)
    status = models.BooleanField(default = False)
    date = models.DateField()#ForeignKey(Class, null = True, blank = True, on_delete=models.CASCADE)

   # def save(self, *args, **kwargs):
   #     if self.date is None:
   #         self.date = Class.date
   #     super(Attendance, self).save(*args, **kwargs)




    class Meta:
        db_table = 'attendances'

 #date = models.DateField()
    #students = models.CharField(max_length=5)
    #classes = models.CharField(max_length=5)
    #status = models.CharField(max_length=50)

#def create_attendance(sender,instance, created, **kwargs):
#    print("Attempting to create attendance!")
#    if created:
#        print("Attempting still!")
#        Attendance.objects.create(course = kwargs['instance'].course, student = kwargs['instance'].students, status = False)
#
#post_save.connect(create_attendance, sender=CourseStudent)
   # if created == False:
   #     instance.Attendance.save()
   #     print('Attendance updated!')