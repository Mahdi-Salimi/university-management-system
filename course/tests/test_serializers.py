from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from faculty.models import Faculty, FacultyGroup, FieldOfStudy
from user.models import Professor, Student
from course.models import (
    Course,
    Semester,
    SemesterCourse,
    StudentCourse,
    StudentSemester,
    CourseType,
    ClassSession,
    AcademicField,
)
from course.serializers import (
    CourseSerializer,
    SemesterSerializer,
    SemesterCourseSerializer,
    StudentCourseSerializer,
    StudentSemesterSerializer,
    CourseTypeSerializer,
    ClassSessionSerializer,
)
from utils.models.choices import AcademicSemesterChoices, CourseTypeChoices, UnitTypeChoices


class SerializerTestCase(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name="civil")
        self.faculty_group = FacultyGroup.objects.create(name="environment", faculty=self.faculty)
        self.field_of_study = FieldOfStudy.objects.create(name="civil", faculty_group=self.faculty_group)
        self.academic_field = AcademicField.objects.create(
            academic_level="Bachelor", field_of_study=self.field_of_study, required_units=146
        )
        self.course = Course.objects.create(
            name="Test Course",
            code="TC101",
            description="A test course.",
            course_unit=3,
            unit_type=UnitTypeChoices.Theory,
        )
        self.course_type = CourseType.objects.create(
            course_type=CourseTypeChoices.GENERAL,
            course=self.course,
            academic_field=self.academic_field,
        )
        self.professor = Professor.objects.create(faculty_group=self.faculty_group)
        self.student = Student.objects.create()
        self.semester = Semester.objects.create(
            academic_year=2023,
            academic_semester=AcademicSemesterChoices.AUTUMN,
            start_course_registration=timezone.now() - timedelta(days=10),
            end_course_registration=timezone.now() + timedelta(days=10),
            start_class_date=timezone.now() + timedelta(days=15),
            end_class_date=timezone.now() + timedelta(days=115),
            start_course_modification=timezone.now() + timedelta(days=5),
            end_course_modification=timezone.now() + timedelta(days=20),
            end_emergency_modification=timezone.now() + timedelta(days=30),
            start_exam_date=timezone.now() + timedelta(days=100),
            end_semester_date=timezone.now() + timedelta(days=120),
        )
        self.semester_course = SemesterCourse.objects.create(
            course=self.course,
            semester=self.semester,
            exam_date_time=timezone.now() + timedelta(days=95),
            exam_place="Room 101",
            course_capacity=30,
        )
        self.student_course = StudentCourse.objects.create(
            student=self.student,
            course_status="N",
            semester_course=self.semester_course,
        )
        self.student_semester = StudentSemester.objects.create(
            student=self.student,
            semester=self.semester,
            gpa=3.5,
            semester_status="ONG",
        )
        self.class_session = ClassSession.objects.create(
            semester_course=self.semester_course,
            day_of_week="MON",
            time_block="7_9",
        )

    def test_course_serializer(self):
        data = {
            "name": "Physics 101",
            "code": "PHY101",
            "description": "Basic Physics",
            "faculty": self.faculty.id,
            "course_unit": 3,
            "unit_type": "T",
        }
        serializer = CourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        course = serializer.save()
        self.assertEqual(course.name, "Physics 101")

    def test_semester_serializer_valid(self):
        data = {
            "academic_year": 2023,
            "academic_semester": "1",
            "start_course_registration": timezone.now() - timedelta(days=10),
            "end_course_registration": timezone.now() + timedelta(days=10),
            "start_class_date": timezone.now() + timedelta(days=15),
            "end_class_date": timezone.now() + timedelta(days=100),
            "start_course_modification": timezone.now() + timedelta(days=20),
            "end_course_modification": timezone.now() + timedelta(days=30),
            "end_emergency_modification": timezone.now() + timedelta(days=40),
            "start_exam_date": timezone.now() + timedelta(days=90),
            "end_semester_date": timezone.now() + timedelta(days=120),
        }
        serializer = SemesterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        semester = serializer.save()
        self.assertEqual(semester.academic_year, 2023)

    def test_semester_serializer_invalid(self):
        data = {
            "academic_year": 2023,
            "academic_semester": "A",
            "start_course_registration": timezone.now() + timedelta(days=10),
            "end_course_registration": timezone.now() - timedelta(days=10),
            "start_class_date": timezone.now() + timedelta(days=15),
            "end_class_date": timezone.now() + timedelta(days=100),
            "start_course_modification": timezone.now() + timedelta(days=20),
            "end_course_modification": timezone.now() + timedelta(days=30),
            "end_emergency_modification": timezone.now() + timedelta(days=40),
            "start_exam_date": timezone.now() + timedelta(days=90),
            "end_semester_date": timezone.now() + timedelta(days=120),
        }
        serializer = SemesterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    def test_semester_course_serializer_valid(self):
        data = {
            "course": self.course.id,
            "semester": self.semester.id,
            "exam_date_time": timezone.now() + timedelta(days=95),
            "exam_place": "Room 102",
            "course_capacity": 30,
            "professor": self.professor.id,
        }
        serializer = SemesterCourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        semester_course = serializer.save()
        self.assertEqual(semester_course.exam_place, "Room 102")

    def test_semester_course_serializer_invalid_exam_date(self):
        data = {
            "course": self.course.id,
            "semester": self.semester.id,
            "exam_date_time": timezone.now() - timedelta(days=5),
            "exam_place": "Room 102",
            "course_capacity": 30,
            "professor": self.professor.id,
        }
        serializer = SemesterCourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    def test_student_course_serializer(self):
        data = {
            "student": self.student.id,
            "course_status": "N",
            "student_grade": 85.0,
            "semester_course": self.semester_course.id,
        }
        serializer = StudentCourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        student_course = serializer.save()
        self.assertEqual(student_course.student_grade, 85.0)

    def test_student_semester_serializer(self):
        data = {
            "student": self.student.id,
            "semester": self.semester.id,
            "gpa": 3.8,
            "semester_status": "ONG",
        }
        serializer = StudentSemesterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        student_semester = serializer.save()
        self.assertEqual(student_semester.gpa, 3.8)

    def test_course_type_serializer(self):
        data = {
            "course_type": "G",
            "course": self.course.id,
            "academic_field": self.academic_field.id,
        }
        serializer = CourseTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        course_type = serializer.save()
        self.assertEqual(course_type.course_type, "G")

    def test_class_session_serializer(self):
        data = {
            "semester_course": self.semester_course.id,
            "day_of_week": "TUE",
            "time_block": "9_11",
        }
        serializer = ClassSessionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        class_session = serializer.save()
        self.assertEqual(class_session.day_of_week, "TUE")
