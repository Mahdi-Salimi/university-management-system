from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SemesterCourseViewSet

router = DefaultRouter()
router.register(r'subjects', CourseViewSet)
router.register(r'semestercourses', SemesterCourseViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
