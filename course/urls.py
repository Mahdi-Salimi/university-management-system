from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'subjects', CourseViewSet)
router.register(r'semestercourses', SemesterCourseViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'studentsemesters', StudentSemesterViewSet)
router.register(r'studentcourse', StudentCourseViewSet)
router.register(r'coursetype', CourseTypeViewSet)
router.register(r'classsession', ClassSessionViewSet)





urlpatterns = [
    path('', include(router.urls)),
]
