from django.db import models
from django.conf import settings


class Contact(models.Model):
    class Meta:
        ordering = ['address']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user id',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    address = models.CharField(
        'address of user',
        max_length=200,
        blank=True,
        null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        verbose_name='user id created this department',
        null=True,
        blank=True,
        related_name='contact_created_by'
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        verbose_name='user id modified this department',
        null=True,
        blank=True,
        related_name='contact_modified_by'
    )

    def __str__(self):
        return self.address if self.address else ''
