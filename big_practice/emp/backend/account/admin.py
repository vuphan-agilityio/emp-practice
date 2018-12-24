"""Modifying admin page."""
from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'first_name', 'last_name')
    list_filter = ('department__name', )
    search_fields = ('first_name', 'last_name', )

admin.site.register(Employee, EmployeeAdmin)
