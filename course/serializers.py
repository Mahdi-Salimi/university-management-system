from .models import Course, SemesterCourse
from rest_framework import serializers
from time import timezone

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

def validate_semester_course(attrs):
    semester_end_modification_date = attrs['semester'].end_course_modification
    if semester_end_modification_date < timezone.now():
        raise serializers.ValidationError("Cannot create semester course. Semester's end modification date has passed.")
    return attrs
   
class SemesterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        fields = '__all__'
        
    def validate(self, attrs):
        return validate_semester_course(attrs)
    
    def validate_exam_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Exam date and time cannot be in the past.")
        return value   