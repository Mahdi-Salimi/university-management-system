import django_filters
from .models import Course, SemesterCourse

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'faculty__name': ['icontains'],
            'name': ['icontains'],
        }
        
class SemesterCourseFilter(django_filters.FilterSet):
    class Meta:
        model = SemesterCourse
        fields = {
            'course__faculty__id': ['icontains'],
            'course__name': ['icontains'],
            'semester__academic_year': ['icontains'],
        }
