from django.test import TestCase

from faculty.models import (
    AcademicField,
    AcademicLevel,
    Faculty,
    FacultyGroup,
    FieldOfStudy,
)


class AcademicFieldModelTest(TestCase):
    def setUp(self):
        self.academic_field = AcademicField.objects.create(
            academic_level=AcademicLevel.BACHELOR,
            field_of_study=FieldOfStudy.objects.create(
                name="Field of Study",
                faculty_group=FacultyGroup.objects.create(
                    name="Faculty Group", faculty=Faculty.objects.create(name="Faculty")
                ),
            ),
            required_units=140,
        )

    def test_create_academic_field(self):
        self.assertEqual(AcademicField.objects.count(), 1)
        self.assertEqual(self.academic_field.academic_level, AcademicLevel.BACHELOR)
        self.assertEqual(self.academic_field.field_of_study.name, "Field of Study")
        self.assertEqual(self.academic_field.required_units, 140)

    def test_academic_field_str(self):
        self.assertEqual(str(self.academic_field), "BACHELOR - Field of Study")


class FacultyModelTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name="Faculty")

    def test_create_faculty(self):
        self.assertEqual(Faculty.objects.count(), 1)
        self.assertEqual(self.faculty.name, "Faculty")

    def test_faculty_str(self):
        self.assertEqual(str(self.faculty), "Faculty")


class FacultyGroupModelTest(TestCase):
    def setUp(self):
        self.faculty_group = FacultyGroup.objects.create(
            name="Faculty Group", faculty=Faculty.objects.create(name="Faculty")
        )

    def test_create_faculty_group(self):
        self.assertEqual(FacultyGroup.objects.count(), 1)
        self.assertEqual(self.faculty_group.name, "Faculty Group")
        self.assertEqual(self.faculty_group.faculty.name, "Faculty")

    def test_faculty_group_str(self):
        self.assertEqual(str(self.faculty_group), "Faculty - Faculty Group")


class FieldOfStudyModelTest(TestCase):
    def setUp(self):
        self.field_of_study = FieldOfStudy.objects.create(
            name="Field of Study",
            faculty_group=FacultyGroup.objects.create(
                name="Faculty Group", faculty=Faculty.objects.create(name="Faculty")
            ),
        )

    def test_create_field_of_study(self):
        self.assertEqual(FieldOfStudy.objects.count(), 1)
        self.assertEqual(self.field_of_study.name, "Field of Study")
        self.assertEqual(self.field_of_study.faculty_group.name, "Faculty Group")

    def test_field_of_study_str(self):
        self.assertEqual(str(self.field_of_study), "Field of Study")
