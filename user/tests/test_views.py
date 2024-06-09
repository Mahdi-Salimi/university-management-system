import json
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import get_user_model
from rest_framework.test import APIClient
from user.models import Student
from course.models import Semester
from faculty.models import AcademicField, AcademicLevel, Faculty, FacultyGroup, FieldOfStudy

User = get_user_model()


class LoginLogoutAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="pass",
        )

    def test_login(self):
        url = reverse_lazy("user:login")
        response = self.client.post(
            url,
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_logout(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        refresh_token = login_response.data["refresh"]
        response = self.client.post(
            reverse_lazy("user:logout"),
            data={"refresh": refresh_token},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            reverse_lazy("user:logout"),
            data={"refresh": refresh_token},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StudentAPITestCase(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.client = APIClient()
        self.semester = Semester.objects.create(
            academic_year=2024,
            academic_semester="1",
            start_course_registration=timezone.now(),
            end_course_registration=timezone.now(),
            start_class_date=timezone.now(),
            end_class_date=timezone.now(),
            start_course_modification=timezone.now(),
            end_course_modification=timezone.now(),
            end_emergency_modification=timezone.now(),
            start_exam_date=timezone.now(),
            end_semester_date=timezone.now(),
        )
        self.faculty_physics = Faculty.objects.create(name="Physics")
        self.faculty_math = Faculty.objects.create(name="Math")
        self.group_physics = FacultyGroup.objects.create(
            name="Condensed Matter",
            faculty=self.faculty_physics,
        )
        self.group_math = FacultyGroup.objects.create(
            name="Practical Math",
            faculty=self.faculty_math,
        )
        self.academic_level = AcademicLevel.BACHELOR
        self.field_of_study_physics = FieldOfStudy.objects.create(
            name="Solid State Physics",
            faculty_group=self.group_physics,
        )
        self.field_of_study_math = FieldOfStudy.objects.create(
            name="Statistics",
            faculty_group=self.group_math,
        )
        self.academic_field_physics = AcademicField.objects.create(
            academic_level=self.academic_level,
            field_of_study=self.field_of_study_physics,
            required_units=136,
        )
        self.academic_field_math = AcademicField.objects.create(
            academic_level=self.academic_level,
            field_of_study=self.field_of_study_math,
            required_units=136,
        )
        self.user_student_physics = User.objects.create_user(
            username="physics",
            password="pass",
            national_id="1111111111",
        )
        self.user_student_math = User.objects.create_user(
            username="math",
            password="pass",
            national_id="0000000000",
        )
        self.user = User.objects.create_user(
            username="user",
            password="pass",
        )
        self.student_physics = Student.objects.create(
            entry_semester=self.semester,
            user=self.user_student_physics,
            academic_field=self.academic_field_physics,
        )
        self.student_math = Student.objects.create(
            entry_semester=self.semester,
            user=self.user_student_math,
            academic_field=self.academic_field_math,
        )

    def test_students_api_no_login(self):
        url = reverse_lazy("user:student-list")
        response = self.client.get(
            url,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_students_no_perm(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_option_students_with_view_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.options(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_head_students_with_view_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.head(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_students_with_view_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(json.loads(response.content)))

    def test_list_students_with_view_faculty_perm(self):
        perm = Permission.objects.get(codename="view_student_faculty")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(1, len(content))
        self.assertEqual(self.user_student_physics.username, content[0]["user"]["username"])

    def test_list_students_with_view_self_perm(self):
        perm = Permission.objects.get(codename="view_student_self")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_student_no_perm(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_student_with_view_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user_student_physics.username,
            json.loads(response.content)["user"]["username"],
        )

    def test_detail_student_with_view_faculty_perm(self):
        perm = Permission.objects.get(codename="view_student_faculty")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user_student_physics.username,
            json.loads(response.content)["user"]["username"],
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_student_with_view_self_perm(self):
        perm = Permission.objects.get(codename="view_student_self")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user_student_physics.username,
            json.loads(response.content)["user"]["username"],
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": "me"})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user_student_physics.username,
            json.loads(response.content)["user"]["username"],
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_put_student_no_perm(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.put(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_put_student_with_change_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user.user_permissions.add(perm)
        perm = Permission.objects.get(codename="change_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        content = json.loads(response.content)
        content["user"]["first_name"] = "Batman"
        content["status"] = "W"
        response = self.client.put(
            url,
            data=content,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "Batman",
            User.objects.get(id=self.user_student_physics.id).first_name,
        )
        self.assertEqual(
            "W",
            Student.objects.get(id=self.student_physics.id).status,
        )

    def test_detail_put_student_with_change_faculty_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user_student_physics.user_permissions.add(perm)
        perm = Permission.objects.get(codename="change_student_faculty")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        content = json.loads(response.content)
        content["user"]["first_name"] = "Batman"
        content["status"] = "W"
        response = self.client.put(
            url,
            data=content,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "Batman",
            User.objects.get(id=self.user_student_physics.id).first_name,
        )
        self.assertEqual(
            "W",
            Student.objects.get(id=self.student_physics.id).status,
        )

        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.put(
            url,
            data=content,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_put_student_with_change_self_perm(self):
        perm = Permission.objects.get(codename="view_student")
        self.user_student_physics.user_permissions.add(perm)
        perm = Permission.objects.get(codename="change_student_self")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.get(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        content = json.loads(response.content)
        content["user"]["first_name"] = "Batman"
        content["status"] = "W"
        response = self.client.put(
            url,
            data=content,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "Batman",
            User.objects.get(id=self.user_student_physics.id).first_name,
        )
        self.assertEqual(
            "W",
            Student.objects.get(id=self.student_physics.id).status,
        )

        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.put(
            url,
            data=content,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_patch_student_no_perm(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.patch(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_patch_student_with_change_perm(self):
        perm = Permission.objects.get(codename="change_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.patch(
            url,
            data={"status": "W"},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "W",
            Student.objects.get(id=self.student_physics.id).status,
        )

    def test_detail_patch_student_user_without_national_id(self):
        perm = Permission.objects.get(codename="change_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.patch(
            url,
            data={"user": {"first_name": "Batman"}},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "Batman",
            Student.objects.get(id=self.student_physics.id).user.first_name,
        )

    def test_detail_patch_student_user_with_national_id(self):
        perm = Permission.objects.get(codename="change_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.patch(
            url,
            data={"user": {"national_id": "2222222222"}},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "2222222222",
            Student.objects.get(id=self.student_physics.id).user.national_id,
        )

    def test_detail_patch_student_with_change_faculty_perm(self):
        perm = Permission.objects.get(codename="change_student_faculty")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.patch(
            url,
            data={"status": "W"},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "W",
            Student.objects.get(id=self.student_physics.id).status,
        )

        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.patch(
            url,
            data={"status": "W"},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_patch_student_with_change_self_perm(self):
        perm = Permission.objects.get(codename="change_student_self")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.patch(
            url,
            data={"status": "W"},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            "W",
            Student.objects.get(id=self.student_physics.id).status,
        )

        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.patch(
            url,
            data={"status": "W"},
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_delete_student_no_perm(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.delete(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Student.objects.filter(id=self.student_physics.id).exists())

    def test_detail_delete_student_with_delete_perm(self):
        perm = Permission.objects.get(codename="delete_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.delete(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student_physics.id).exists())

    def test_detail_delete_student_with_delete_faculty_perm(self):
        perm = Permission.objects.get(codename="delete_student_faculty")
        self.user_student_physics.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user_student_physics.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_math.id})
        response = self.client.delete(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Student.objects.filter(id=self.student_math.id).exists())
        url = reverse_lazy("user:student-detail", kwargs={"pk": self.student_physics.id})
        response = self.client.delete(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student_physics.id).exists())

    def test_create_student_no_perm(self):
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        response = self.client.post(
            url,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_student_with_add_perm_duplicated_national_id(self):
        perm = Permission.objects.get(codename="add_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        data = {
            "user": {
                "username": "test_user_dup",
                "first_name": "Amoo",
                "last_name": "Hasan",
                "email": "",
                "phone": None,
                "national_id": "1111111111",
                "gender": "M",
                "birthdate": None,
                "date_joined": "2024-04-02T21:22:05Z",
                "image": None,
            },
            "entry_semester": self.semester.id,
            "academic_field": self.academic_field_physics.id,
            "professor": None,
            "military_service": "A",
            "status": "S",
            "allowed_half_years": 8,
        }
        response = self.client.post(
            url,
            data=data,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", json.loads(response.content))

    def test_create_student_with_add_perm(self):
        perm = Permission.objects.get(codename="add_student")
        self.user.user_permissions.add(perm)
        login_response = self.client.post(
            reverse_lazy("user:login"),
            {"username": self.user.username, "password": "pass"},
            format="json",
        )
        url = reverse_lazy("user:student-list")
        data = {
            "user": {
                "username": "test_user",
                "first_name": "Amoo",
                "last_name": "Hasan",
                "email": "",
                "phone": None,
                "national_id": "1000000001",
                "gender": "M",
                "birthdate": None,
                "date_joined": "2024-04-02T21:22:05Z",
                "image": None,
            },
            "entry_semester": self.semester.id,
            "academic_field": self.academic_field_physics.id,
            "professor": None,
            "military_service": "A",
            "status": "S",
            "allowed_half_years": 8,
        }
        response = self.client.post(
            url,
            data=data,
            format="json",
            **{"HTTP_AUTHORIZATION": "Bearer " + login_response.data["access"]},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(user__national_id=data["user"]["national_id"]).exists())
        self.assertTrue(User.objects.filter(national_id=data["user"]["national_id"]).exists())
