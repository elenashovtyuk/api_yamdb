from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'title', 'author', 'score',)
    search_fields = ('text', 'author', 'title',)
    list_filter = ('title', 'author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'title', 'author')
    search_fields = ('text', 'author', 'title',)
    list_filter = ('title', 'author',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
