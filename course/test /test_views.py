from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from faculty.models import Faculty, FacultyGroup, FieldOfStudy
from user.models import Professor, Student
from ..models import (
    Course, Semester, SemesterCourse, StudentCourse, 
    StudentSemester, CourseType, ClassSession, AcademicField
)
from utils.models.choices import AcademicSemesterChoices, CourseTypeChoices, UnitTypeChoices
from user.models import CustomUser
from django.contrib.auth.models import Permission

class ViewTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        
        # Grant all permissions to the test user
        all_permissions = Permission.objects.all()
        self.user.user_permissions.set(all_permissions)
        
        # Authenticate the test client as the test user
        self.client.force_authenticate(user=self.user)
        self.faculty = Faculty.objects.create(name='civil')
        self.faculty_group = FacultyGroup.objects.create(name='environment', faculty=self.faculty)
        self.field_of_study = FieldOfStudy.objects.create(name='civil', faculty_group=self.faculty_group)
        self.academic_field = AcademicField.objects.create(academic_level='Bachelor', field_of_study=self.field_of_study, required_units=146)
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
            semester_status='ONG',
        )
        self.class_session = ClassSession.objects.create(
            semester_course=self.semester_course,
            day_of_week="MON",
            time_block="7_9",
        )


    def test_course_list(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_create(self):
        data = {
            "name": "Physics 101",
            "code": "PHY101",
            "description": "Basic Physics",
            "faculty": self.faculty.id,
            "course_unit": 3,
            "unit_type": "T",
        }
        response = self.client.post(reverse('course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_retrieve(self):
        response = self.client.get(reverse('course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update(self):
        data = {
            "name": "Updated Course",
            "code": "TC101",
            "description": "Updated description.",
            "course_unit": 4,
            "unit_type": "T",
        }
        response = self.client.put(reverse('course-detail', args=[self.course.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Updated Course")

    def test_course_delete(self):
        response = self.client.delete(reverse('course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_semester_list(self):
        response = self.client.get(reverse('semester-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_create(self):
        data = {
            "academic_year": 2023,
            "academic_semester": "1",
            "start_course_registration": timezone.now() - timedelta(days=10),
            "end_course_registration": timezone.now() + timedelta(days=10),
            "start_class_date": timezone.now() + timedelta(days=15),
            "end_class_date": timezone.now() + timedelta(days=115),
            "start_course_modification": timezone.now() + timedelta(days=5),
            "end_course_modification": timezone.now() + timedelta(days=20),
            "end_emergency_modification": timezone.now() + timedelta(days=30),
            "start_exam_date": timezone.now() + timedelta(days=100),
            "end_semester_date": timezone.now() + timedelta(days=120),
        }
        response = self.client.post(reverse('semester-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_semester_retrieve(self):
        response = self.client.get(reverse('semester-detail', args=[self.semester.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_update(self):
        data = {
            "academic_year": 2024,
            "academic_semester": "3",
            "start_course_registration": timezone.now() - timedelta(days=10),
            "end_course_registration": timezone.now() + timedelta(days=10),
            "start_class_date": timezone.now() + timedelta(days=15),
            "end_class_date": timezone.now() + timedelta(days=115),
            "start_course_modification": timezone.now() + timedelta(days=5),
            "end_course_modification": timezone.now() + timedelta(days=20),
            "end_emergency_modification": timezone.now() + timedelta(days=30),
            "start_exam_date": timezone.now() + timedelta(days=100),
            "end_semester_date": timezone.now() + timedelta(days=120),
        }
        response = self.client.put(reverse('semester-detail', args=[self.semester.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.semester.refresh_from_db()
        self.assertEqual(self.semester.academic_year, 2024)

    def test_semester_delete(self):
        response = self.client.delete(reverse('semester-detail', args=[self.semester.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_semester_course_list(self):
        response = self.client.get(reverse('semestercourse-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_course_create(self):
        data = {
            "course": self.course.id,
            "semester": self.semester.id,
            "exam_date_time": timezone.now() + timedelta(days=95),
            "exam_place": "Room 102",
            "course_capacity": 30,
            "professor": self.professor.id
        }
        response = self.client.post(reverse('semestercourse-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_semester_course_retrieve(self):
        response = self.client.get(reverse('semestercourse-detail', args=[self.semester_course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_course_update(self):
        data = {
            "course": self.course.id,
            "semester": self.semester.id,
            "exam_date_time": timezone.now() + timedelta(days=100),
            "exam_place": "Room 103",
            "course_capacity": 35,
            "professor": self.professor.id
        }
        response = self.client.put(reverse('semestercourse-detail', args=[self.semester_course.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.semester_course.refresh_from_db()
        self.assertEqual(self.semester_course.exam_place, "Room 103")

    def test_semester_course_delete(self):
        response = self.client.delete(reverse('semestercourse-detail', args=[self.semester_course.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_course_list(self):
        response = self.client.get(reverse('studentcourse-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_course_create(self):
        data = {
            "student": self.student.id,
            "course_status": "N",
            "student_grade": 85.0,
            "semester_course": self.semester_course.id,
        }
        response = self.client.post(reverse('studentcourse-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_course_retrieve(self):
        response = self.client.get(reverse('studentcourse-detail', args=[self.student_course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_course_update(self):
        data = {
            "student": self.student.id,
            "course_status": "N",
            "student_grade": 90.0,
            "semester_course": self.semester_course.id,
        }
        response = self.client.put(reverse('studentcourse-detail', args=[self.student_course.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_course.refresh_from_db()
        self.assertEqual(self.student_course.student_grade, 90.0)

    def test_student_course_delete(self):
        response = self.client.delete(reverse('studentcourse-detail', args=[self.student_course.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_semester_list(self):
        response = self.client.get(reverse('studentsemester-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_semester_create(self):
        data = {
            "student": self.student.id,
            "semester": self.semester.id,
            "gpa": 3.8,
            "semester_status": "ONG",
        }
        response = self.client.post(reverse('studentsemester-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_semester_retrieve(self):
        response = self.client.get(reverse('studentsemester-detail', args=[self.student_semester.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_semester_update(self):
        data = {
            "student": self.student.id,
            "semester": self.semester.id,
            "gpa": 3.9,
            "semester_status": "ONG",
        }
        response = self.client.put(reverse('studentsemester-detail', args=[self.student_semester.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_semester.refresh_from_db()
        self.assertEqual(self.student_semester.gpa, 3.9)

    def test_student_semester_delete(self):
        response = self.client.delete(reverse('studentsemester-detail', args=[self.student_semester.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_type_list(self):
        response = self.client.get(reverse('coursetype-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_type_create(self):
        data = {
            "course_type": "G",
            "course": self.course.id,
            "academic_field": self.academic_field.id,
        }
        response = self.client.post(reverse('coursetype-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_type_retrieve(self):
        response = self.client.get(reverse('coursetype-detail', args=[self.course_type.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_type_update(self):
        data = {
            "course_type": "S",
            "course": self.course.id,
            "academic_field": self.academic_field.id,
        }
        response = self.client.put(reverse('coursetype-detail', args=[self.course_type.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course_type.refresh_from_db()
        self.assertEqual(self.course_type.course_type, "S")

    def test_course_type_delete(self):
        response = self.client.delete(reverse('coursetype-detail', args=[self.course_type.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_class_session_list(self):
        response = self.client.get(reverse('classsession-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_class_session_create(self):
        data = {
            "semester_course": self.semester_course.id,
            "day_of_week": "TUE",
            "time_block": "9_11",
        }
        response = self.client.post(reverse('classsession-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_class_session_retrieve(self):
        response = self.client.get(reverse('classsession-detail', args=[self.class_session.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_class_session_update(self):
        data = {
            "semester_course": self.semester_course.id,
            "day_of_week": "WED",
            "time_block": "11_13",
        }
        response = self.client.put(reverse('classsession-detail', args=[self.class_session.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.class_session.refresh_from_db()
        self.assertEqual(self.class_session.day_of_week, "WED")

    def test_class_session_delete(self):
        response = self.client.delete(reverse('classsession-detail', args=[self.class_session.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
