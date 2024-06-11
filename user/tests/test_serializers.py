from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from user.models import Assistant, Professor, Student
from user.serializers import (
    AssistantSerializer,
    ChangePasswordRequestSerializer,
    ChangePasswordVerifySerializer,
    ProfessorSerializer,
    StudentSerializer,
    UserSerializer,
)
from course.models import Semester
from faculty.models import AcademicField, AcademicLevel, Faculty, FacultyGroup, FieldOfStudy

User = get_user_model()


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_with_perm = User.objects.create_user(username="withperm", password="pass")
        perm = Permission.objects.get(codename="change_customuser")
        self.user_with_perm.user_permissions.add(perm)
        self.user = User.objects.create_user(username="user", password="pass")

    def test_user_creation(self):
        user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "09123456789",
            "national_id": "1111111111",
            "gender": "M",
            "birthdate": "1990-01-01",
            "password": "password123",
        }
        request = APIRequestFactory().request()
        request.user = self.user_with_perm
        user_serializer = UserSerializer(data=user_data, context={"request": request})
        self.assertTrue(user_serializer.is_valid())
        user = user_serializer.save()
        self.assertIsInstance(user, User)
        self.assertTrue(User.objects.filter(id=user.id).exists())

    def test_username_change(self):
        user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "09123456789",
            "national_id": "1111111111",
            "gender": "M",
            "birthdate": "1990-01-01",
            "password": "password123",
        }
        request = APIRequestFactory().request()
        request.user = self.user_with_perm
        user_serializer = UserSerializer(data=user_data, context={"request": request})
        user_serializer.is_valid()
        user = user_serializer.save()
        user_data["username"] = "newusername"
        request = APIRequestFactory().request()
        request.user = self.user
        user_serializer = UserSerializer(data=user_data, instance=user, context={"request": request})
        self.assertTrue(user_serializer.is_valid())
        user = user_serializer.save()
        self.assertNotEqual(user_data["username"], user.username)
        self.assertFalse(User.objects.filter(username=user_data["username"]).exists())
        request = APIRequestFactory().request()
        request.user = self.user_with_perm
        user_serializer = UserSerializer(data=user_data, instance=user, context={"request": request})
        self.assertTrue(user_serializer.is_valid())
        user = user_serializer.save()
        self.assertEqual(user_data["username"], user.username)
        self.assertTrue(User.objects.filter(username=user_data["username"]).exists())

    def test_username_read_only(self):
        user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "09123456789",
            "national_id": "1111111111",
            "gender": "M",
            "birthdate": "1990-01-01",
            "password": "password123",
        }
        request = APIRequestFactory().request()
        request.user = self.user
        user_serializer = UserSerializer(data=user_data, context={"request": request})
        self.assertTrue(user_serializer.fields["username"].read_only)
        request.user = self.user_with_perm
        user_serializer = UserSerializer(data=user_data, context={"request": request})
        self.assertFalse(user_serializer.fields["username"].read_only)


