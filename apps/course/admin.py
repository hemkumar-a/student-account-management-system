from django.contrib import admin

from .models import Course, CourseAllocation, Department, Program


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("title", "code")
    search_fields = ("title", "code")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "department")
    list_filter = ("department",)
    search_fields = ("title", "department__title")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
        "program",
        "semester",
        "credit",
        "is_elective",
    )
    list_filter = (
        "semester",
        "is_elective",
        "program",
    )
    search_fields = (
        "code",
        "title",
        "program__title",
    )


@admin.register(CourseAllocation)
class CourseAllocationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "session",
        "created_at",
    )
    list_filter = ("session",)
    search_fields = (
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
    )
    filter_horizontal = ("courses",)