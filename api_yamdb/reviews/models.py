from django.db import models
from .validators import validate_year
from django.core.validators import RegexValidator


# создаем модель категорий произведений
# у нее будет 2 поля - название категории и ее идентификатор
class Category(models.Model):
    """Модель категории произведения"""
    name = models.CharField(
        verbose_name='Название категории',
        # по ТЗ есть ограничение длины этого текстового поля,
        # указываем это в параметре max_length
        max_length=256
    )
    # поле slug должно быть уникальным,
    # поэтому указываем в параметрах unique = True
    # Также по ТЗ есть ограничение длины этого текстового поля,
    # указываем это в параметре max_length
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


# создаем модель жанров произведений
# у нее также два поля - название жанра и его идентификатор
class Genre(models.Model):
    """Модель жанра произведения"""
    name = models.CharField(
        verbose_name='Название жанра',
        # по ТЗ есть ограничение длины этого текстового поля,
        # указываем это в параметре max_length
        max_length=256
    )

    # поле slug должно быть уникальным,
    # поэтому указываем в параметрах unique = True
    # Также по ТЗ есть ограничение длины этого текстового поля,
    # указываем это в параметре max_length
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
    # по ТЗ есть ограничение длины этого текстового поля,
    # указываем это в параметре max_length
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

        # добавляем опцию для поля - blank
        # т.е есть возможность добавлять произведение без описания
        # это поле не является обязательным cогласно ТЗ
        blank=True
    )

    # Т.к по ТЗ одно произведение может быть привязано
    # только к одной категории,
    # то используем тип поля ForeignKey(cвязь один-ко-многим)
    # поле category определяем как внешний ключ.
    # Оно будет хранить идентификатор категории этого произведения
    # т.е поле category представляет собой
    # отношение к другой таблице - Category
    # согласно ТЗ при удалении объекта категории Category
    # не нужно удалять связанные с этой категорией произведения
    # для этого в указываем параметр on_delete = models.SET_NULL
    # Этот параметр определяет, должно ли происходить удаление.
    # Он сообщает, что делать, когда родительское значение удалено.
    # Для нашего случая категория будет удаляться
    # без удаления связанного произведения
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True
    )

    # rating = models.IntegerField(
    #     verbose_name='Рейтинг',
    #     null=True,
    #     default=None
    # )

    # Так как одно произведение может быть привязано к нескольким жанрам,
    #  то используем тип поля ManyToMany
    # поле genre представляет собой отношение к другой таблице Genre
    # в конструктор models.ManyToMany передаем модель,
    # с которой установливаются отношения
    # "многие-ко-многим" - модель Жанра
    # в итоге между 2-мя этими таблицами(Title и Genre)
    # будет создана промежуточная таблица,
    #  через которую и будет осуществляться связь

    # согласно ТЗ при удалении объекта жанра Genre
    # не нужно удалять связанные с этим жанром произведения
    # для этого в указываем параметр on_delete = models.SET_NULL
    # Этот параметр определяет, должно ли происходить удаление.
    # Он сообщает, что делать, когда родительское значение удалено.
    # Для нашего случая жанр будет удаляться
    # без удаления связанного произведения
    # указываем параметр blank = True,
    # чтобы была возможность создавать экземпляры модели Title без категории

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
        # в качестве дополнительного парамметра указываем throught
        #  здесь указываем промежуточную модель,
        # через которую обеспечивается связь
        # многие ко многим между моделями Title и Genre
        # through='GenreTitle',

    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
