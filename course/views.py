from rest_framework import viewsets
import course.models as models
import course.serializers as serializers
from .filters import CourseFilter, SemesterCourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import DefaultPermissionOrAnonReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    permission_classes = [DefaultPermissionOrAnonReadOnly]


class SemesterCourseViewSet(viewsets.ModelViewSet):
    queryset = models.SemesterCourse.objects.all()
    serializer_class = serializers.SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SemesterCourseFilter
    permission_classes = [DefaultPermissionOrAnonReadOnly]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]


class StudentSemesterViewSet(viewsets.ModelViewSet):
    queryset = models.StudentSemester.objects.all()
    serializer_class = serializers.StudentSemesterSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]


class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = models.StudentCourse.objects.all()
    serializer_class = serializers.StudentCourseSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]


class CourseTypeViewSet(viewsets.ModelViewSet):
    queryset = models.CourseType.objects.all()
    serializer_class = serializers.CourseTypeSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]


class ClassSessionViewSet(viewsets.ModelViewSet):
    queryset = models.ClassSession.objects.all()
    serializer_class = serializers.ClassSessionSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]
