from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import StudentProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "get_full_name",
        "is_student",
        "is_lecturer",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_student",
        "is_lecturer",
        "is_staff",
        "is_active",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "address",
                    "picture",
                )
            },
        ),
        (
            "Roles",
            {
                "fields": (
                    "is_student",
                    "is_lecturer",
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
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = "Name"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "full_name",
        "department",
        "status",
        "admission_date",
    )
    list_filter = ("status", "department")
    search_fields = (
        "student_id",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    ordering = ("student_id",)