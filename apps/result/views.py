from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AssessmentResultForm, ResultForm
from .models import AssessmentResult, Result


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_authenticated and user.is_staff)(
        view_func
    )


@login_required
def result_list(request):
    results = Result.objects.select_related(
        "student",
        "student__user",
        "course",
    ).order_by("-session", "student__student_id")

    if not request.user.is_staff:
        student = getattr(request.user, "student_profile", None)

        if student:
            results = results.filter(student=student)
        else:
            results = results.none()

    return render(
        request,
        "result/result_list.html",
        {"results": results},
    )


@login_required
def result_detail(request, pk):
    result = get_object_or_404(
        Result.objects.select_related(
            "student",
            "student__user",
            "course",
        ),
        pk=pk,
    )

    if not request.user.is_staff:
        student = getattr(request.user, "student_profile", None)

        if result.student != student:
            return redirect("result:result_list")

    return render(
        request,
        "result/result_detail.html",
        {"result": result},
    )


@staff_required
def result_create(request):
    if request.method == "POST":
        form = ResultForm(request.POST)

        if form.is_valid():
            result = form.save()
            messages.success(
                request,
                f"Result for {result.student.full_name} added successfully.",
            )
            return redirect("result:result_list")
    else:
        form = ResultForm()

    return render(
        request,
        "result/result_form.html",
        {
            "form": form,
            "title": "Add Result",
        },
    )


@staff_required
def result_edit(request, pk):
    result = get_object_or_404(Result, pk=pk)

    if request.method == "POST":
        form = ResultForm(request.POST, instance=result)

        if form.is_valid():
            form.save()
            messages.success(request, "Result updated successfully.")
            return redirect("result:result_detail", pk=result.pk)
    else:
        form = ResultForm(instance=result)

    return render(
        request,
        "result/result_form.html",
        {
            "form": form,
            "title": "Edit Result",
        },
    )


@staff_required
def result_delete(request, pk):
    result = get_object_or_404(Result, pk=pk)

    if request.method == "POST":
        result.delete()
        messages.success(request, "Result deleted successfully.")
        return redirect("result:result_list")

    return render(
        request,
        "result/result_delete.html",
        {"result": result},
    )


@login_required
def transcript(request):
    student = getattr(request.user, "student_profile", None)

    if request.user.is_staff:
        student_id = request.GET.get("student")

        if student_id:
            from apps.accounts.models import StudentProfile

            student = get_object_or_404(
                StudentProfile,
                pk=student_id,
            )

    if not student:
        return render(
            request,
            "result/transcript.html",
            {
                "student": None,
                "results": [],
                "summary": None,
            },
        )

    results = Result.objects.filter(
        student=student
    ).select_related("course").order_by(
        "semester",
        "course__code",
    )

    total_credits = sum(result.course.credit for result in results)

    weighted_points = sum(
        result.point * result.course.credit
        for result in results
    )

    cgpa = (
        round(weighted_points / total_credits, 2)
        if total_credits
        else 0
    )

    summary = {
        "total_courses": results.count(),
        "total_credits": total_credits,
        "cgpa": cgpa,
    }

    return render(
        request,
        "result/transcript.html",
        {
            "student": student,
            "results": results,
            "summary": summary,
        },
    )


@login_required
def performance(request):
    student = getattr(request.user, "student_profile", None)

    if request.user.is_staff:
        student_id = request.GET.get("student")

        if student_id:
            from apps.accounts.models import StudentProfile

            student = get_object_or_404(
                StudentProfile,
                pk=student_id,
            )

    if not student:
        return render(
            request,
            "result/performance.html",
            {"student": None},
        )

    results = Result.objects.filter(
        student=student
    ).select_related("course")

    average_score = results.aggregate(
        average=Avg("total_score")
    )["average"]

    total_points = results.aggregate(
        total=Sum("point")
    )["total"] or 0

    passed = results.filter(
        grade__in=["A", "B", "C", "D"]
    ).count()

    failed = results.filter(
        grade="F"
    ).count()

    context = {
        "student": student,
        "results": results,
        "average_score": round(average_score, 2)
        if average_score is not None
        else 0,
        "total_points": total_points,
        "passed": passed,
        "failed": failed,
    }

    return render(
        request,
        "result/performance.html",
        context,
    )


@staff_required
def assessment_create(request):
    if request.method == "POST":
        form = AssessmentResultForm(request.POST)

        if form.is_valid():
            student = form.cleaned_data["student"]

            assessment, created = AssessmentResult.objects.get_or_create(
                student=student
            )

            assessment.calculate_cgpa()
            assessment.save()

            messages.success(
                request,
                "Student CGPA updated successfully.",
            )

            return redirect("result:transcript")
    else:
        form = AssessmentResultForm()

    return render(
        request,
        "result/assessment_form.html",
        {"form": form},
    )