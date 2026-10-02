from django import forms

from .models import AssessmentResult, Result


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "student",
            "course",
            "assignment_score",
            "exam_score",
            "session",
            "semester",
        ]

    def clean(self):
        cleaned_data = super().clean()

        assignment_score = cleaned_data.get("assignment_score")
        exam_score = cleaned_data.get("exam_score")

        if assignment_score is not None and exam_score is not None:
            total = assignment_score + exam_score

            if total > 100:
                raise forms.ValidationError(
                    "Assignment score and exam score cannot exceed 100."
                )

        return cleaned_data


class AssessmentResultForm(forms.ModelForm):
    class Meta:
        model = AssessmentResult
        fields = ["student"]
