from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.db import connection
from django.http import HttpResponseRedirect
import datetime
from django.http import JsonResponse
from administrator.models import Course, CourseTeacher, CourseStudent, Student
from django.core.exceptions import PermissionDenied


def teacher_only(function):
  #"""Limit view to teacher only."""
   def _inner(request, *args, **kwargs):
       if not request.user.is_staff == False | request.user.is_superuser:
           raise PermissionDenied           
       return function(request, *args, **kwargs)
   return _inner

@login_required(login_url = '/users')
@teacher_only
def home(request):
        current_user = request.user.id
        teacher_current_courses = Course.objects.select_related().raw('SELECT * '
                                                        'FROM course_teachers as CT, courses as C '
                                                        'WHERE CT.teachers_id = %s AND C.course_id = CT.course_id AND C.is_complete = 0 ', [current_user])

        currentdate = datetime.datetime.today().strftime('%Y-%m-%d')

        with connection.cursor() as cursor:
                cursor.execute('SELECT CL.course_id, CL.date '
                                'FROM classes as CL, course_teachers as CT '
                                'WHERE CT.teachers_id = %s AND CL.date >= %s '
                                'AND CT.course_id = CL.course_id '
                                'GROUP BY CL.course_id ', [current_user, currentdate])
    
                next_class_date = cursor.fetchall()
        
        with connection.cursor() as cursor:
                cursor.execute('SELECT CS.course_id, COUNT(CS.students_id) '
                        'FROM course_teachers as CT, course_students as CS '
                        'WHERE CT.teachers_id = %s AND CT.course_id = CS.course_id '
                        'GROUP BY CS.course_id ', [current_user])
                teacher_student_count = cursor.fetchall()

        with connection.cursor() as cursor:
                cursor.execute('SELECT C.course_id, C.notes '
                                'FROM course_teachers as CT, courses as C '
                                'WHERE CT.teachers_id = %s AND C.course_id = CT.course_id '
                                'GROUP BY CT.course_id ', [current_user])
                teacher_course_notes = cursor.fetchall()
                                                        

        template = loader.get_template('teacher/dashboard.html')
        context = {
                'teacher_current_courses': teacher_current_courses,
                'teacher_student_count': teacher_student_count,
                'next_class_date': next_class_date,
                'teacher_course_notes': teacher_course_notes
        }
    
    # Render the template to the user
        return HttpResponse(template.render(context, request))

@csrf_exempt
def update_course_notes(request):
    # Get the student name that was passed from the web page
    courseNotes = request.POST.get('courseNotes')
    courseId = request.POST.get('courseId')
    # Create a cursor to execute raw SQL queries.
    with connection.cursor() as cursor:
        cursor.execute('UPDATE courses '
                        'SET notes = %s '
                        'WHERE course_id = %s', [courseNotes, courseId])

    # Render the response to the user
  
