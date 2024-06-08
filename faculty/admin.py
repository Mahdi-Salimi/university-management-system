from django.contrib import admin

from faculty.models import Faculty, FacultyGroup, FieldOfStudy, AcademicField


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("name",)

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"


@admin.register(FacultyGroup)
class FacultyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")
    search_fields = ("name", "faculty")
    ordering = ("name",)
    list_filter = ("name", "faculty")

    class Meta:
        verbose_name = "Faculty Group"
        verbose_name_plural = "Faculty Groups"


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty_group")
    search_fields = ("name", "faculty_group")
    ordering = ("name",)
    list_filter = ("name", "faculty_group")

    class Meta:
        verbose_name = "Field of Study"
        verbose_name_plural = "Fields of Study"


@admin.register(AcademicField)
class AcademicFieldAdmin(admin.ModelAdmin):
    list_display = ("academic_level", "field_of_study", "required_units")
    search_fields = ("academic_level", "field_of_study")
    ordering = ("academic_level", "field_of_study")
    list_filter = ("academic_level", "field_of_study")

    class Meta:
        verbose_name = "Academic Field"
        verbose_name_plural = "Academic Fields"
