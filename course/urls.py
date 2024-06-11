from django.urls import path, include
from rest_framework.routers import DefaultRouter
import course.views as views

router = DefaultRouter()
router.register(r"subjects", views.CourseViewSet)
router.register(r"semestercourses", views.SemesterCourseViewSet)
router.register(r"semesters", views.SemesterViewSet)
router.register(r"studentsemesters", views.StudentSemesterViewSet)
router.register(r"studentcourse", views.StudentCourseViewSet)
router.register(r"coursetype", views.CourseTypeViewSet)
router.register(r"classsession", views.ClassSessionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
