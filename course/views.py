from rest_framework import viewsets
from .models import Course, SemesterCourse
from .serializers import CourseSerializer, SemesterCourseSerializer
from .filters import CourseFilter, SemesterCourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class SemesterCourseViewSet(viewsets.ModelViewSet):
    queryset = SemesterCourse.objects.all()
    serializer_class =SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SemesterCourseFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


