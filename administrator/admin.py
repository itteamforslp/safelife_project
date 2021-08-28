from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from datetime import datetime
from .models import Student, Teacher, Course, CourseStudent, CourseTeacher, Class, Attendance
from .forms import UserRegistrationForm

class AttendanceInline(admin.TabularInline):
   model = Attendance

   def save_model(self, request, form, change):
        if getattr(obj, 'date', None) is None:
            obj.date = datetime.now


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_id')

class CourseStudentInline(admin.TabularInline):
    model = CourseStudent
 

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

    list_display = ('course_name', 'course_id')

class UserAdmin(admin.ModelAdmin):
    model = User
    form = UserRegistrationForm
    list_display = ('username', 'first_name', 'last_name')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.site_header = "Safe Life Project ";
admin.site.site_title = "Safe Life Project ";
admin.site.site_url = '/administrator'