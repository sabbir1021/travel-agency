from django.contrib import admin
from .models import Category, Post
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'title','active']
    search_fields = ['title', 'category__name','user__username']
    list_editable = ['active']
    list_per_page = 20


admin.site.register(Post, PostAdmin)
