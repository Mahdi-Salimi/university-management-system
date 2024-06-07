from rest_framework.serializers import ModelSerializer

from .models import Faculty, FacultyGroup, FieldOfStudy, AcademicField


class FacultySerializer(ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class FacultyGroupSerializer(ModelSerializer):
    class Meta:
        model = FacultyGroup
        fields = "__all__"


class FieldOfStudySerializer(ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = "__all__"


class AcademicFieldSerializer(ModelSerializer):
    class Meta:
        model = AcademicField
        fields = "__all__"
