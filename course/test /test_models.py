from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from ..models import Course, Semester, CourseType, SemesterCourse, StudentCourse, StudentSemester, ClassSession
from faculty.models import Faculty, AcademicField, FieldOfStudy, FacultyGroup
from user.models import Professor, Student
from utils.models.choices import AcademicSemesterChoices, CourseTypeChoices, StudentCourseStatusChoices, UnitTypeChoices

class CourseModelTest(TestCase):

    def setUp(self):
        self.faculty = Faculty.objects.create(name="Engineering")
        self.professor = Professor.objects.create()
        self.course = Course.objects.create(
            name="Test Course",
            code="TC101",
            description="A test course.",
            faculty=self.faculty,
            course_unit=3,
            unit_type=UnitTypeChoices.Theory,
        )
        self.course.professors.add(self.professor)

    def test_course_creation(self):
        course = Course.objects.get(code="TC101")
        self.assertEqual(course.name, "Test Course")
        self.assertEqual(course.code, "TC101")
        self.assertEqual(course.course_status(), "available")

    def test_course_read(self):
        course = Course.objects.get(code="TC101")
        self.assertEqual(course.description, "A test course.")

    def test_course_update(self):
        self.course.name = "Updated Course"
        self.course.save()
        updated_course = Course.objects.get(code="TC101")
        self.assertEqual(updated_course.name, "Updated Course")

    def test_course_delete(self):
        self.course.delete()
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(code="TC101")

    def test_course_string_representation(self):
        self.assertEqual(str(self.course), "Test Course_TC101")


class SemesterModelTest(TestCase):

    def setUp(self):
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

    def test_semester_creation(self):
        semester = Semester.objects.get(academic_year=2023)
        self.assertEqual(semester.academic_year, 2023)
        self.assertEqual(semester.get_semester_code(), "231")

    def test_semester_read(self):
        semester = Semester.objects.get(academic_year=2023)
        self.assertEqual(semester.academic_semester, AcademicSemesterChoices.AUTUMN)

    def test_semester_update(self):
        self.semester.academic_year = 2024
        self.semester.save()
        updated_semester = Semester.objects.get(pk=self.semester.pk)
        self.assertEqual(updated_semester.academic_year, 2024)

    def test_semester_delete(self):
        self.semester.delete()
        with self.assertRaises(Semester.DoesNotExist):
            Semester.objects.get(academic_year=2023)

    def test_semester_string_representation(self):
        self.assertEqual(str(self.semester), "2023 Autumn")

    def test_get_current_semester(self):
        current_semester = Semester.get_current_semester()
        self.assertEqual(current_semester, self.semester)


class CourseTypeModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name="Test Course",
            code="TC101",
            description="A test course.",
            course_unit=3,
            unit_type=UnitTypeChoices.Theory,
        )
        self.faculty = Faculty.objects.create(name = 'civil')
        self.faculty_group = FacultyGroup.objects.create(name = 'environment', faculty = self.faculty)
        self.field_of_study= FieldOfStudy.objects.create(name = 'civil', faculty_group = self.faculty_group)
        self.academic_field = AcademicField.objects.create(academic_level= 'Bachelor', field_of_study=self.field_of_study, required_units = 146)
        self.course_type = CourseType.objects.create(
            course_type=CourseTypeChoices.GENERAL,
            course=self.course,
            academic_field=self.academic_field,
        )

    def test_course_type_creation(self):
        course_type = CourseType.objects.get(course=self.course)
        self.assertEqual(course_type.course_type, CourseTypeChoices.GENERAL)
        self.assertEqual(str(course_type), "Test Course_TC101 - Bachelor - civil")

    def test_course_type_read(self):
        course_type = CourseType.objects.get(course=self.course)
        self.assertEqual(f'{course_type.academic_field.academic_level} - {course_type.academic_field.field_of_study}', "Bachelor - civil")

    def test_course_type_update(self):
        self.course_type.course_type = CourseTypeChoices.GENERAL
        self.course_type.save()
        updated_course_type = CourseType.objects.get(pk=self.course_type.pk)
        self.assertEqual(updated_course_type.course_type, CourseTypeChoices.GENERAL)

    def test_course_type_delete(self):
        self.course_type.delete()
        with self.assertRaises(CourseType.DoesNotExist):
            CourseType.objects.get(course=self.course)


class SemesterCourseModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name="Test Course",
            code="TC101",
            description="A test course.",
            course_unit=3,
            unit_type=UnitTypeChoices.Theory,
        )
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
        self.professor = Professor.objects.create()
        self.semester_course = SemesterCourse.objects.create(
            course=self.course,
            semester=self.semester,
            exam_date_time=timezone.now() + timedelta(days=90),
            exam_place="Room 101",
            course_capacity=30,
            professor=self.professor,
        )

    def test_semester_course_creation(self):
        semester_course = SemesterCourse.objects.get(course=self.course)
        self.assertEqual(str(semester_course), "Test Course_TC101 - 2023 Autumn")

    def test_semester_course_read(self):
        semester_course = SemesterCourse.objects.get(course=self.course)
        self.assertEqual(semester_course.exam_place, "Room 101")

    def test_semester_course_update(self):
        self.semester_course.exam_place = "Room 102"
        self.semester_course.save()
        updated_semester_course = SemesterCourse.objects.get(pk=self.semester_course.pk)
        self.assertEqual(updated_semester_course.exam_place, "Room 102")

    def test_semester_course_delete(self):
        self.semester_course.delete()
        with self.assertRaises(SemesterCourse.DoesNotExist):
            SemesterCourse.objects.get(course=self.course)


class StudentCourseModelTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create()
        self.course = Course.objects.create(
            name="Test Course",
            code="TC101",
            description="A test course.",
            course_unit=3,
            unit_type=UnitTypeChoices.Theory,
        )
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
            exam_date_time=timezone.now() + timedelta(days=90),
            exam_place="Room 101",
            course_capacity=30,
            professor=None,
        )
        self.student_course = StudentCourse.objects.create(
            student=self.student,
            course_status=StudentCourseStatusChoices.NOTTAKEN,
            semester_course=self.semester_course,
        )

    def test_student_course_creation(self):
        student_course = StudentCourse.objects.get(student=self.student)
        self.assertEqual(str(student_course), "None - Test Course_TC101 - 2023 Autumn")

    def test_student_course_read(self):
        student_course = StudentCourse.objects.get(student=self.student)
        self.assertEqual(student_course.course_status, StudentCourseStatusChoices.NOTTAKEN)

    def test_student_course_update(self):
        self.student_course.course_status = StudentCourseStatusChoices.NOTTAKEN
        self.student_course.save()
        updated_student_course = StudentCourse.objects.get(pk=self.student_course.pk)
        self.assertEqual(updated_student_course.course_status, StudentCourseStatusChoices.NOTTAKEN)

    def test_student_course_delete(self):
        self.student_course.delete()
        with self.assertRaises(StudentCourse.DoesNotExist):
            StudentCourse.objects.get(student=self.student)


class StudentSemesterModelTest(TestCase):

    def setUp(self):
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
        self.student_semester = StudentSemester.objects.create(
            student=self.student,
            semester=self.semester,
            gpa=3.5,
            semester_status='UNK',
        )

    def test_student_semester_creation(self):
        student_semester = StudentSemester.objects.get(student=self.student)
        self.assertEqual(str(student_semester), "NoneUNK")

    def test_student_semester_read(self):
        student_semester = StudentSemester.objects.get(student=self.student)
        self.assertEqual(student_semester.gpa, 3.5)

    def test_student_semester_update(self):
        self.student_semester.gpa = 4.0
        self.student_semester.save()
        updated_student_semester = StudentSemester.objects.get(pk=self.student_semester.pk)
        self.assertEqual(updated_student_semester.gpa, 4.0)

    def test_student_semester_delete(self):
        self.student_semester.delete()
        with self.assertRaises(StudentSemester.DoesNotExist):
            StudentSemester.objects.get(student=self.student)


class ClassSessionModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name="Test Course",
            code="TC101",
            description="A test course.",
            course_unit=3,
            unit_type=UnitTypeChoices.Theory,
        )
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
            exam_date_time=timezone.now() + timedelta(days=90),
            exam_place="Room 101",
            course_capacity=30,
            professor=None,
        )
        self.class_session = ClassSession.objects.create(
            semester_course=self.semester_course,
            day_of_week='MON',
            time_block='7_9',
        )

    def test_class_session_creation(self):
        class_session = ClassSession.objects.get(semester_course=self.semester_course)
        self.assertEqual(class_session.day_of_week, 'MON')
        self.assertEqual(class_session.time_block, '7_9')

    def test_class_session_read(self):
        class_session = ClassSession.objects.get(semester_course=self.semester_course)
        self.assertEqual(class_session.day_of_week, 'MON')

    def test_class_session_update(self):
        self.class_session.day_of_week = 'TUE'
        self.class_session.save()
        updated_class_session = ClassSession.objects.get(pk=self.class_session.pk)
        self.assertEqual(updated_class_session.day_of_week, 'TUE')

    def test_class_session_delete(self):
        self.class_session.delete()
        with self.assertRaises(ClassSession.DoesNotExist):
            ClassSession.objects.get(semester_course=self.semester_course)
