from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'publish', 'status')
    list_filter = ("status","publish")
    search_fields = ['title', 'content']
    prepopulated_fields = {'snippet': ('body'[:30],)}
    list_editable = ('status','user')
    ordering = ['-status', '-publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reply', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated', 'reply')
    search_fields = ('name', 'body')
    list_editable = ('active',)