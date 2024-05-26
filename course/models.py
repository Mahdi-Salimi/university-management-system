from django.db import models
from django.utils import timezone

from faculty.models import AcademicField, Faculty
from user.models import Professor, Student
from utils.models.choices import AcademicSemesterChoices, CourseTypeChoices, grade_validatior, UnitTypeChoices, StudentCourseStatusChoices, WeekDayChoices

class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='prerequisite_of', blank=True)
    corequisites = models.ManyToManyField('self', symmetrical=False, related_name='corequisite_of', blank=True)
    course_unit = models.IntegerField()
    unit_type = models.CharField(
        max_length=1,
        choices=UnitTypeChoices.choices,
        default=UnitTypeChoices.Theory,
    )
    professors = models.ManyToManyField(Professor, related_name='teaching_courses', blank=True)
    
    def course_status(self):
        if self.professors.exists():
            return "available"
        else:
            return "Not available"


    def __str__(self):
        return self.name + '_' + self.code
    
    
    
class Semester(models.Model):
    academic_year = models.IntegerField()
    academic_semester = models.CharField(
        max_length=1,
        choices=AcademicSemesterChoices.choices,
        default=AcademicSemesterChoices.AUTUMN,
    )
    start_course_registration = models.DateTimeField()
    end_course_registration = models.DateTimeField()
    start_class_date = models.DateTimeField()
    end_class_date = models.DateTimeField()
    start_course_modification = models.DateTimeField()
    end_course_modification = models.DateTimeField()
    end_emergency_modification = models.DateTimeField()
    start_exam_date = models.DateTimeField()
    end_semester_date = models.DateTimeField()

    def __str__(self):
        return str(self.academic_year) + " " + self.get_academic_semester_display()

    def get_semester_code(self):
        return str(self.academic_year)[-2:] + self.academic_semester

    @classmethod
    def get_current_semester(cls):
        return Semester.objects.filter(start_course_registration__lte=timezone.now(),
                                       end_course_registration__gte=timezone.now()).first()





class CourseType(models.Model):
    course_type = models.CharField(
        max_length=1,
        choices=CourseTypeChoices.choices,
        default=CourseTypeChoices.GENERAL,
    )
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    academic_field = models.ForeignKey(to=AcademicField, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} - {self.academic_field}"


class SemesterCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    exam_date_time = models.DateTimeField()
    exam_place = models.CharField(max_length=30)
    course_capacity = models.IntegerField()
    professor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.course} - {self.semester}"


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_status = models.CharField(
        max_length=1,
        choices=StudentCourseStatusChoices.choices,
        default=StudentCourseStatusChoices.NOTTAKEN,
    )
    student_grade = models.DecimalField(decimal_places=2, max_digits=5, validators=(grade_validatior,), null=True, blank=True)
    semester_course = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student) + " - " + str(self.semester_course)


class StudentSemester(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    gpa = models.FloatField()
    semester_count = models.IntegerField()
    
    def __str__(self):
        return self.student.name + str(self.semester_count)
    
    
class ClassSession(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    TIME_BLOCK_CHOICES = [
        ('7_9', '7:00 - 9:00'),
        ('9_11', '9:00 -11:00'),
        ('11_13', '11:00 -13:00'),
        ('13_15', '13:00 -15:00'),
        ('15_17', '15:00 -17:00'),
        ('17_19', '17:00 -19:00'),   
    ]
    
    semester_course = models.ForeignKey(SemesterCourse, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    time_block= models.CharField(max_length=5, choices=TIME_BLOCK_CHOICES)