from typing import Any
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.conf import settings

PERM_GROUPS = settings.PERM_GROUPS
STUDENTS_GROUP = PERM_GROUPS["STUDENTS"]
PROFESSORS_GROUP = PERM_GROUPS["PROFESSORS"]
ASSISTANT_GROUP = PERM_GROUPS["ASSISTANTS"]


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            students = Group.objects.get(name=STUDENTS_GROUP)
            students.delete()
        except Group.DoesNotExist:
            pass
        finally:
            students = Group.objects.create(name=STUDENTS_GROUP)
        try:
            professors = Group.objects.get(name=PROFESSORS_GROUP)
            professors.delete()
        except Group.DoesNotExist:
            pass
        finally:
            professors = Group.objects.create(name=PROFESSORS_GROUP)
        try:
            evps = Group.objects.get(name=ASSISTANT_GROUP)
            evps.delete()
        except Group.DoesNotExist:
            pass
        finally:
            evps = Group.objects.create(name=ASSISTANT_GROUP)

        # Students
        view_student_self = Permission.objects.get(codename="view_student_self")
        change_student_self = Permission.objects.get(codename="change_student_self")

        students.permissions.add(view_student_self)
        students.permissions.add(change_student_self)

        # Professors
        view_professor_self = Permission.objects.get(codename="view_student_self")
        change_professor_self = Permission.objects.get(codename="change_student_self")

        professors.permissions.add(view_professor_self)
        professors.permissions.add(change_professor_self)

        # Assistants
        view_students_faculty = Permission.objects.get(codename="view_student_faculty")

        view_professors_faculty = Permission.objects.get(codename="view_professor_faculty")

        evps.permissions.add(view_students_faculty)
        evps.permissions.add(view_professors_faculty)
