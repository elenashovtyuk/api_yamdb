from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from users.models import User

from .validators import validate_year


class Category(models.Model):
    """Модель категории произведения"""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        max_length=50,
        unique=True,
        validators=(RegexValidator(r'^[-a-zA-Z0-9_]+$'),)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанра произведения"""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )

    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        max_length=50,
        unique=True,
        validators=(RegexValidator(r'^[-a-zA-Z0-9_]+$'),)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )

    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )

    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True
    )

    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
        
        
class Review(models.Model):
    """Модель отзыва на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        null=True
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='Only the one review is allowed from every person'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария на отзыв."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение',
        null=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        null=True
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
