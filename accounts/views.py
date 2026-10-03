from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    RegistrationForm,
    StudentCreateForm,
    StudentProfileForm,
    StudentStatusForm,
    UserUpdateForm,
)
from .models import StudentProfile, User


def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff
    )(view_func)


def generate_student_id():
    last_student = (
        StudentProfile.objects
        .order_by("-id")
        .first()
    )

    next_number = (
        (last_student.id + 1)
        if last_student
        else 1
    )

    return f"STU{next_number:05d}"


def register(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)

                user.set_password(
                    form.cleaned_data["password"]
                )

                user.is_student = True

                user.save()

                StudentProfile.objects.create(
                    user=user,
                    student_id=generate_student_id(),
                )

            login(request, user)

            messages.success(
                request,
                "Your student account has been created successfully.",
            )

            return redirect("core:dashboard")
    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


@login_required
def profile(request):
    student = getattr(
        request.user,
        "student_profile",
        None,
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "student": student,
        },
    )


@login_required
def profile_edit(request):
    student = getattr(
        request.user,
        "student_profile",
        None,
    )

    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        profile_form = (
            StudentProfileForm(
                request.POST,
                instance=student,
            )
            if student
            else None
        )

        if user_form.is_valid() and (
            profile_form is None
            or profile_form.is_valid()
        ):
            user_form.save()

            if profile_form:
                profile_form.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = (
            StudentProfileForm(
                instance=student
            )
            if student
            else None
        )

    return render(
        request,
        "accounts/profile_edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


@staff_required
def student_list(request):
    query = request.GET.get(
        "q",
        "",
    ).strip()

    students = (
        StudentProfile.objects
        .select_related(
            "user",
            "department",
        )
    )

    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
            | Q(department__title__icontains=query)
        )

    return render(
        request,
        "accounts/student_list.html",
        {
            "students": students,
            "query": query,
        },
    )


@staff_required
def student_detail(request, pk):
    student = get_object_or_404(
        StudentProfile.objects.select_related(
            "user",
            "department",
        ),
        pk=pk,
    )

    return render(
        request,
        "accounts/student_detail.html",
        {
            "student": student,
        },
    )


@staff_required
def student_create(request):
    if request.method == "POST":
        form = StudentCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)

                password = form.cleaned_data["password"]

                user.set_password(password)
                user.is_student = True
                user.save()

                StudentProfile.objects.create(
                    user=user,
                    student_id=generate_student_id(),
                )

            messages.success(
                request,
                "Student created successfully.",
            )

            return redirect(
                "accounts:student_list"
            )
    else:
        form = StudentCreateForm()

    return render(
        request,
        "accounts/student_form.html",
        {
            "form": form,
            "title": "Add Student",
        },
    )


@staff_required
def student_edit(request, pk):
    student = get_object_or_404(
        StudentProfile,
        pk=pk,
    )

    if request.method == "POST":
        form = StudentCreateForm(
            request.POST,
            instance=student.user,
        )

        if form.is_valid():
            user = form.save(
                commit=False
            )

            password = form.cleaned_data.get(
                "password"
            )

            if password:
                user.set_password(password)

            user.is_student = True
            user.save()

            messages.success(
                request,
                "Student updated successfully.",
            )

            return redirect(
                "accounts:student_detail",
                pk=student.pk,
            )
    else:
        form = StudentCreateForm(
            instance=student.user
        )

    return render(
        request,
        "accounts/student_form.html",
        {
            "form": form,
            "title": "Edit Student",
            "student": student,
        },
    )


@staff_required
def student_delete(request, pk):
    student = get_object_or_404(
        StudentProfile,
        pk=pk,
    )

    if request.method == "POST":
        student.user.delete()

        messages.success(
            request,
            "Student account deleted successfully.",
        )

        return redirect(
            "accounts:student_list"
        )

    return render(
        request,
        "accounts/student_detail.html",
        {
            "student": student,
            "confirm_delete": True,
        },
    )


@staff_required
def student_status(request, pk):
    student = get_object_or_404(
        StudentProfile,
        pk=pk,
    )

    if request.method == "POST":
        form = StudentStatusForm(
            request.POST,
            instance=student,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student status updated successfully.",
            )

            return redirect(
                "accounts:student_detail",
                pk=student.pk,
            )
    else:
        form = StudentStatusForm(
            instance=student
        )

    return render(
        request,
        "accounts/student_status.html",
        {
            "form": form,
            "student": student,
        },
    )