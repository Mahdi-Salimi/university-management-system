from django.core.management import call_command
from django.test import TestCase
from rest_framework.authentication import get_user_model
from user.models import Student, Professor, Assistant

User = get_user_model()


class EducationalVPAdminTest(TestCase):
    def setUp(self):
        call_command("create_perm_groups")
        self.user = User.objects.create_user(username="test_user", password="pass")

    def test_student_delete(self):
        student = Student.objects.create(user=self.user)
        student.delete()
        self.assertFalse(User.objects.filter(username=self.user.username).exists())

    def test_professor_delete(self):
        professor = Professor.objects.create(user=self.user)
        professor.delete()
        self.assertFalse(User.objects.filter(username=self.user.username).exists())

    def test_assistant_delete(self):
        assistant = Assistant.objects.create(user=self.user)
        assistant.delete()
        self.assertFalse(User.objects.filter(username=self.user.username).exists())
