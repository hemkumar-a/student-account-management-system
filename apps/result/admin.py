from django.contrib import admin

from .models import AssessmentResult, Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "total_score",
        "grade",
        "point",
        "session",
        "semester",
    )
    list_filter = (
        "grade",
        "session",
        "semester",
    )
    search_fields = (
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
        "course__code",
        "course__title",
    )


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "cgpa",
        "updated_at",
    )
    search_fields = (
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
    )