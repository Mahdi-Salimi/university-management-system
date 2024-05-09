import os
from django.core.management import call_command
from rest_framework.authentication import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from user.models import Assistant, Professor, Student

User = get_user_model()


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser",
            email="test@example.com",
            first_name="Amoo",
            last_name="Hasan",
            phone="09123456789",
            gender="M",
            national_id="1111111111",
            image=SimpleUploadedFile("test_image.jpg", b"empty", content_type="image/jpeg"),
        )

    def test_create_custom_user(self):
        self.assertTrue(User.objects.filter(pk=self.user.id).exists())
        self.assertEqual(self.user.username, "TestUser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "Amoo")
        self.assertEqual(self.user.last_name, "Hasan")
        self.assertEqual(self.user.phone, "09123456789")
        self.assertEqual(self.user.get_gender_display(), "Male")
        self.assertEqual(self.user.national_id, "1111111111")
        self.assertEqual(self.user.image, f"user_images/user_{self.user.username}.jpg")

    def test_phone_number_validation(self):
        self.user.full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", phone="0912345678").full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", phone="091234567890").full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", phone="08123456789").full_clean()

    def test_national_id_validation(self):
        self.user.full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", national_id="111111111").full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", national_id="11111111111").full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", national_id="2111111111").full_clean()
        with self.assertRaises(ValidationError):
            User(username="testuser", national_id="0000000001").full_clean()

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), "Amoo Hasan")
        user = User(username="testuser")
        self.assertEqual(str(user), "testuser")

    def tearDown(self) -> None:
        os.remove(str(self.user.image))


class CustomStudentTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_user(
            username="TestUser",
            email="test@example.com",
            first_name="Amoo",
            last_name="Hasan",
            phone="09123456789",
            gender="M",
            national_id="1111111111",
        )
        self.student = Student.objects.create(user=self.user)

    def test_create_student(self):
        self.assertTrue(Student.objects.filter(pk=self.student.id).exists())
        self.assertEqual(self.student.user, self.user)
        self.assertEqual(self.student.entry_semester, None)
        self.assertEqual(self.student.academic_field, None)
        self.assertEqual(self.student.professor, None)
        self.assertEqual(self.student.get_military_service_display(), "Subject to duty")
        self.assertEqual(self.student.get_status_display(), "Studying")
        self.assertEqual(self.student.allowed_half_years, 8)

    def test_get_role_student(self):
        try:
            self.assertEqual(self.student, self.user.get_role())
        except Exception:
            self.assertTrue(False)

    def test_get_faculty_student(self):
        # faculty models need to be implented
        ...

    def test_get_passed_courses(self):
        # course models need to be implented
        ...

    def test_get_current_courses(self):
        # course models need to be implented
        ...


class CustomProfessorTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_user(
            username="TestUser",
            email="test@example.com",
            first_name="Amoo",
            last_name="Hasan",
            phone="09123456789",
            gender="M",
            national_id="1111111111",
        )
        self.professor = Professor.objects.create(user=self.user)

    def test_create_student(self):
        self.assertTrue(Professor.objects.filter(pk=self.professor.id).exists())
        self.assertEqual(self.professor.user, self.user)
        self.assertEqual(self.professor.faculty_group, None)
        self.assertEqual(self.professor.get_rank_display(), "Assistant Professor")
        self.assertEqual(self.professor.expertise, None)

    def test_get_role_professor(self):
        try:
            self.assertEqual(self.professor, self.user.get_role())
        except Exception:
            self.assertTrue(False)

    def test_get_faculty_professor(self):
        # faculty models need to be implented
        ...


class CustomAssistantTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_user(
            username="TestUser",
            email="test@example.com",
            first_name="Amoo",
            last_name="Hasan",
            phone="09123456789",
            gender="M",
            national_id="1111111111",
        )
        self.evp = Assistant.objects.create(user=self.user)

    def test_create_student(self):
        self.assertTrue(Assistant.objects.filter(pk=self.evp.id).exists())
        self.assertEqual(self.evp.user, self.user)
        self.assertEqual(self.evp.faculty, None)

    def test_get_role_evp(self):
        try:
            self.assertEqual(self.evp, self.user.get_role())
        except Exception:
            self.assertTrue(False)

    def test_get_faculty_assistant(self):
        # faculty models need to be implented
        ...
