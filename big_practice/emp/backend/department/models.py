from django.db import models
from django.conf import settings


class Department(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField('name of department', max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, verbose_name='user id created this department', null=True, blank=True, related_name='department_created_by')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, verbose_name='user id modified this department', null=True, blank=True, related_name='department_modified_by')

    def __str__(self):
        return self.name if self.name else ''