class TestStudentSerializers(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_superuser(
            username="request_user",
            password="pass",
        )
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
        self.faculty = Faculty.objects.create(name="Test Faculty")
        self.group = FacultyGroup.objects.create(
            name="Test Group",
            faculty=self.faculty,
        )
        self.field_of_study = FieldOfStudy.objects.create(
            name="test field",
            faculty_group=self.group,
        )
        self.academic_field = AcademicField.objects.create(
            academic_level=AcademicLevel.BACHELOR,
            field_of_study=self.field_of_study,
            required_units=136,
        )
        self.valid_user_data = {
            "username": "testtest",
            "first_name": "Bahman",
            "last_name": "Hashemi",
            "national_id": "1111111111",
        }
        self.valid_student_data = {
            "entry_semester": self.semester.id,
            "academic_field": self.academic_field.id,
            "military_service": "N",
            "status": "S",
            "allowed_half_years": 8,
            "user": self.valid_user_data,
        }

    def test_student_serializer_create(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = StudentSerializer(
            data=self.valid_student_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsInstance(instance, Student)
        self.assertTrue(Student.objects.filter(id=instance.id).exists())
        self.assertTrue(User.objects.filter(username=instance.user.username).exists())

    def test_student_serializer_update(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = StudentSerializer(
            data=self.valid_student_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        updated_data = self.valid_student_data.copy()
        updated_data["user"]["username"] = "testtesttest"
        updated_data["user"]["first_name"] = "Batman"
        updated_data["status"] = "G"
        serializer = StudentSerializer(
            data=updated_data,
            instance=instance,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        updated_instance = serializer.save()
        self.assertEqual(
            updated_instance.user.first_name,
            updated_data["user"]["first_name"],
        )
        self.assertEqual(
            updated_instance.status,
            updated_data["status"],
        )
        self.assertEqual(
            Student.objects.get(id=instance.id).status,
            updated_data["status"],
        )
        self.assertTrue(
            User.objects.get(id=instance.user.id).first_name,
            updated_data["user"]["first_name"],
        )

    def test_student_serializer_partial_update(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = StudentSerializer(
            data=self.valid_student_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        updated_data = {
            "user": {
                "first_name": "Batman",
            },
            "status": "G",
        }
        serializer = StudentSerializer(
            data=updated_data,
            instance=instance,
            partial=True,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        updated_instance = serializer.save()
        self.assertEqual(
            updated_instance.user.first_name,
            updated_data["user"]["first_name"],
        )
        self.assertEqual(
            updated_instance.status,
            updated_data["status"],
        )
        self.assertEqual(
            Student.objects.get(id=instance.id).status,
            updated_data["status"],
        )
        self.assertTrue(
            User.objects.get(id=instance.user.id).first_name,
            updated_data["user"]["first_name"],
        )

    def test_student_serializer_validate_user(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = StudentSerializer(
            data=self.valid_student_data,
            context={"request": request},
        )
        serializer.is_valid()
        serializer.save()
        serializer = StudentSerializer(
            data=self.valid_student_data,
            context={"request_user": self.user},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)


class TestProfessorSerializers(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_superuser(
            username="request_user",
            password="pass",
        )
        self.faculty = Faculty.objects.create(name="Test Faculty")
        self.group = FacultyGroup.objects.create(
            name="Test Group",
            faculty=self.faculty,
        )
        self.valid_user_data = {
            "username": "test_professor",
            "first_name": "Bahman",
            "last_name": "Hashemi",
            "national_id": "1111111111",
        }
        self.valid_professor_data = {
            "faculty_group": self.group.id,
            "rank": "A",
            "user": self.valid_user_data,
        }

    def test_professor_serializer_create(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = ProfessorSerializer(
            data=self.valid_professor_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsInstance(instance, Professor)
        self.assertTrue(Professor.objects.filter(id=instance.id).exists())
        self.assertTrue(User.objects.filter(username=instance.user.username).exists())

    def test_professor_serializer_update(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = ProfessorSerializer(
            data=self.valid_professor_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        updated_data = self.valid_professor_data.copy()
        updated_data["user"]["first_name"] = "Batman"
        updated_data["rank"] = "B"
        updated_data["user"].pop("username")
        serializer = ProfessorSerializer(
            data=updated_data,
            instance=instance,
            partial=True,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        updated_instance = serializer.save()
        self.assertEqual(
            updated_instance.user.first_name,
            updated_data["user"]["first_name"],
        )
        self.assertEqual(
            updated_instance.rank,
            updated_data["rank"],
        )
        self.assertEqual(
            Professor.objects.get(id=instance.id).rank,
            updated_data["rank"],
        )
        self.assertTrue(
            User.objects.get(id=instance.user.id).first_name,
            updated_data["user"]["first_name"],
        )

    def test_professor_serializer_validate_user(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = ProfessorSerializer(
            data=self.valid_professor_data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = ProfessorSerializer(
            data=self.valid_professor_data,
            context={"request_user": self.user},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)


class TestAssistantSerializers(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_superuser(
            username="request_user",
            password="pass",
        )
        self.faculty = Faculty.objects.create(name="Test Faculty")
        self.valid_user_data = {
            "username": "test_assistant",
            "first_name": "Bahman",
            "last_name": "Hashemi",
            "national_id": "1111111111",
        }
        self.valid_assistant_data = {
            "faculty": self.faculty.id,
            "user": self.valid_user_data,
        }

    def test_assistant_serializer_create(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = AssistantSerializer(
            data=self.valid_assistant_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsInstance(instance, Assistant)
        self.assertTrue(Assistant.objects.filter(id=instance.id).exists())
        self.assertTrue(User.objects.filter(username=instance.user.username).exists())

    def test_assistant_serializer_update(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = AssistantSerializer(
            data=self.valid_assistant_data,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        updated_data = self.valid_assistant_data.copy()
        updated_data["user"]["first_name"] = "Batman"
        updated_data["user"].pop("username")
        serializer = AssistantSerializer(
            data=updated_data,
            instance=instance,
            partial=True,
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid())
        updated_instance = serializer.save()
        self.assertEqual(
            updated_instance.user.first_name,
            updated_data["user"]["first_name"],
        )
        self.assertTrue(
            User.objects.get(id=instance.user.id).first_name,
            updated_data["user"]["first_name"],
        )

    def test_assistant_serializer_validate_user(self):
        request = APIRequestFactory().request()
        request.user = self.user
        serializer = AssistantSerializer(
            data=self.valid_assistant_data,
            context={"request": request},
        )
        serializer.is_valid()
        serializer.save()
        serializer = AssistantSerializer(
            data=self.valid_assistant_data,
            context={"request_user": self.user},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)


class TestChangePasswordRequestSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="request_user",
            password="pass",
        )

    def test_change_password(self):
        serializer = ChangePasswordRequestSerializer(
            data={"username": self.user.username},
        )
        self.assertTrue(serializer.is_valid())


class TestChangePasswordVerifySerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="request_user",
            password="pass",
        )

    def test_change_password(self):
        new_pass = "Pa$$word123"
        data = {
            "username": self.user.username,
            "new_password": new_pass,
            "confirm_new_password": new_pass,
            "otp": "nothing",
        }
        serializer = ChangePasswordVerifySerializer(
            data=data,
        )
        self.assertTrue(serializer.is_valid())
        self.user = serializer.change_password(self.user)
        self.assertTrue(self.user.check_password(new_pass))

    def test_change_invalid_password(self):
        new_pass = "Pass"
        data = {
            "username": self.user.username,
            "new_password": new_pass,
            "confirm_new_password": new_pass,
            "otp": "nothing",
        }
        serializer = ChangePasswordVerifySerializer(
            data=data,
        )
        self.assertRaises(AssertionError, serializer.change_password, user=self.user)
        self.assertRaises(serializers.ValidationError, serializer.is_valid, raise_exception=True)
        self.assertRaises(AssertionError, serializer.change_password, user=self.user)

    def test_change_no_match_password(self):
        new_pass = "Pass"
        data = {
            "username": self.user.username,
            "new_password": new_pass,
            "confirm_new_password": new_pass + "s",
            "otp": "nothing",
        }
        serializer = ChangePasswordVerifySerializer(
            data=data,
        )
        self.assertRaises(serializers.ValidationError, serializer.is_valid, raise_exception=True)
        self.assertRaises(AssertionError, serializer.change_password, user=self.user)
