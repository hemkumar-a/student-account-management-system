from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = "accounts"


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "profile/edit/",
        views.profile_edit,
        name="profile_edit",
    ),

    path(
        "students/",
        views.student_list,
        name="student_list",
    ),

    path(
        "students/<int:pk>/",
        views.student_detail,
        name="student_detail",
    ),

    path(
        "students/add/",
        views.student_create,
        name="student_create",
    ),

    path(
        "students/<int:pk>/edit/",
        views.student_edit,
        name="student_edit",
    ),

    path(
        "students/<int:pk>/delete/",
        views.student_delete,
        name="student_delete",
    ),

    path(
        "students/<int:pk>/status/",
        views.student_status,
        name="student_status",
    ),
]