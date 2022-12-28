from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_me

USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Модель User проекта."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Недопустимое имя пользователя'
            ),
            validate_me,)
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=13,
        choices=USER_ROLES,
        blank=True,
        null=True,
        default='user'
    )

    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    @property
    def is_admin(self):
        """Свойство наличия у пользователя роли администратора."""
        return self.role == 'admin'

    @property
    def is_moderator(self):
        """Свойство наличия у пользователя роли модератора."""
        return self.role == 'moderator'

    @property
    def is_user(self):
        """Свойство наличия у пользователя роли обычного
        пользователя. """
        return self.role == 'user'

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.email
