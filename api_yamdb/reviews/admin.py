from django.contrib import admin

from .models import Title, Category, Genre, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'title', 'score',)
    search_fields = ('text', 'author', 'title')
    list_filter = ('title', 'author', 'score')
    ordering = ('-score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'review', 'title', 'author',)
    search_fields = ('text', 'author', 'review')
    list_filter = ('title', 'author', 'review')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
