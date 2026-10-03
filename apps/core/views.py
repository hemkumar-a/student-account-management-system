from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.accounts.models import StudentProfile


def home(request):
    return render(
        request,
        "core/home.html",
    )


@login_required
def dashboard(request):
    if request.user.is_staff:
        context = {
            "total_students": StudentProfile.objects.count(),
            "active_students": StudentProfile.objects.filter(
                status=StudentProfile.STATUS_ACTIVE
            ).count(),
            "graduated_students": StudentProfile.objects.filter(
                status=StudentProfile.STATUS_GRADUATED
            ).count(),
            "suspended_students": StudentProfile.objects.filter(
                status=StudentProfile.STATUS_SUSPENDED
            ).count(),
        }

        return render(
            request,
            "core/dashboard.html",
            context,
        )

    student = getattr(
        request.user,
        "student_profile",
        None,
    )

    context = {
        "student": student,
    }

    return render(
        request,
        "core/student_dashboard.html",
        context,
    )