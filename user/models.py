from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework.authentication import get_user_model
from user.validators import phone_validator, national_id_validator
from utils.models.choices import (
    GenderChoices,
    MilitaryServiceChoices,
    ProfessorRankChoices,
    StudentStatusChoices,
)
from utils.misc import user_image_path


class CustomUser(AbstractUser):
    national_id = models.CharField(
        max_length=10,
        validators=[national_id_validator],
    )
    image = models.ImageField(upload_to=user_image_path, blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.FEMALE,
    )
    phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        null=True,
        blank=True,
    )
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.username

    def get_role(self):
        try:
            return self.student
        except ObjectDoesNotExist:
            pass
        try:
            return self.professor
        except ObjectDoesNotExist:
            pass
        try:
            return self.assistant
        except ObjectDoesNotExist:
            pass

    def get_faculty(self):
        role = self.get_role()
        if role:
            return role.get_faculty()


User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    entry_semester = models.ForeignKey(
        to="course.Semester",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    academic_field = models.ForeignKey(
        to="faculty.AcademicField",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    professor = models.ForeignKey(
        to="Professor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    military_service = models.CharField(
        max_length=1,
        choices=MilitaryServiceChoices.choices,
        default=MilitaryServiceChoices.APPLICABLE,
    )
    status = models.CharField(
        max_length=1,
        choices=StudentStatusChoices.choices,
        default=StudentStatusChoices.STUDYING,
    )
    allowed_half_years = models.PositiveSmallIntegerField(default=8)
    gpa = models.DecimalField(max_digits=2, decimal_places=2, null=True, blank=True)

    class Meta:
        permissions = [
            ("view_student_faculty", "Can view students in faculty"),
            ("view_student_self", "Can view student of itself"),
            ("change_student_faculty", "Can change students in faculty"),
            ("change_student_self", "Can change student of itself"),
            ("delete_student_faculty", "Can delete students in faculty"),
        ]

    def __str__(self) -> str:
        return str(self.user)

    def get_faculty(self):
        return self.academic_field.field_of_study.faculty_group.faculty

    def get_passed_courses(self): ...

    def get_current_courses(self): ...

    @staticmethod
    def filter_by_faculty(faculty):
        return Student.objects.filter(academic_field__field_of_study__faculty_group__faculty=faculty)


class Professor(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    faculty_group = models.ForeignKey(
        to="faculty.FacultyGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    rank = models.CharField(
        max_length=1,
        choices=ProfessorRankChoices.choices,
        default=ProfessorRankChoices.ASSISTANT,
    )
    expertise = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        permissions = [
            ("view_professor_faculty", "Can view professors in faculty"),
            ("view_professor_self", "Can view professor of itself"),
            ("change_professor_faculty", "Can change professors in faculty"),
            ("change_professor_self", "Can change professor of itself"),
            ("delete_professor_faculty", "Can delete professors in faculty"),
        ]

    def __str__(self) -> str:
        return "Dr. " + str(self.user)

    def get_faculty(self):
        return self.field_of_study.faculty_group.faculty

    def get_taught_courses(self): ...

    @staticmethod
    def filter_by_faculty(faculty):
        return Professor.objects.filter(field_of_study__faculty_group__faculty=faculty)


class Assistant(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    faculty = models.OneToOneField(
        to="faculty.Faculty",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.user)
