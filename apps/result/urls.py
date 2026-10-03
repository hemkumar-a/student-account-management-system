from django.urls import path

from . import views

app_name = "result"

urlpatterns = [
    path("", views.result_list, name="result_list"),
    path("add/", views.result_create, name="result_create"),
    path("<int:pk>/", views.result_detail, name="result_detail"),
    path("<int:pk>/edit/", views.result_edit, name="result_edit"),
    path("<int:pk>/delete/", views.result_delete, name="result_delete"),

    path("transcript/", views.transcript, name="transcript"),
    path("performance/", views.performance, name="performance"),
    path(
        "assessment/add/",
        views.assessment_create,
        name="assessment_create",
    ),
]