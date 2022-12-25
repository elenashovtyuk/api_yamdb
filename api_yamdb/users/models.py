from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(
        self, username, email, password=None,**extra_fields
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        username,
        email,
        password,
        **extra_fields
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.is_staff=True
        user.is_superuser=True
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    bio = models.TextField(
        verbose_name="Биография пользователя",
        blank=True,
        null=True,
    )
    confirmation_code = models.CharField(
        verbose_name="Код подтверждения", max_length=6, default="000000"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    USER_ROLE = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )

    role = models.CharField(
        verbose_name="Роль пользователя",
        max_length=9,
        choices=USER_ROLE,
        default="user",
        blank=True,
        null=True,
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email
