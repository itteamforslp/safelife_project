from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.db import connection
from django.http import HttpResponseRedirect
import datetime
from django.http import JsonResponse
from django.db.models import Count
from administrator.models import Course, CourseTeacher, CourseStudent, Student, Class
from documents.models import Document
from django.core.exceptions import PermissionDenied

 #Limit view to admin only."""
def admin_only(function):
    def _inner(request, *args, **kwargs):
       if not request.user.is_staff | request.user.is_superuser:
           raise PermissionDenied           
       return function(request, *args, **kwargs)
    return _inner

 
@login_required(login_url = '/users')
@admin_only
def home(request):
        current_user = request.user.id
        admin_current_courses = Course.objects.select_related().raw('SELECT * '
                                                        'FROM course_teachers as CT, courses as C '
                                                        'WHERE CT.teachers_id = %s AND C.course_id = CT.course_id AND C.is_complete = 0 ', [current_user])
        
        all_courses = Course.objects.select_related().raw('SELECT * '
                                                        'FROM courses as C '
                                                        'WHERE C.is_complete = 0')

        currentdate = datetime.datetime.today().strftime('%Y-%m-%d')

        with connection.cursor() as cursor:
                docs =cursor.execute('SELECT D.id, D.doc_type_id '
                                                        'FROM documents AS D '
                                                        'GROUP BY D.doc_type_id '
                                                        'ORDER BY D.doc_type_id ')
                docs = cursor.fetchall()
        firstdoc = docs[:1]
        print(firstdoc)

        with connection.cursor() as cursor:
                cursor.execute('SELECT CL.course_id, CL.date '
                                'FROM classes as CL, course_teachers as CT '
                                'WHERE CT.teachers_id = %s AND CL.date >= %s '
                                'AND CT.course_id = CL.course_id '
                                'GROUP BY CL.course_id ', [current_user, currentdate])

                next_class_date = cursor.fetchall()
        
        with connection.cursor() as cursor:
                cursor.execute('SELECT CL.course_id, CL.date '
                                'FROM classes as CL '
                                'WHERE CL.date >= %s '
                                'GROUP BY CL.course_id ', [currentdate])

                all_next_class_date = cursor.fetchall()
        
        with connection.cursor() as cursor:
                cursor.execute('SELECT CS.course_id, COUNT(CS.students_id) '
                        'FROM course_teachers as CT, course_students as CS '
                        'WHERE CT.teachers_id = %s AND CT.course_id = CS.course_id '
                        'GROUP BY CS.course_id ', [current_user])
                admin_student_count = cursor.fetchall()

        with connection.cursor() as cursor:
                cursor.execute('SELECT CS.course_id, COUNT(CS.students_id) '
                        'FROM course_students as CS '
                        'GROUP BY CS.course_id ')

                all_student_count = cursor.fetchall()


        with connection.cursor() as cursor:
                cursor.execute('SELECT C.course_id, C.notes '
                                'FROM course_teachers as CT, courses as C '
                                'WHERE CT.teachers_id = %s AND C.course_id = CT.course_id '
                                'GROUP BY CT.course_id ', [current_user])
                admin_course_notes = cursor.fetchall()

        with connection.cursor() as cursor:
                cursor.execute('SELECT CT.course_id, U.first_name, U.last_name '
                                'FROM course_teachers AS CT, auth_user AS U '
                                'WHERE CT.teachers_id = U.id '
                                'ORDER BY CT.course_id ')
                all_course_teachers = cursor.fetchall()
                                                        

        template = loader.get_template('administrator/dashboard.html')
        context = {
                'admin_current_courses': admin_current_courses,
                'all_courses': all_courses,
                'admin_student_count': admin_student_count,
                'all_student_count': all_student_count,
                'next_class_date': next_class_date,
                'all_next_class_date': all_next_class_date,
                'all_course_teachers': all_course_teachers,
                'admin_course_notes': admin_course_notes,
                'firstdoc': firstdoc
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

@login_required(login_url = '/users')
@admin_only
def docs(request):
        template = loader.get_template('administrator/docs.html')
        return HttpResponse(template.render())