from django.urls import path

from . import views

app_name = "course"

urlpatterns = [
    # Courses
    path("", views.course_list, name="course_list"),
    path("add/", views.course_create, name="course_create"),
    path("<int:pk>/", views.course_detail, name="course_detail"),
    path("<int:pk>/edit/", views.course_edit, name="course_edit"),
    path("<int:pk>/delete/", views.course_delete, name="course_delete"),

    # Departments
    path("departments/", views.department_list, name="department_list"),
    path(
        "departments/add/",
        views.department_create,
        name="department_create",
    ),
    path(
        "departments/<int:pk>/edit/",
        views.department_edit,
        name="department_edit",
    ),
    path(
        "departments/<int:pk>/delete/",
        views.department_delete,
        name="department_delete",
    ),

    # Programs
    path("programs/", views.program_list, name="program_list"),
    path(
        "programs/add/",
        views.program_create,
        name="program_create",
    ),
    path(
        "programs/<int:pk>/edit/",
        views.program_edit,
        name="program_edit",
    ),
    path(
        "programs/<int:pk>/delete/",
        views.program_delete,
        name="program_delete",
    ),

    # Course allocation
    path(
        "allocations/",
        views.allocation_list,
        name="allocation_list",
    ),
    path(
        "allocations/add/",
        views.allocation_create,
        name="allocation_create",
    ),
]