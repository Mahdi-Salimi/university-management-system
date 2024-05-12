from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FacultyGroup(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.faculty.name} - {self.name}"


class AcademicLevel(models.Model):
    name = models.CharField(max_length=100)  # maybe use choices
    required_units = models.IntegerField()  # required units differ for each faculty

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100)
    faculty_group = models.ForeignKey(
        FacultyGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class AcademicField(models.Model):
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    required_units = models.IntegerField()

    def __str__(self):
        return f"{self.academic_level.name} - {self.field_of_study.name}"
