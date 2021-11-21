from django.contrib import admin
from .models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'publish', 'status')
    list_filter = ("status","publish")
    search_fields = ['title', 'content']
    prepopulated_fields = {'snippet': ('body'[:30],)}
    list_editable = ('status','user')
    ordering = ['-status', '-publish']

admin.site.register(Post, PostAdmin)