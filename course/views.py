from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from .filters import CourseFilter, SemesterCourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    permission_classes = [DjangoModelPermissions]

