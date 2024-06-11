from rest_framework import viewsets
from .models import *
from .serializers import *
from .filters import CourseFilter, SemesterCourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import DefaultPermissionOrAnonReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    permission_classes = [DefaultPermissionOrAnonReadOnly]
    
class SemesterCourseViewSet(viewsets.ModelViewSet):
    queryset = SemesterCourse.objects.all()
    serializer_class =SemesterCourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SemesterCourseFilter
    permission_classes = [DefaultPermissionOrAnonReadOnly]
    
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class =SemesterSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]

class StudentSemesterViewSet(viewsets.ModelViewSet):
    queryset = StudentSemester.objects.all()
    serializer_class =StudentSemesterSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]
    
class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class =StudentCourseSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]
    
class CourseTypeViewSet(viewsets.ModelViewSet):
    queryset = CourseType.objects.all()
    serializer_class =CourseTypeSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]
    
class ClassSessionViewSet(viewsets.ModelViewSet):
    queryset = ClassSession.objects.all()
    serializer_class =ClassSessionSerializer
    permission_classes = [DefaultPermissionOrAnonReadOnly]
    