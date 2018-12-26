from django.db import models
from django.db.models import Avg
from django.conf import settings

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import SmartResize, Transpose

from ..department.models import Department


class EmployeeManager(models.Manager):
    # def get_queryset(self):
    #     return super().get_queryset().filter(status_code=1)

    def with_age_great_more_than_25(self):
        return self.filter(age__gt=25)

    def with_aggregate_avg_age_of_employees(self):
        return self.aggregate(Avg('age'))

    def with_raw_sql_get_employees_has_status_code_is_true(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM account_employee WHERE status_code = 1")
            row = cursor.fetchall()
            return row

    def with_raw_sql_get_employees_get_age_great_more_than_25(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM account_employee WHERE age > 25")
            row = cursor.fetchall()
            return row

    def with_raw_sql_get_avg_of_employees(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT AVG(age) FROM account_employee")
            row = cursor.fetchall()
            return row


class Employee(models.Model):
    class Meta():
        ordering = ['first_name']

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        verbose_name='user id',
        blank=True, null=True)
    department = models.ForeignKey(
        Department,
        models.SET_NULL,
        verbose_name='department id',
        blank=True, null=True)
    status_code = models.SmallIntegerField('status code activity of user', default=0)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField('age of user', blank=True, null=True)
    about_me = models.CharField('introduce about me of user', max_length=400)
    birthday = models.DateTimeField(
        'birthday of user',
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True)
    avatar_original = ProcessedImageField(
        null=True,
        blank=True,
        processors=[Transpose()],
        format='JPEG',
        options={'quality': 50})
    small = ImageSpecField(
        source='avatar_original',
        processors=[Transpose(), SmartResize(640, 505)],
        format='JPEG',
        options={'quality': 50})
    medium = ImageSpecField(
        source='avatar_original',
        # processors=[Transpose(), ResizeToFit(640, 600, False)],
        # processors=[Transpose(), SmartResize(320, 300)],
        processors=[Transpose(), SmartResize(640, 600)],
        format='JPEG',
        options={'quality': 70})
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    objects = EmployeeManager()

    def full_name(self):
        """Custom full name method as a property."""
        return str(self.first_name) + ' ' + str(self.last_name)

    def __str__(self):
        """Default string."""
        return self.user.email if self.user else ''
