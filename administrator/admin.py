from django.contrib import admin
from datetime import datetime
from .models import Student, Teacher, Course, CourseStudent, CourseTeacher, Class, Attendance

class AttendanceInline(admin.TabularInline):
   model = Attendance

   def save_model(self, request, form, change):
        if getattr(obj, 'date', None) is None:
            obj.date = datetime.now


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_id')

class CourseStudentInline(admin.TabularInline):
    model = CourseStudent
    #inlines = [
    #    AttendanceInline,
    #]

class CourseTeacherInline(admin.TabularInline):
    model = CourseTeacher


class ClassInline(admin.TabularInline):
    model = Class
    inlines = [
        AttendanceInline,
    ]
    list_filter = ('date')


class CourseAdmin(admin.ModelAdmin):
    inlines = [
        CourseStudentInline,
        CourseTeacherInline,
        ClassInline,
    ]
    exclude = ('notes',)
    

admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.site_header = "Safe Life Project ";
admin.site.site_title = "Safe Life Project ";
admin.site.site_url = '/administrator'