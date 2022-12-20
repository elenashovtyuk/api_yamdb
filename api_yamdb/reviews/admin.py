from django.contrib import admin

from .models import Title, Category, Genre

# Чтобы добавить эти модели в интерфейс администратора,
# их надо зарегистрировать в файле reviews/admin.py.

# В файле reviews/admin.py создаем классы
# TitleAdmin, CategoryAdmin, GenreAdmin,
# наследующиеся от admin.ModelAdmin,
# и зарегистрируем их как источники конфигурации для моделей
# Title, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name', 'year', 'description', 'category',)
    # Добавляем интерфейс для поиска по произведениям
    search_fields = ('name',)
    # Добавляем возможность фильтрации названию
    list_filter = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name', 'slug',)
    # добавляем интерфейс для поиска по категориям
    search_fields = ('name',)
    # добавляем возможность фильтрации по названию
    list_filter = ('name',)


class GenreAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name', 'slug',)
    # добавляем интерфейс для поиска по жанрам
    search_fields = ('name',)
    # добавляем возможность фильтрации по названию
    list_filter = ('name',)


# При регистрации модели Title источником конфигурации для неё назначаем
# класс TitleAdmin
admin.site.register(Title, TitleAdmin)
# При регистрации модели Category источником конфигурации для неё назначаем
# класс CategoryAdmin
admin.site.register(Category, CategoryAdmin)
# При регистрации модели Genre источником конфигурации для неё назначаем
# класс GenreAdmin
admin.site.register(Genre, GenreAdmin)
