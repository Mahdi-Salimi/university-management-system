from course.models import ClassSession, Course, CourseType, Semester, SemesterCourse, StudentCourse, StudentSemester
from rest_framework import serializers
from django.utils import timezone


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


def validate_semester_course(attrs):
    semester_end_modification_date = attrs["semester"].end_course_modification
    if semester_end_modification_date < timezone.now():
        raise serializers.ValidationError("Cannot create semester course. Semester's end modification date has passed.")
    return attrs


class SemesterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterCourse
        fields = "__all__"

    def validate(self, attrs):
        return validate_semester_course(attrs)

    def validate_exam_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Exam date and time cannot be in the past.")
        return value


def validate_semester(attrs):
    start_course_registration = attrs["start_course_registration"]
    end_course_registration = attrs["end_course_registration"]
    start_class_date = attrs["start_class_date"]
    end_class_date = attrs["end_class_date"]
    start_course_modification = attrs["start_course_modification"]
    end_course_modification = attrs["end_course_modification"]
    end_emergency_modification = attrs["end_emergency_modification"]
    start_exam_date = attrs["start_exam_date"]
    end_semester_date = attrs["end_semester_date"]

    if end_course_registration < start_course_registration:
        raise serializers.ValidationError("end_course_registration should be after start_course_registration")

    if end_class_date < start_class_date:
        raise serializers.ValidationError("end_class_date should be after start_class_date")

    if end_course_modification < start_course_modification:
        raise serializers.ValidationError("end_course_modification should be after start_course_modification")

    if end_emergency_modification < end_course_modification or end_emergency_modification > start_exam_date:
        raise serializers.ValidationError(
            "emergency modification date should not be before end normal modification date and not after starting exams!"
        )

    if end_semester_date < start_exam_date:
        raise serializers.ValidationError("end_semester_date should not be before exams")

    return attrs


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"

    def validate(self, attrs):
        return validate_semester(attrs)


class StudentSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSemester
        fields = "__all__"


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = "__all__"


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = "__all__"


class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = "__all__"
