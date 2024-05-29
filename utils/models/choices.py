from django.db import models
from django.core.exceptions import ValidationError



class GenderChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class MilitaryServiceChoices(models.TextChoices):
    APPLICABLE = "A", "Subject to duty"
    NOT_APPLICABLE = "N", "Not subject to duty"
    EXEMPT = "E", "Exempt from duty"


class ProfessorRankChoices(models.TextChoices):
    ASSISTANT = "C", "Assistant Professor"
    ASSOCIATE = "B", "Associate Professor"
    PROFESSOR = "A", "Full Professor"


class StudentStatusChoices(models.TextChoices):
    STUDYING = "S", "Studying"
    DISMISSAL = "D", "Dismissal from education"
    WITHDRAWAL = "W", "Withdrawal from education"
    GRADUATED = "G", "Graduated"
    
class AcademicSemesterChoices(models.TextChoices):
    AUTUMN = "1", "Autumn"
    WINTER = "2", "Winter"
    SUMMER = "3", "Summer"
    
class CourseTypeChoices(models.TextChoices):
    GENERAL = "G", "General"
    SPECIALIZED = "S", "Specialized"
    OPTIONAL = "O", "Optional"
    BASIC = "B", "Basic"


class UnitTypeChoices(models.TextChoices):
    Theory = "T", "Theory"
    Practical = "P", "Practical"

class WeekDayChoices(models.TextChoices):
    SATURDAY = "1", "Saturday"
    SUNDAY = "2", "Sunday"
    MONDAY = "3", "Monday"
    TUESDAY = "4", "Tuesday"
    WEDNESDAY = "5", "Wednesday"

class StudentCourseStatusChoices(models.TextChoices):
    NOTTAKEN = "N", "Withdrawn in Emenrgency"
    STUDYING = "S", "Studying"
    FAILED = "F", "Failed Student Course"
    PASSED = "P", "Passed Student Course"
    
def grade_validatior(input: float):
    if input > 20 and input < 0:
        raise ValidationError("Grade must be between 0 and 20!")
