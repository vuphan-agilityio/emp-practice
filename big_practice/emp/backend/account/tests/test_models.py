from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Employee
from backend.department.models import Department


class AccountModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@gmail.com', 'testpassword')
        self.department = Department.objects.create(name='department')

    def test_create_new_employee(self):
        employee = Employee.objects.create(
            user=self.user,
            department=self.department,
            age=23)
        self.assertTrue(employee)
