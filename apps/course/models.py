from django.db import models


class Department(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
    )

    summary = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class Program(models.Model):
    title = models.CharField(
        max_length=150,
    )

    summary = models.TextField(
        blank=True,
        null=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programs",
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    SEMESTER_CHOICES = [
        ("1st", "First Semester"),
        ("2nd", "Second Semester"),
        ("3rd", "Third Semester"),
        ("4th", "Fourth Semester"),
        ("5th", "Fifth Semester"),
        ("6th", "Sixth Semester"),
        ("7th", "Seventh Semester"),
        ("8th", "Eighth Semester"),
    ]

    title = models.CharField(
        max_length=200,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    credit = models.PositiveIntegerField(
        default=3,
    )

    summary = models.TextField(
        blank=True,
        null=True,
    )

    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES,
    )

    is_elective = models.BooleanField(
        default=False,
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="courses",
    )

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class CourseAllocation(models.Model):
    student = models.ForeignKey(
        "accounts.StudentProfile",
        on_delete=models.CASCADE,
        related_name="allocations",
    )

    courses = models.ManyToManyField(
        Course,
        related_name="allocations",
    )

    session = models.CharField(
        max_length=20,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.student_id} - {self.session}"