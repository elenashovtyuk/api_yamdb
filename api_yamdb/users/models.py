from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from .validators import validate_me


USER_ROLES = (
    ("user", "пользователь"),
    ("moderator", "модератор"),
    ("admin", "администратор"),
    )

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(RegexValidator(regex=r'^[\w.@+-]+\Z',  message= 'недопустимое имя пользователя',),
        validate_me)
        )
    email = models.EmailField(verbose_name="Электронная почта", max_length=254, unique=True)
    bio = models.TextField(
        verbose_name="Биография пользователя",
        blank=True,
        null=True,
    )
    confirmation_code = models.CharField(
        verbose_name="Код подтверждения", max_length=6, default="000000"
    )
    role = models.CharField(
        verbose_name="Роль пользователя",
        max_length=9,
        choices=USER_ROLES,
        default="user",
        blank=True,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username")

    objects =  UserManager()

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"



    def __str__(self):
        return self.email
