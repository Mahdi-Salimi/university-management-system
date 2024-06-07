from django.test import TestCase

from faculty.serializers import (
    # AcademicFieldSerializer,
    FacultySerializer,
    # FacultyGroupSerializer,
    # FieldOfStudySerializer,
)

# from utils.models.choices import AcademicLevel
from faculty.views import (
    # AcademicFieldViewSet,
    FacultyViewSet,
    # FacultyGroupViewSet,
    # FieldOfStudyViewSet,
)


class FacultyViewSetTest(TestCase):
    def setUp(self):
        self.faculty_serializer = FacultySerializer(data={"name": "Faculty 1"})
        self.faculty_serializer.is_valid()
        self.faculty_serializer.save()

        self.faculty_serializer = FacultySerializer(data={"name": "Faculty 2"})
        self.faculty_serializer.is_valid()
        self.faculty_serializer.save()

        self.view = FacultyViewSet()

    def test_view_set(self):
        self.assertEqual(self.view.queryset.count(), 2)
        self.assertEqual(self.view.serializer_class, FacultySerializer)

    def test_create_url(self):
        response = self.client.get("/faculties/")
        self.assertEqual(response.status_code, 200)
