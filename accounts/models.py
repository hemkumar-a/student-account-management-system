from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom manager for email-based authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")

        if not extra_fields.get("is_superuser"):
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractUser):
    """
    Custom user model for the Student Account Management System.
    """

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
    )

    is_student = models.BooleanField(
        default=False,
        verbose_name="Student",
    )

    is_lecturer = models.BooleanField(
        default=False,
        verbose_name="Lecturer",
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        upload_to="profile_pictures/",
        default="default.png",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        full_name = self.get_full_name()

        if full_name:
            return full_name

        return self.email


class StudentProfile(models.Model):
    """
    Additional academic information belonging to a student account.
    """

    STATUS_ACTIVE = "active"
    STATUS_SUSPENDED = "suspended"
    STATUS_GRADUATED = "graduated"
    STATUS_WITHDRAWN = "withdrawn"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_SUSPENDED, "Suspended"),
        (STATUS_GRADUATED, "Graduated"),
        (STATUS_WITHDRAWN, "Withdrawn"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    student_id = models.CharField(
        max_length=20,
        unique=True,
    )

    department = models.ForeignKey(
        "course.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )

    admission_date = models.DateField(
        default=timezone.now,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["student_id"]

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def is_active_student(self):
        return self.status == self.STATUS_ACTIVE