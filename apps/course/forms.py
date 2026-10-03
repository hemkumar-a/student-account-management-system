from django import forms

from .models import Course, CourseAllocation, Department, Program


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["title", "code", "summary"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ["title", "department", "summary"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "code",
            "credit",
            "program",
            "semester",
            "is_elective",
            "summary",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
        }


class CourseAllocationForm(forms.ModelForm):
    class Meta:
        model = CourseAllocation
        fields = ["student", "courses", "session"]
        widgets = {
            "courses": forms.CheckboxSelectMultiple(),
        }