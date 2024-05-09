from django.db import models


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
