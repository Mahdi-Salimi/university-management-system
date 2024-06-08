from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from rest_framework.authentication import get_user_model
from .models import Assistant, Professor, Student

User = get_user_model()

admin.site.register(Permission)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "national_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "gender",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "is_active",
        "is_superuser",
        "is_staff",
        "last_login",
        "date_joined",
    )
    search_fields = (
        "username__icontains",
        "national_id__icontains",
        "first_name__icontains",
        "last_name__icontains",
        "email__icontains",
        "phone__contains",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Image", {"fields": ("image",)}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "national_id",
                    "gender",
                    "email",
                    "phone",
                    "birthdate",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "entry_semester",
        "academic_field",
        "professor",
        "military_service",
        "status",
    )
    list_filter = (
        "status",
        "military_service",
        "entry_semester",
        "user__gender",
    )
    search_fields = (
        "user__first_name__icontains",
        "user__last_name__icontains",
        "user__username__icontains",
        "user__national_id__icontains",
    )


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "faculty_group",
        "rank",
        "expertise",
    )
    list_filter = ("rank",)
    search_fields = (
        "user__first_name__icontains",
        "user__last_name__icontains",
        "user__username__icontains",
        "user__national_id__icontains",
    )


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "faculty",
    )
    list_filter = ("faculty", "user__gender")
    search_fields = (
        "user__first_name__icontains",
        "user__last_name__icontains",
        "user__username__icontains",
        "user__national_id__icontains",
    )
