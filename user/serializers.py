from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authentication import get_user_model
from user.models import Student, Professor, Assistant
from utils.models.choices import StudentStatusChoices
from django.core import exceptions

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "national_id",
            "gender",
            "birthdate",
            "date_joined",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "image",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
        ]

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if self.context.get("request"):
            request_user = self.context.get("request").user
            if request_user and not (
                request_user.has_perm("user.change_customuser") or request_user.has_perm("user.add_student")
            ):
                fields["username"].read_only = True
                fields["is_active"].read_only = True

        return fields

    def create(self, validated_data):
        validated_data["password"] = validated_data["national_id"]
        user = User.objects.create_user(**validated_data)
        return user


class CustomModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        instance = self.Meta.model(**validated_data)
        user_serializer = UserSerializer(
            data=user_data,
            context={
                "request": self.context.get("request"),
            },
        )
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            instance.user = user
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(user_serializer.errors)

    def validate_user(self, value):
        if "national_id" in value:
            if not self.instance or (self.instance and self.instance.user.national_id != value["national_id"]):
                if self.Meta.model.objects.filter(user__national_id=value["national_id"]).exists():
                    raise serializers.ValidationError(
                        f"A {self.Meta.model._meta.model_name} with this National id already exists!"
                    )
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(
                instance=instance.user,
                data=user_data,
                partial=True,
                context={
                    "object": instance,
                    "request": self.context.get("request"),
                },
            )
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
                instance.user = user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class StudentSerializer(CustomModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "entry_semester",
            "academic_field",
            "professor",
            "military_service",
            "status",
            "allowed_half_years",
        ]
        read_only_fields = ["id"]

    def validate_user(self, value):
        if "national_id" in value:
            if not self.instance or (self.instance and self.instance.user.national_id != value["national_id"]):
                if (
                    Student.objects.filter(user__national_id=value["national_id"])
                    .exclude(status=StudentStatusChoices.DISMISSAL)
                    .exclude(status=StudentStatusChoices.GRADUATED)
                    .exclude(status=StudentStatusChoices.WITHDRAWAL)
                    .exists()
                ):
                    raise serializers.ValidationError("An active student with this National id already exists!")
        return value


class ProfessorSerializer(CustomModelSerializer):
    class Meta:
        model = Professor
        fields = [
            "id",
            "user",
            "faculty_group",
            "rank",
            "expertise",
        ]
        read_only_fields = ["id"]


class AssistantSerializer(CustomModelSerializer):
    class Meta:
        model = Assistant
        fields = [
            "id",
            "user",
            "faculty",
        ]
        read_only_fields = ["id"]


class UserPasswordSerializerField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["style"] = {"input_type": "password"}
        kwargs["write_only"] = True
        super().__init__(**kwargs)

    def validate(self, value):
        try:
            validate_password(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value


class ChangePasswordRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)


class ChangePasswordVerifySerializer(ChangePasswordRequestSerializer):
    new_password = UserPasswordSerializerField()
    confirm_new_password = UserPasswordSerializerField()
    otp = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        if data.get("new_password") != data.get("confirm_new_password"):
            raise serializers.ValidationError("Passwords doesn't match.")
        for field_name in ["new_password", "confirm_new_password"]:
            self.fields[field_name].validate(data[field_name])

        return data

    def change_password(self, user):
        assert hasattr(self, "_errors"), "You must call `.is_valid()` before calling `.change_password`."
        assert not self.errors, "You cannot call `.change_password` on a serializer with invalid data."
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user
