from django.contrib import admin
from .models import Course, Semester, CourseType, SemesterCourse, StudentCourse, StudentSemester, ClassSession


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "faculty", "course_unit", "unit_type", "course_status")
    search_fields = ("name", "code")
    list_filter = ("faculty", "unit_type")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("academic_year", "academic_semester", "start_course_registration", "end_course_registration")
    search_fields = ("academic_year", "academic_semester")
    list_filter = ("academic_year", "academic_semester")


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ("course", "academic_field", "course_type")
    search_fields = ("course__name", "academic_field__name")
    list_filter = ("course_type",)


@admin.register(SemesterCourse)
class SemesterCourseAdmin(admin.ModelAdmin):
    list_display = ("course", "semester", "exam_date_time", "exam_place", "course_capacity", "professor")
    search_fields = ("course__name", "semester__academic_year", "professor__user__username")
    list_filter = ("semester", "professor")


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ("student", "course_status", "student_grade", "semester_course")
    search_fields = ("student__user__username", "semester_course__course__name")
    list_filter = ("course_status",)


@admin.register(StudentSemester)
class StudentSemesterAdmin(admin.ModelAdmin):
    list_display = ("student", "semester", "gpa", "semester_status")
    search_fields = ("student__user__username", "semester__academic_year")
    list_filter = ("semester_status",)


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("semester_course", "day_of_week", "time_block")
    search_fields = ("semester_course__course__name", "day_of_week")
    list_filter = ("day_of_week", "time_block")
