from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Department


class DepartmentModelsTestCase(TestCase):
    def test_create_new_department(self):
        department = Department.objects.create(name='department')
        self.assertTrue(department)
