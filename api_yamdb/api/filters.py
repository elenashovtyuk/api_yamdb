from django_filters import rest_framework as filters
from reviews.models import Title

# создадим свой класс-фильтр на основе FilterSet
# класса, который позволяет определить - как фильтровать различные поля модели
# name указывает, поле, которое нужно фильтровать
# lookup_expr


class FilterForTitle(filters.FilterSet):
    name = filters.CharFilter(field_name='name')
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
