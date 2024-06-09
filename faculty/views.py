from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Faculty, FacultyGroup, FieldOfStudy, AcademicField
from .serializers import FacultySerializer, FacultyGroupSerializer, FieldOfStudySerializer, AcademicFieldSerializer


class FacultyViewSet(ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class FacultyGroupViewSet(ModelViewSet):
    queryset = FacultyGroup.objects.all()
    serializer_class = FacultyGroupSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class FieldOfStudyViewSet(ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AcademicFieldViewSet(ModelViewSet):
    queryset = AcademicField.objects.all()
    serializer_class = AcademicFieldSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
