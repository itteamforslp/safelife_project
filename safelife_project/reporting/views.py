from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from administrator.models import Student, Class
from administrator.models import Course
from administrator.models import CourseStudent
from django.db import connection
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def staffCheck(function):
  #"""Limit view to teacher only."""
   def _inner(request, *args, **kwargs):
       if not request.user.is_staff is False | request.user.is_superuser:
           raise PermissionDenied           
       return function(request, *args, **kwargs)
   return _inner


@login_required(login_url='/users')
@staffCheck
def index(request):
    super = request.user.is_superuser
    current_user = request.user.id
    # Get the current date in the following format: <4 Digit Year>-<2 Digit Month>-<2 Digit Day>
    currentdate = datetime.datetime.today().strftime('%Y-%m-%d')
    # Get the name of each student that is enrolled in the class
    all_courses = Course.objects.select_related().raw('SELECT * '
                                                      'FROM courses')
                                                        
    test = CourseStudent.objects.select_related().raw('SELECT * '
                                                      'FROM course_students')

    all_students = Student.objects.select_related().raw('SELECT * '
                                                        'FROM students as S, classes as CL, attendances as A '
                                                        'WHERE CL.course_id = 306 AND S.student_id = A.students '
                                                        'AND CL.course_id = A.classes AND CL.date = A.date ')

    with connection.cursor() as cursor:
        cursor.execute('SELECT CS.course_id, S.student_name '
                       ' FROM course_students as CS, students as S, course_teachers as CT '
                       'WHERE CT.teachers_id = 1 AND CT.course_id = 306 '
                       'AND CS.course_id = CT.course_id AND CS.students_id = S.student_id ')
        cursor.execute('SELECT * FROM courses')
        course_name = cursor.fetchone()

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

    # Create a template using AdminAttendanceIndex.html, and pass into it the list of student names and recorded absences

    if super is True:
        teacher_current_courses = Course.objects.select_related().raw('SELECT * '
                                                                      'FROM courses as C '
                                                                      'WHERE C.is_complete = 0')
        template = loader.get_template('AdminIndex.html')
        context = {
            'all_courses': all_courses,
            'all_students': all_students,
            'test': test,
            'course_name': course_name,
            'next_class_date': next_class_date,
            'teacher_student_count': teacher_student_count,
            'teacher_current_courses': teacher_current_courses
        }
    else:
        # Get the list of the current teacher courses
        teacher_current_courses = Course.objects.select_related().raw('SELECT * '
                                                                      'FROM course_teachers as CT, courses as C '
                                                                      'WHERE CT.teachers_id = %s '
                                                                      'AND C.course_id = CT.course_id '
                                                                      'AND C.is_complete = 0 ', [current_user])
        template = loader.get_template('TeacherIndex.html')
        context = {
            'all_courses': all_courses,
            'all_students': all_students,
            'test': test,
            'course_name': course_name,
            'next_class_date': next_class_date,
            'teacher_student_count': teacher_student_count,
            'teacher_current_courses': teacher_current_courses
        }
    # Render the template to the user
    return HttpResponse(template.render(context, request))


def report(request, course_id, month):
    super = request.user.is_superuser
    class_dates = Class.objects.filter(course=course_id)
    class_name = Course.objects.get(course_id=course_id)

    if super is True:
        template = loader.get_template('AdminReport.html')
    else:
        template = loader.get_template('TeacherReport.html')

    if month is 0:
        all_students = Student.objects.select_related().raw('SELECT * '
                                                            'FROM students as S, classes as CL, attendances as A '
                                                            'WHERE CL.course_id = %s AND S.student_id = A.students '
                                                            'AND CL.course_id = A.classes AND CL.date = A.date '
                                                            'GROUP BY student_name', [course_id])

        status = Student.objects.select_related().raw('SELECT    * '
                                                      'FROM students as S, classes as CL, attendances as A '
                                                      'WHERE CL.course_id = %s AND CL.course_id = A.classes '
                                                      'AND CL.date = A.date '
                                                      'GROUP BY A.id '
                                                      'ORDER BY A.date ', [course_id])

        all_dates = Course.objects.select_related().raw('SELECT * '
                                                        'FROM classes '
                                                        'WHERE course_id = %s ', [course_id])
        context = {
            'course_name': class_name,
            'all_dates': all_dates,
            'class_dates': class_dates,
            'all_students': all_students,
            'status': status
        }
    else:
        all_students = Student.objects.select_related().raw('SELECT * '
                                                            'FROM students as S, classes as CL, attendances as A '
                                                            'WHERE CL.course_id = %s AND S.student_id = A.students '
                                                            'AND CL.course_id = A.classes AND MONTH(CL.date) = %s '
                                                            'AND CL.date = A.date '
                                                            'GROUP BY student_name', [course_id, month])

        status = Student.objects.select_related().raw('SELECT    * '
                                                      'FROM students as S, classes as CL, attendances as A '
                                                      'WHERE CL.course_id = %s '
                                                      'AND CL.course_id = A.classes '
                                                      'AND MONTH(CL.date) = %s '
                                                  'AND CL.date = A.date '
                                                      'GROUP BY A.id '
                                                      'ORDER BY A.date ', [course_id, month])

        all_dates = Course.objects.select_related().raw('SELECT * '
                                                        'FROM classes '
                                                        'WHERE course_id = %s '
                                                        'AND MONTH(date) = %s', [course_id, month])
        context = {
            'course_name': class_name,
            'all_dates': all_dates,
            'class_dates': class_dates,
            'all_students': all_students,
            'status': status
        }

    # Render the template to the user
    return HttpResponse(template.render(context, request))
