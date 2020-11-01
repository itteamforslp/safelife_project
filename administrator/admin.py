from django.contrib import admin

from .models import Student, Teacher, Course, CourseStudent, CourseTeacher, Class

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_id')

class CourseStudentInline(admin.TabularInline):
    model = CourseStudent

class CourseTeacherInline(admin.TabularInline):
    model = CourseTeacher

class ClassInline(admin.TabularInline):
    model = Class
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