from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from faculty.models import Faculty, FacultyGroup, FieldOfStudy, AcademicField

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a superuser for unrestricted access
        self.superuser = User.objects.create_superuser(username="admin", password="password", email="admin@example.com")

        # Create a regular user
        self.user = User.objects.create_user(username="user", password="password", email="user@example.com")

        # Create test data
        self.faculty = Faculty.objects.create(name="Engineering")
        self.faculty_group = FacultyGroup.objects.create(name="Computer Science", faculty=self.faculty)
        self.field_of_study = FieldOfStudy.objects.create(name="Software Engineering", faculty_group=self.faculty_group)
        self.academic_field = AcademicField.objects.create(
            academic_level="Bachelor", field_of_study=self.field_of_study, required_units=180
        )


class FacultyViewSetTests(BaseTestCase):
    def test_anonymous_user_cannot_view_faculties(self):
        response = self.client.get(reverse("faculty:faculty-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_create_faculty(self):
        data = {"name": "Science"}
        response = self.client.post(reverse("faculty:faculty-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_create_faculty(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Science"}
        response = self.client.post(reverse("faculty:faculty-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_without_permission_cannot_create_faculty(self):
        self.client.login(username="user", password="password")
        data = {"name": "Science"}
        response = self.client.post(reverse("faculty:faculty-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_create_faculty(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Science"}
        response = self.client.post(reverse("faculty:faculty-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_view_faculties(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("faculty:faculty-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_update_faculty(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Engineering Updated"}
        response = self.client.put(reverse("faculty:faculty-detail", args=[self.faculty.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.faculty.refresh_from_db()
        self.assertEqual(self.faculty.name, "Engineering Updated")

    def test_authenticated_user_without_permission_cannot_update_faculty(self):
        self.client.login(username="user", password="password")
        data = {"name": "Engineering Updated"}
        response = self.client.put(reverse("faculty:faculty-detail", args=[self.faculty.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_delete_faculty(self):
        self.client.login(username="admin", password="password")
        response = self.client.delete(reverse("faculty:faculty-detail", args=[self.faculty.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Faculty.objects.filter(id=self.faculty.id).exists())

    def test_authenticated_user_without_permission_cannot_delete_faculty(self):
        self.client.login(username="user", password="password")
        response = self.client.delete(reverse("faculty:faculty-detail", args=[self.faculty.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FacultyGroupViewSetTests(BaseTestCase):
    def test_anonymous_user_cannot_view_faculty_groups(self):
        response = self.client.get(reverse("faculty:facultygroup-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_create_faculty_group(self):
        data = {"name": "Mathematics", "faculty": self.faculty.id}
        response = self.client.post(reverse("faculty:facultygroup-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_create_faculty_group(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Mathematics", "faculty": self.faculty.id}
        response = self.client.post(reverse("faculty:facultygroup-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_without_permission_cannot_create_faculty_group(self):
        self.client.login(username="user", password="password")
        data = {"name": "Mathematics", "faculty": self.faculty.id}
        response = self.client.post(reverse("faculty:facultygroup-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_create_faculty_group(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Mathematics", "faculty": self.faculty.id}
        response = self.client.post(reverse("faculty:facultygroup-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_view_faculty_groups(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("faculty:facultygroup-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_update_faculty_group(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Computer Science Updated", "faculty": self.faculty.id}
        response = self.client.put(reverse("faculty:facultygroup-detail", args=[self.faculty_group.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.faculty_group.refresh_from_db()
        self.assertEqual(self.faculty_group.name, "Computer Science Updated")

    def test_authenticated_user_without_permission_cannot_update_faculty_group(self):
        self.client.login(username="user", password="password")
        data = {"name": "Computer Science Updated", "faculty": self.faculty.id}
        response = self.client.put(reverse("faculty:facultygroup-detail", args=[self.faculty_group.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_delete_faculty_group(self):
        self.client.login(username="admin", password="password")
        response = self.client.delete(reverse("faculty:facultygroup-detail", args=[self.faculty_group.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FacultyGroup.objects.filter(id=self.faculty_group.id).exists())

    def test_authenticated_user_without_permission_cannot_delete_faculty_group(self):
        self.client.login(username="user", password="password")
        response = self.client.delete(reverse("faculty:facultygroup-detail", args=[self.faculty_group.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FieldOfStudyViewSetTests(BaseTestCase):
    def test_anonymous_user_cannot_view_fields_of_study(self):
        response = self.client.get(reverse("faculty:fieldofstudy-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_create_field_of_study(self):
        data = {"name": "Physics", "faculty_group": self.faculty_group.id}
        response = self.client.post(reverse("faculty:fieldofstudy-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_create_field_of_study(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Physics", "faculty_group": self.faculty_group.id}
        response = self.client.post(reverse("faculty:fieldofstudy-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_without_permission_cannot_create_field_of_study(self):
        self.client.login(username="user", password="password")
        data = {"name": "Physics", "faculty_group": self.faculty_group.id}
        response = self.client.post(reverse("faculty:fieldofstudy-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_create_field_of_study(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Physics", "faculty_group": self.faculty_group.id}
        response = self.client.post(reverse("faculty:fieldofstudy-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_view_fields_of_study(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("faculty:fieldofstudy-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_update_field_of_study(self):
        self.client.login(username="admin", password="password")
        data = {"name": "Physics Updated", "faculty_group": self.faculty_group.id}
        response = self.client.put(reverse("faculty:fieldofstudy-detail", args=[self.field_of_study.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.field_of_study.refresh_from_db()
        self.assertEqual(self.field_of_study.name, "Physics Updated")

    def test_authenticated_user_without_permission_cannot_update_field_of_study(self):
        self.client.login(username="user", password="password")
        data = {"name": "Physics Updated", "faculty_group": self.faculty_group.id}
        response = self.client.put(reverse("faculty:fieldofstudy-detail", args=[self.field_of_study.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_delete_field_of_study(self):
        self.client.login(username="admin", password="password")
        response = self.client.delete(reverse("faculty:fieldofstudy-detail", args=[self.field_of_study.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FieldOfStudy.objects.filter(id=self.field_of_study.id).exists())

    def test_authenticated_user_without_permission_cannot_delete_field_of_study(self):
        self.client.login(username="user", password="password")
        response = self.client.delete(reverse("faculty:fieldofstudy-detail", args=[self.field_of_study.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AcademicFieldViewSetTests(BaseTestCase):
    def test_anonymous_user_cannot_view_academic_fields(self):
        response = self.client.get(reverse("faculty:academicfield-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_create_academic_field(self):
        data = {"academic_level": "Master", "field_of_study": self.field_of_study.id, "required_units": 120}
        response = self.client.post(reverse("faculty:academicfield-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_create_academic_field(self):
        self.client.login(username="admin", password="password")
        data = {"academic_level": "Master", "field_of_study": self.field_of_study.id, "required_units": 120}
        response = self.client.post(reverse("faculty:academicfield-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_without_permission_cannot_create_academic_field(self):
        self.client.login(username="user", password="password")
        data = {"academic_level": "Master", "field_of_study": self.field_of_study.id, "required_units": 120}
        response = self.client.post(reverse("faculty:academicfield-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_create_academic_field(self):
        self.client.login(username="admin", password="password")
        data = {"academic_level": "Master", "field_of_study": self.field_of_study.id, "required_units": 120}
        response = self.client.post(reverse("faculty:academicfield-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_view_academic_fields(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("faculty:academicfield-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_update_academic_field(self):
        self.client.login(username="admin", password="password")
        data = {"academic_level": "Master", "field_of_study": self.field_of_study.id, "required_units": 120}
        response = self.client.put(reverse("faculty:academicfield-detail", args=[self.academic_field.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.academic_field.refresh_from_db()
        self.assertEqual(self.academic_field.academic_level, "Master")

    def test_authenticated_user_without_permission_cannot_update_academic_field(self):
        self.client.login(username="user", password="password")
        data = {"academic_level": "Master", "field_of_study": self.field_of_study.id, "required_units": 120}
        response = self.client.put(reverse("faculty:academicfield-detail", args=[self.academic_field.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_permission_can_delete_academic_field(self):
        self.client.login(username="admin", password="password")
        response = self.client.delete(reverse("faculty:academicfield-detail", args=[self.academic_field.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AcademicField.objects.filter(id=self.academic_field.id).exists())

    def test_authenticated_user_without_permission_cannot_delete_academic_field(self):
        self.client.login(username="user", password="password")
        response = self.client.delete(reverse("faculty:academicfield-detail", args=[self.academic_field.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
