from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Result(models.Model):
    GRADE_CHOICES = [
        ("A", "A (5.00)"),
        ("B", "B (4.00)"),
        ("C", "C (3.00)"),
        ("D", "D (2.00)"),
        ("F", "F (0.00)"),
    ]

    GRADE_POINTS = {
        "A": Decimal("5.00"),
        "B": Decimal("4.00"),
        "C": Decimal("3.00"),
        "D": Decimal("2.00"),
        "F": Decimal("0.00"),
    }

    student = models.ForeignKey(
        "accounts.StudentProfile",
        on_delete=models.CASCADE,
        related_name="results",
    )

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="results",
    )

    assignment_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("30")),
        ],
    )

    exam_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("70")),
        ],
    )

    total_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        blank=True,
    )

    point = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
    )

    session = models.CharField(
        max_length=20,
    )

    semester = models.CharField(
        max_length=10,
    )

    class Meta:
        ordering = ["student", "course"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "course",
                    "session",
                    "semester",
                ],
                name="unique_student_course_result",
            )
        ]

    def calculate_grade(self):
        self.total_score = (
            self.assignment_score + self.exam_score
        )

        if self.total_score >= 70:
            self.grade = "A"
        elif self.total_score >= 60:
            self.grade = "B"
        elif self.total_score >= 50:
            self.grade = "C"
        elif self.total_score >= 45:
            self.grade = "D"
        else:
            self.grade = "F"

        self.point = self.GRADE_POINTS[self.grade]

    def save(self, *args, **kwargs):
        self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.course.code} - "
            f"{self.grade}"
        )


class AssessmentResult(models.Model):
    student = models.OneToOneField(
        "accounts.StudentProfile",
        on_delete=models.CASCADE,
        related_name="gpa_record",
    )
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_cgpa(self):
        results = Result.objects.filter(student=self.student)

        total_credits = 0
        weighted_points = 0

        for result in results:
            credit = result.course.credit
            total_credits += credit
            weighted_points += result.point * credit

        if total_credits:
            self.cgpa = round(
                weighted_points / total_credits,
                2,
            )
        else:
            self.cgpa = 0

        return self.cgpa

    def save(self, *args, **kwargs):
        self.calculate_cgpa()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.student_id} - CGPA {self.cgpa}"