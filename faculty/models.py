from django.db import models
from utils.models.choices import AcademicLevel


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FacultyGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.name} - {self.name}"


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty_group = models.ForeignKey(FacultyGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AcademicField(models.Model):
    academic_level = models.CharField(max_length=10, choices=AcademicLevel.choices)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    required_units = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.academic_level.name} - {self.field_of_study.name}"
