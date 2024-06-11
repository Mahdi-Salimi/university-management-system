from django.core.management import call_command
from django.test import TestCase
from rest_framework.authentication import get_user_model
from user.models import Assistant, Professor, Student
from utils.models.choices import GenderChoices, ProfessorRankChoices, StudentStatusChoices

User = get_user_model()


class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            username="admin",
            password="password",
            first_name="Bahman",
            last_name="Hashemi",
            email="test@noemail.invalid",
            phone="09123456789",
        )
        self.user = User.objects.create_user(
            username="normal",
            password="password",
            first_name="Amoo",
            last_name="Hasan",
            email="test1@email.invalid",
            phone="09133456788",
            is_active=False,
        )

    def test_custom_user_model_admin_list_display(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get("/admin/user/customuser/")
        self.assertContains(response, "username")
        self.assertContains(response, "national_id")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "email")
        self.assertContains(response, "phone")
        self.assertContains(response, "gender")
        self.assertContains(response, "is_active")
        self.assertContains(response, "is_staff")
        self.assertContains(response, "is_superuser")

    def test_custom_user_model_admin_search(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/customuser/?q={self.super_user.username}")
        self.assertContains(response, str(self.super_user))
        self.assertNotContains(response, str(self.user))
        response = self.client.get(f"/admin/user/customuser/?q={self.super_user.email}")
        self.assertContains(response, str(self.super_user))
        self.assertNotContains(response, str(self.user))
        response = self.client.get("/admin/user/customuser/?q=0912")
        self.assertContains(response, str(self.super_user))
        self.assertNotContains(response, str(self.user))
        response = self.client.get(f"/admin/user/customuser/?q={self.super_user.first_name}")
        self.assertContains(response, str(self.super_user))
        self.assertNotContains(response, str(self.user))

    def test_custom_user_model_admin_filter(self):
        self.client.login(username=self.super_user.username, password="password")
        filter_params = {"is_active": True}
        response = self.client.get("/admin/user/customuser/", data=filter_params)
        self.assertContains(response, self.super_user.username)
        self.assertNotContains(response, self.user.username)

    def test_custom_user_model_admin_permissions(self):
        response = self.client.get("/admin/user/customuser/")
        self.assertEqual(response.status_code, 302)

        self.user.is_active = True
        self.user.save()
        self.client.login(username=self.user.username, password="password")
        response = self.client.get("/admin/user/customuser/")
        self.assertEqual(response.status_code, 302)

    def test_custom_user_model_admin_fieldtest(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/customuser/{self.super_user.id}/change/")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Image:")
        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "National id:")
        self.assertContains(response, "Gender:")
        self.assertContains(response, "Birthdate:")
        self.assertContains(response, "Email address:")
        self.assertContains(response, "Phone:")
        self.assertContains(response, "Permissions")
        self.assertContains(response, "Last login:")
        self.assertContains(response, "Date joined:")


class StudentAdminTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.super_user = User.objects.create_superuser(
            username="admin",
            password="password",
            first_name="Bahman",
            last_name="Hashemi",
            email="test@noemail.invalid",
            phone="09123456789",
        )
        self.student = Student.objects.create(user=self.super_user)

    def test_custom_user_model_admin_list_display(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get("/admin/user/student/")
        self.assertContains(response, "user")
        self.assertContains(response, "entry_semester")
        self.assertContains(response, "academic_field")
        self.assertContains(response, "professor")
        self.assertContains(response, "military_service")
        self.assertContains(response, "status")

    def test_custom_user_model_admin_search(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/student/?q={self.super_user}")
        self.assertContains(response, str(self.student))
        response = self.client.get("/admin/user/student/?q=nothing")
        self.assertNotContains(response, str(self.student))

    def test_custom_user_model_admin_filter(self):
        self.client.login(username=self.super_user.username, password="password")
        filter_params = {"status": StudentStatusChoices.STUDYING}
        response = self.client.get("/admin/user/student/", data=filter_params)
        self.assertContains(response, self.super_user)
        filter_params = {"status": GenderChoices.MALE}
        response = self.client.get("/admin/user/student/", data=filter_params)
        self.assertNotContains(response, self.super_user)

    def test_custom_user_model_admin_fieldtest(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/student/{self.student.id}/change/")
        self.assertContains(response, "User:")
        self.assertContains(response, "Entry semester:")
        self.assertContains(response, "Academic field:")
        self.assertContains(response, "Professor:")
        self.assertContains(response, "Military service:")
        self.assertContains(response, "Status:")


class ProfessorAdminTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.super_user = User.objects.create_superuser(
            username="admin",
            password="password",
            first_name="Bahman",
            last_name="Hashemi",
            email="test@noemail.invalid",
            phone="09123456789",
        )
        self.professor = Professor.objects.create(user=self.super_user)

    def test_custom_user_model_admin_list_display(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get("/admin/user/professor/")
        self.assertContains(response, "user")
        self.assertContains(response, "faculty_group")
        self.assertContains(response, "rank")
        self.assertContains(response, "expertise")

    def test_custom_user_model_admin_search(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/professor/?q={self.super_user}")
        self.assertContains(response, str(self.professor))
        response = self.client.get("/admin/user/professor/?q=nothing")
        self.assertNotContains(response, str(self.professor))

    def test_custom_user_model_admin_filter(self):
        self.client.login(username=self.super_user.username, password="password")
        filter_params = {"rank": ProfessorRankChoices.ASSISTANT}
        response = self.client.get("/admin/user/professor/", data=filter_params)
        self.assertContains(response, self.super_user)
        filter_params = {"rank": ProfessorRankChoices.PROFESSOR}
        response = self.client.get("/admin/user/professor/", data=filter_params)
        self.assertNotContains(response, self.super_user)

    def test_custom_user_model_admin_fieldtest(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/professor/{self.professor.id}/change/")
        self.assertContains(response, "User:")
        self.assertContains(response, "Faculty group:")
        self.assertContains(response, "Rank:")
        self.assertContains(response, "Expertise:")


class AssistantAdminTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.super_user = User.objects.create_superuser(
            username="admin",
            password="password",
            first_name="Bahman",
            last_name="Hashemi",
            email="test@noemail.invalid",
            phone="09123456789",
        )
        self.evp = Assistant.objects.create(user=self.super_user)

    def test_custom_user_model_admin_list_display(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get("/admin/user/assistant/")
        self.assertContains(response, "user")

    def test_custom_user_model_admin_search(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/assistant/?q={self.super_user}")
        self.assertContains(response, str(self.evp))
        response = self.client.get("/admin/user/assistant/?q=nothing")
        self.assertNotContains(response, str(self.evp))

    def test_custom_user_model_admin_filter(self):
        self.client.login(username=self.super_user.username, password="password")
        filter_params = {"user__gender": GenderChoices.FEMALE}
        response = self.client.get("/admin/user/assistant/", data=filter_params)
        self.assertContains(response, self.super_user)
        filter_params = {"user__gender": GenderChoices.MALE}
        response = self.client.get("/admin/user/assistant/", data=filter_params)
        self.assertNotContains(response, self.super_user)

    def test_custom_user_model_admin_fieldtest(self):
        self.client.login(username=self.super_user.username, password="password")
        response = self.client.get(f"/admin/user/assistant/{self.evp.id}/change/")
        self.assertContains(response, "User:")
        self.assertContains(response, "Faculty:")
