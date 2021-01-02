from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from administrator.models import Student, Class
from django.db import connection
import datetime


def index(request, course_id, date):
    super = request.user.is_superuser

    with connection.cursor() as cursor:
        # Get the students attendance status
        cursor.execute('SELECT * '
                       'FROM course_teachers '
                       'WHERE course_id = %s AND teachers_id = %s ', [course_id, request.user.id])
        # attendance_status is a tuple containing the students attendance status
        attendance_status = cursor.fetchone()
        cursor.execute('SELECT course_name '
                       'FROM courses '
                       'WHERE course_id = %s', [course_id])
        course_name = cursor.fetchone()
    if super is True:
        template = loader.get_template('AdminAttendanceIndex.html')
    else:
        template = loader.get_template('TeacherAttendanceIndex.html')
    if attendance_status is not None or super is True:
        # Get the current date in the following format: <4 Digit Year>-<2 Digit Month>-<2 Digit Day>
        currentdate = datetime.datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
        # Get the name of each student that is enrolled in the class
        all_students = Student.objects.select_related().raw('SELECT * '
                                                            'FROM students as S, classes as CL, course_students as CS '
                                                            'WHERE CL.course_id = %s AND S.student_id = CS.students_id '
                                                            'AND CL.course_id = CS.course_id '
                                                            'AND CL.date = %s ', [course_id, currentdate])

        # Get every recorded absence prior to the current date
        absent_students = Student.objects.select_related().raw('SELECT * '
                                                               'FROM students as S, classes as CL, attendances as A '
                                                               'WHERE CL.course_id = %s AND S.student_id = A.student_id '
                                                               'AND CL.course_id = A.course_id AND CL.date = A.date '
                                                               'AND A.status = 1 AND A.date < %s ',
                                                               [course_id, currentdate])
        class_dates = Class.objects.filter(course=course_id)

                                                                  
        currentdate = datetime.datetime.strptime(currentdate, '%Y-%m-%d').strftime('%B %d, %Y')
        # Create a template using AdminAttendanceIndex.html, and pass into it the list of student names and recorded absences

        context = {
            'course_name': course_name[0],
            'current_date': currentdate,
            'class_dates': class_dates,
            'all_students': all_students,
            'absent_students': absent_students
        }
    else:
        template = loader.get_template('AttendanceError.html')
        context = { }
    return HttpResponse(template.render(context, request))



def update_student(request, course_id, date):
    # Get the current date in the following format: <4 Digit Year>-<2 Digit Month>-<2 Digit Day>
    currentdate = datetime.datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
    # Get the student name that was passed from the web page
    name = request.GET['studentName']
    # Get the Student_ID from the Student table
    student_data = Student.objects.get(student_name=name)
    # Create a cursor to execute raw SQL queries.
    with connection.cursor() as cursor:
        # Get the students attendance status
        cursor.execute('SELECT A.status '
                       'FROM students as S, classes as CL, attendances as A '
                       'WHERE CL.course_id = %s AND S.student_id = A.student_id '
                       'AND CL.course_id = A.course_id AND CL.class_id = A.class_id '
                       'AND CL.date = %s AND S.student_name = %s ', [course_id, currentdate, student_data.student_name])
       
        # attendance_status is a tuple containing the students attendance status
        attendance_status = cursor.fetchone()
        
        #This is the button part, so it flips between present and absent (1 being Absent, 0 being present)
        # If the student was inadvertently marked as present, switch their status to Absent
        if attendance_status[0] == 0:
            print("this statement is true!")
            cursor.execute('UPDATE attendances, classes '
                           'SET attendances.status = 1 '
                           'WHERE attendances.student_id = %s AND classes.class_id = attendances.class_id '
                           'AND classes.date = %s ', [student_data.student_id, currentdate])
            print("Attendance changed to Absent!")
        # If the students status is set to Absent, mark them Present
        else:
            cursor.execute('UPDATE attendances, classes '
                           'SET attendances.status = 0, attendances.date = %s '
                           'WHERE attendances.student_id = %s AND classes.class_id = attendances.class_id '
                           'AND classes.date = %s  ', [currentdate, student_data.student_id, currentdate])
            print("Attendance changed to Present!")
    # Render the response to the user
    return render(request, 'TeacherAttendanceIndex.html', {})


def update_student_absent(request, course_id, date):
    # Get the current date in the following format: <4 Digit Year>-<2 Digit Month>-<2 Digit Day>
    currentdate = datetime.datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
    # Get the student name that was passed from the web page
    name = request.GET['studentName']
    # Get the absent date that was passed from the web page
    ##NEW: Get the date picked by the teacher
    date = request.GET['absentDate']
    # Convert the date to the following format: <4 Digit Year>-<2 Digit Month>-<2 Digit Day>
    date = datetime.datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
    # Get the Student_ID from the Student table
    student_data = Student.objects.get(student_name=name)
    # Create a cursor to execute raw SQL queries.
    with connection.cursor() as cursor:
    # Change the students attendance status from Absent to 'Makeup: <date>'
      cursor.execute('UPDATE attendances, classes '
                      'SET attendances.status = 1, attendances.date = %s '
                      'WHERE attendances.student_id = %s AND classes.class_id = attendances.class_id ' 
                      'classes.date = %s ', [request.GET['makeupDate'], student_data.student_id, date])
        
    # Render the response to the user
    return render(request, 'TeacherAttendanceIndex.html', {})
