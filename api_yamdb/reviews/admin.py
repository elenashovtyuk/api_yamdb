from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'title', 'score',)
    search_fields = ('text', 'author', 'title')
    list_filter = ('title', 'author', 'score')
    ordering = ('-score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'review', 'title', 'author',)
    search_fields = ('text', 'author', 'review')
    list_filter = ('title', 'author', 'review')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
