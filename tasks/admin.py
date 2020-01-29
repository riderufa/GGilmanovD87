from django.contrib import admin

from tasks.models import *


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'todos_count')

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'todos_count')

