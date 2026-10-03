from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CourseAllocationForm,
    CourseForm,
    DepartmentForm,
    ProgramForm,
)
from .models import Course, CourseAllocation, Department, Program


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_authenticated and user.is_staff)(
        view_func
    )


@login_required
def course_list(request):
    courses = Course.objects.select_related("program", "program__department")

    search = request.GET.get("search", "").strip()

    if search:
        courses = courses.filter(
            Q(title__icontains=search)
            | Q(code__icontains=search)
            | Q(program__title__icontains=search)
            | Q(program__department__title__icontains=search)
        )

    context = {
        "courses": courses,
        "search": search,
    }

    return render(request, "course/course_list.html", context)


@login_required
def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related("program", "program__department"),
        pk=pk,
    )

    allocations = course.allocations.select_related(
        "student",
        "student__user",
    )

    return render(
        request,
        "course/course_detail.html",
        {
            "course": course,
            "allocations": allocations,
        },
    )


@staff_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Course created successfully.")
            return redirect("course:course_list")
    else:
        form = CourseForm()

    return render(
        request,
        "course/course_form.html",
        {
            "form": form,
            "title": "Add Course",
        },
    )


@staff_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect("course:course_detail", pk=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "course/course_form.html",
        {
            "form": form,
            "title": "Edit Course",
            "course": course,
        },
    )


@staff_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect("course:course_list")

    return render(
        request,
        "course/course_delete.html",
        {"course": course},
    )


@login_required
def department_list(request):
    departments = Department.objects.all().order_by("title")

    return render(
        request,
        "course/department_list.html",
        {"departments": departments},
    )


@staff_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect("course:department_list")
    else:
        form = DepartmentForm()

    return render(
        request,
        "course/department_form.html",
        {
            "form": form,
            "title": "Add Department",
        },
    )


@staff_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect("course:department_list")
    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        "course/department_form.html",
        {
            "form": form,
            "title": "Edit Department",
        },
    )


@staff_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        department.delete()
        messages.success(request, "Department deleted successfully.")
        return redirect("course:department_list")

    return render(
        request,
        "course/department_delete.html",
        {"department": department},
    )


@login_required
def program_list(request):
    programs = Program.objects.select_related("department").order_by(
        "department__title",
        "title",
    )

    return render(
        request,
        "course/program_list.html",
        {"programs": programs},
    )


@staff_required
def program_create(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Program created successfully.")
            return redirect("course:program_list")
    else:
        form = ProgramForm()

    return render(
        request,
        "course/program_form.html",
        {
            "form": form,
            "title": "Add Program",
        },
    )


@staff_required
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)

    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)

        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully.")
            return redirect("course:program_list")
    else:
        form = ProgramForm(instance=program)

    return render(
        request,
        "course/program_form.html",
        {
            "form": form,
            "title": "Edit Program",
        },
    )


@staff_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)

    if request.method == "POST":
        program.delete()
        messages.success(request, "Program deleted successfully.")
        return redirect("course:program_list")

    return render(
        request,
        "course/program_delete.html",
        {"program": program},
    )


@staff_required
def allocation_create(request):
    if request.method == "POST":
        form = CourseAllocationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Courses allocated successfully.")
            return redirect("course:allocation_list")
    else:
        form = CourseAllocationForm()

    return render(
        request,
        "course/allocation_form.html",
        {
            "form": form,
            "title": "Allocate Courses",
        },
    )


@login_required
def allocation_list(request):
    allocations = CourseAllocation.objects.select_related(
        "student",
        "student__user",
    ).prefetch_related("courses")

    if not request.user.is_staff:
        student = getattr(request.user, "student_profile", None)

        if student:
            allocations = allocations.filter(student=student)
        else:
            allocations = allocations.none()

    return render(
        request,
        "course/allocation_list.html",
        {"allocations": allocations},
    )