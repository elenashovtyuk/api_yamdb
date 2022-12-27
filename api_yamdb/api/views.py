from django.core.validators import RegexValidator
# from django.shortcuts import render
from rest_framework import filters, viewsets
# from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

# из приложения reviews импортируем все нужные модели
from reviews.models import Category, Genre, Title
from .filters import FilterForTitle
from .mixins import CLDViewSet
# из приложения api импортируем необходимые кастомные пермишнс
# для моделей Title, Category, Genre это IsAdminOrReadOnly
# from .permissions  import IsAdminOrReadOnly
from .permissions import (IsAdminOrReadOnly,)
# из приложения api импортируем все нужные сериализаторы
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          ReadOnlyTitleSerializer,
                          TitleSerializer)


# для создания вьюсета для Title используем класс ModelViewSet
# он может обрабатывать все 6 типичных действий с моделями
# (create, retriev, list, update, partial_update, destroy)
# при создании вьюсета указываем 2 обязательных поля
# qweryset- выборка объектов модели, с которой будет работать вьюсет
# serializer_class - сериализатор,
# который будет применяться для сериализации и валидации

# а для создания вьюсетов для Genre и Category
# создадим свой базовый класс в файле mixins.py
# который будет включать в себя только три нужных нам вьюсета
# которые отвечают за получение списка объектов,
# добавление  и удаление объекта
# плюс GenericViewSet.

# создадим вьюсет для модели Category
class CategoryViewSet(CLDViewSet):
    """Отображение действий с категориями произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    validators = (RegexValidator(r'^[-a-zA-Z0-9_]+$'))
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    # lookup_field = 'slug'

    # чтобы создать ограничение прав доступа на уровне вьюсетов
    # нужно добавить параметр permission_classes
    # и в виде кортежа указать один или несколько кастомных пермишнс
    # permission_classes = (IsAdminOrReadOnly,)


# создадим вьюсет для модели Genre
class GenreViewSet(CLDViewSet):
    """Отображение действий с жанрами произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    validators = (RegexValidator(r'^[-a-zA-Z0-9_]+$'))
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    # lookup_field = 'slug'

    # чтобы создать ограничение прав доступа на уровне вьюсетов
    # нужно добавить параметр permission_classes
    # и в виде кортежа указать один или несколько кастомных пермишнс
    # permission_classes = (IsAdminOrReadOnly,)


# создадим вьюсет для модели Title
class TitleViewSet(viewsets.ModelViewSet):
    """Отображение действий с произведениями"""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle
    # так как для модели Title у нас 2 сериализатора, то во вьюсете для Title
    # мы не указываем serializer_class,
    # а переопределяем метод get_serializer_class()
    # указывая в каком случае(при каком типе запроса)
    # какой сериализатор использовать
    # если эти действия связаны с получением кверисета
    # или отдельного экземпляра, то применяем сериализатор для чтения
    # в противном случае(при любых других действиях)
    # применяем второй сериализатор(для записи)

    # чтобы создать ограничение прав доступа на уровне вьюсетов
    # нужно добавить параметр permission_classes
    # и в виде кортежа указать один или несколько кастомных пермишнс
    # permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retriev'):
            return ReadOnlyTitleSerializer
        return TitleSerializer
